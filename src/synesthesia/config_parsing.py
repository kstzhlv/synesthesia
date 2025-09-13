# Standard
import configparser
from pathlib import Path


def parse_config(config_dir: Path) -> dict[str, dict[str, str]]:
    config_path = config_dir / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    required = {
        "device": ["MAC", "CHAR_UUID", "DEVICE_NAME"],
        "lastfm": ["API_KEY", "USERNAME"],
    }

    result: dict[str, dict[str, str]] = {}

    for section, keys in required.items():
        if not parser.has_section(section):
            raise ValueError(f"Config missing [{section}] section")

        result[section] = {}
        for key in keys:
            if not parser.has_option(section, key):
                raise ValueError(f"Missing key '{key}' in [{section}] section")
            result[section][key] = parser.get(section, key)

    return result
