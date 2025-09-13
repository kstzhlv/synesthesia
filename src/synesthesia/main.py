# Standard
import asyncio
import configparser
from pathlib import Path

# Third-party
from loguru import logger

# local
from synesthesia.config_parsing import parse_config
from synesthesia.cover_fetch.get_last_album_cover import (
    get_last_album_cover,
    turn_link_into_image,
)
from synesthesia.cover_fetch.save_image import save_image
from synesthesia.resolve_bluetooth_device import resolve_bluetooth_device
from synesthesia.rgb_control import RGBController
from synesthesia.utils import get_main_hue_hex, gradient_hex


def create_config_dir_if_not_exists():
    config_path = Path.home() / ".config" / "synesthesia"
    config_path.mkdir(exist_ok=True)

    return config_path


async def run():
    config_path = create_config_dir_if_not_exists()
    config_params = parse_config(config_path)

    MAC = config_params["device"]["MAC"]
    CHAR_UUID = config_params["device"]["CHAR_UUID"]
    DEVICE_NAME = config_params["device"]["DEVICE_NAME"]
    API_KEY = config_params["lastfm"]["API_KEY"]
    USER_NAME = config_params["lastfm"]["USERNAME"]

    ble_device = await resolve_bluetooth_device(MAC, DEVICE_NAME)
    if ble_device is None:
        raise RuntimeError(f"Bluetooth device ({MAC}) not found after scan")

    while True:
        try:
            async with RGBController(ble_device, CHAR_UUID) as rgb:
                current_album: str = ""
                current_hex_colour: str = ""
                last_album: str = ""
                last_hex_colour: str = "000000"
                while True:
                    if response := get_last_album_cover(USER_NAME, API_KEY):
                        current_album, image_link = response
                    else:
                        await asyncio.sleep(5)
                        continue

                    if current_album != last_album:
                        img = turn_link_into_image(image_link)
                        img_path = save_image(img)
                        current_hex_colour = get_main_hue_hex(img_path)
                        logger.info(f"Color hex: {current_hex_colour}")

                        for gr_colour in gradient_hex(
                            last_hex_colour, current_hex_colour, steps=50
                        ):
                            await rgb.send(gr_colour)
                            await asyncio.sleep(0.02)

                        last_hex_colour = current_hex_colour
                        last_album = current_album

                    await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"{e}")

        finally:
            await asyncio.sleep(5)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
