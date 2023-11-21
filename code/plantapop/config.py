import os
import threading
from typing import Optional

from omegaconf import DictConfig, ListConfig, OmegaConf

EXCEPTION_MESSAGE = "CONFIGMAP_PATH environment variable not set \n'\
try: export CONFIGMAP_PATH=config/configmap.yml"


class Config:
    """
    Singleton class to load the configmap.yml file
    """

    _instance: Optional[ListConfig | DictConfig] = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def _load_config(cls) -> DictConfig | ListConfig:
        config_path = os.getenv("CONFIGMAP_PATH")
        if not config_path:
            raise ValueError(EXCEPTION_MESSAGE)
        return OmegaConf.load(config_path)

    @classmethod
    def get_instance(cls) -> DictConfig | ListConfig:
        if cls._instance is None:
            cls._instance = cls._load_config()
        return cls._instance
