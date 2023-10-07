from fastapi import FastAPI

from plantapop.config import Config
from plantapop.controller import Controller

app = FastAPI()
CONFIGMAP = Config.get_instance()

controller = Controller(app)
controller.register()

__all__ = ["app", "CONFIGMAP"]
