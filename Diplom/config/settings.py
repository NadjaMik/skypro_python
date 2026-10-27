"""Загрузчик настроек проекта из config.ini."""
import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.ini"


class Settings:
    """Настройки тестового проекта, загруженные из config.ini."""

    def __init__(self, config_path: Path = CONFIG_PATH) -> None:
        parser = configparser.ConfigParser()
        if not parser.read(config_path, encoding="utf-8"):
            raise FileNotFoundError(f"Конфиг не найден: {config_path}")
        self.ui_base_url: str = parser["common"]["ui_base_url"]
        self.api_base_url: str = parser["common"]["api_base_url"]
        self.company_name: str = parser["common"]["company_name"]
        self.user_id: str = parser["common"]["user_id"]
        self.default_timeout: int = int(parser["timeouts"]["default"])


settings = Settings()
