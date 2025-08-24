# Standard
import asyncio
import time

# Third-party
from loguru import logger

# local
from synesthesia.cover_fetch.get_last_album_cover import (
    get_last_album_cover,
    turn_link_into_image,
)
from synesthesia.cover_fetch.save_image import save_image
from synesthesia.environment_variables import API_KEY
from synesthesia.utils import get_main_hue_hex, gradient_hex
from synesthesia.rgb_control import RGBController

MAC = "be:59:a4:01:7b:84"
CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"  

async def main():
    while True:
        try:
            async with RGBController(MAC, CHAR_UUID) as rgb:
                current_album: str = ""
                current_hex_colour: str = ""
                last_album: str = ""
                last_hex_colour: str = "000000"
                while True:
                    if response := get_last_album_cover("codeling", API_KEY):
                        current_album, image_link = response 
                    else:
                        await asyncio.sleep(5)
                        continue
                    
                    if current_album != last_album:
                        img = turn_link_into_image(image_link)
                        img_path = save_image(img)
                        current_hex_colour = get_main_hue_hex(img_path)
                        logger.info(f"Color hex: {current_hex_colour}")

                        for gr_colour in gradient_hex(last_hex_colour, current_hex_colour, steps=50):
                            await rgb.send(gr_colour)
                            await asyncio.sleep(0.02)

                        last_hex_colour = current_hex_colour
                        last_album = current_album

                    await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"{e}")

        finally:
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
