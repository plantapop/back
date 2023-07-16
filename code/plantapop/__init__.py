from fastapi import FastAPI

from plantapop.config import Config

app = FastAPI()
CONFIGMAP = Config.get_instance()

__all__ = ["app", "CONFIGMAP"]
