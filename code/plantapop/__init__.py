from fastapi import FastAPI

from plantapop.shared_kernel.config import Config
from plantapop.shared_kernel.controller import Controller

app = FastAPI()
CONFIGMAP = Config.get_instance()

Controller(app).register()

__all__ = ["app", "CONFIGMAP"]
