from fastapi import FastAPI

from plantapop.config import Config
from plantapop.shared.infrastructure.container import SessionContainer, engine
from plantapop.shared.infrastructure.endpoints import FastApiEndpoints

session_container = SessionContainer()
CONFIGMAP = Config.get_instance()


def configure_database(container):
    from plantapop.shared.infrastructure.repository.database import Base

    Base.metadata.create_all(bind=engine)


def create_app():
    app = FastAPI()

    app.config = CONFIGMAP
    app.session = session_container
    app = FastApiEndpoints(app).register()
    configure_database(session_container)
    return app


app = create_app()


__all__ = ["app", "CONFIGMAP"]
