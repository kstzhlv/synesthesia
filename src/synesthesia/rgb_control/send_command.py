# Stadard
import asyncio

# Third-party
from bleak import BleakClient
from loguru import logger

MAC = "be:59:a4:01:7b:84"
CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"  

class RGBController:
    COMMAND_PREFIX = "7e070503"
    COMMAND_POSTFIX = "000010ef"
    def __init__(self, address: str, char_uuid: str):
        self.address = address
        self.char_uuid = char_uuid
        self.client: BleakClient | None = None

    async def __aenter__(self):
        self.client = BleakClient(self.address)
        await self.client.__aenter__()
        if not self.client.is_connected:
            raise RuntimeError("Not connected")
        logger.info(f"Connected to {self.address}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

        print(f"Disconnected from {self.address}")

    async def send(self, colour_hex: str):
        if len(colour_hex) != 6:
            logger.error("Length of colour hex must be 6")
        try:
            data = bytes.fromhex("".join([self.COMMAND_PREFIX, colour_hex, self.COMMAND_POSTFIX]))
            if self.client:
                await self.client.write_gatt_char(self.char_uuid, data, response=False)
                logger.info(f"Sent {data.hex()} to {self.char_uuid}")
            else:
                logger.error("Can't send colour command: connection is not asstablished")
        except Exception as e:
            logger.error(f"Failed to send {colour_hex}: {e}")


async def main():
    async with RGBController(MAC, CHAR_UUID) as rgb:
        await rgb.send("0000ff")


if __name__ == "__main__":
    asyncio.run(main())
