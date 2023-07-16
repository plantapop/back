import os
import yaml
import threading
from typing import Optional
from dataclasses import dataclass

EXCEPTION_MESSAGE = "CONFIGMAP_PATH environment variable not set \ntry: export CONFIGMAP_PATH=config/configmap.yml"


@dataclass(frozen=True)
class ConfigType:
    HOST: str
    PORT: int
    RELOAD: bool
    WORKERS: int
    ENVIRONMENT: str
    LOG_LEVEL: str


class Config:
    _instance: Optional[ConfigType] = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def _load_config(cls) -> ConfigType:
        config_path = os.environ.get("CONFIGMAP_PATH", False)

        if not config_path:
            raise Exception(EXCEPTION_MESSAGE)

        with open(config_path, "r") as config_file:
            config_data = yaml.safe_load(config_file)
        return ConfigType(**config_data)

    def __new__(cls) -> ConfigType:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._load_config()
        return cls._instance
