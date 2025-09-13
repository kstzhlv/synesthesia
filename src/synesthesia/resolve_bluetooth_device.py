# Standard
from typing import Literal

# Third-party
from bleak import BleakScanner
from loguru import logger


async def resolve_bluetooth_device(
    mac: str | None,
    name_hint: str | None,
    timeout: float = 30.0,
    adapter: str | None = "hci0",
    scanning_mode: Literal["active", "passive"] = "active",
):
    mac = (mac or "").strip().lower()
    print(mac)
    name_hint = (name_hint or "").strip()

    scanner = BleakScanner(adapter=adapter, scanning_mode=scanning_mode)

    dev = None
    if mac:
        dev = await scanner.find_device_by_address(mac, timeout=timeout)

    if dev is None and name_hint:

        def _flt(d, ad):
            return (d.name or "").startswith(name_hint)

        dev = await scanner.find_device_by_filter(_flt, timeout=timeout)

    logger.info(
        f"[resolver] adapter={adapter} mode={scanning_mode} mac={mac} "
        f"name_hint={name_hint} -> dev={getattr(dev, 'address', None)} {getattr(dev, 'name', None)}"
    )
    return dev
