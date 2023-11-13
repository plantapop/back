from fastapi import FastAPI

from plantapop.config import Config
from plantapop.shared_kernel.infrastructure.container import SessionContainer
from plantapop.shared_kernel.infrastructure.endpoints import FastApiEndpoints

session_container = SessionContainer()

app = FastAPI()
CONFIGMAP = Config.get_instance()

app.config = CONFIGMAP
app.session = session_container
app = FastApiEndpoints(app).register()

__all__ = ["app", "CONFIGMAP"]
