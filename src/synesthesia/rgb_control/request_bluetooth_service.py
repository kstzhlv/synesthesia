import asyncio
from typing import Dict, Any
from bleak import BleakClient

RGB_MAC = "be:59:a4:01:7b:84"

async def request_bluetooth_services(rgb_mac: str) -> Dict[str, Any]:
    result_services: Dict[str, Any] = {}
    async with BleakClient(rgb_mac) as client:
        if not client.is_connected:
            raise RuntimeError("Not connected.")

        svcs = client.services
        for service in svcs:
            chars_dict = {}
            for char in service.characteristics:
                descs_list = [str(desc.uuid) for desc in char.descriptors]
                chars_dict[str(char.uuid)] = {
                    "description": char.description or "",
                    "properties": list(char.properties),
                    "descriptors": descs_list,
                }

            result_services[str(service.uuid)] = {
                "description": service.description or "",
                "characteristics": chars_dict,
            }

    return result_services

async def main():
    result = await request_bluetooth_services(RGB_MAC)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())

