from fastapi import FastAPI
from plantapop.config import Config

app = FastAPI()
configmap = Config()

__all__ = ["app", "configmap"]
