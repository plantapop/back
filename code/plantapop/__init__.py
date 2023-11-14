from fastapi import FastAPI

from plantapop.config import Config
from plantapop.shared_kernel.infrastructure.container import SessionContainer
from plantapop.shared_kernel.infrastructure.endpoints import FastApiEndpoints

session_container = SessionContainer()
CONFIGMAP = Config.get_instance()


def create_app():
    app = FastAPI()

    app.config = CONFIGMAP
    app.session = session_container
    app = FastApiEndpoints(app).register()
    return app


app = create_app()


__all__ = ["app", "CONFIGMAP"]
