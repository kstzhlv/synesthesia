
# Third-party
from bleak import BleakClient
from loguru import logger


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

        logger.warning(f"Disconnected from {self.address}")

    async def send(self, colour_hex: str):
        if len(colour_hex) != 6:
            logger.error("Length of colour hex must be 6")

        data = bytes.fromhex("".join([self.COMMAND_PREFIX, colour_hex, self.COMMAND_POSTFIX]))
        if self.client:
            await self.client.write_gatt_char(self.char_uuid, data, response=False)
            logger.info(f"Sent {data.hex()} to {self.char_uuid}")
        else:
            logger.error("Can't send colour command: connection is not asstablished")

