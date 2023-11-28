from fastapi import FastAPI

from plantapop.config import Config
from plantapop.shared.infrastructure.container import SessionContainer
from plantapop.shared.infrastructure.controller.endpoints import FastApiEndpoints

configmap = Config.get_instance()


def create_app():
    app = FastAPI()

    session_container = SessionContainer()

    app.config = configmap
    app.session = session_container
    app = FastApiEndpoints(app).register()
    return app
