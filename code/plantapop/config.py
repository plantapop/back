import os
import threading
from typing import Optional

import yaml
from pydantic_settings import BaseSettings

EXCEPTION_MESSAGE = "CONFIGMAP_PATH environment variable not set \n'\
try: export CONFIGMAP_PATH=config/configmap.yml"


class ConfigType(BaseSettings):
    """
    ConfigType class to load the configmap
    """

    HOST: str
    PORT: int
    RELOAD: bool
    WORKERS: int
    ENVIRONMENT: str
    LOG_LEVEL: str

    class Config:
        frozen = True


class Config:
    """
    Singleton class to load the configmap.yml file
    """

    _instance: Optional[ConfigType] = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def _load_config(cls) -> ConfigType:
        config_path = os.getenv("CONFIGMAP_PATH")
        if not config_path:
            raise ValueError(EXCEPTION_MESSAGE)
        with open(config_path, "r", encoding="utf-8") as config_file:
            config_data = yaml.safe_load(config_file)
        return ConfigType(**config_data)

    @classmethod
    def get_instance(cls) -> ConfigType:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls._load_config()
        return cls._instance
