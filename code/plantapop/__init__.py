from fastapi import FastAPI

from plantapop.config import Config

CONFIGMAP = Config.get_instance()


def get_base():
    from plantapop.shared.infrastructure.repository.database import Base

    return Base


def configure_database(container, engine):
    Base = get_base()

    Base.metadata.create_all(bind=engine)


def create_app():
    app = FastAPI()
    from plantapop.shared.infrastructure.container import SessionContainer, engine
    from plantapop.shared.infrastructure.endpoints import FastApiEndpoints

    session_container = SessionContainer()

    app.config = CONFIGMAP
    app.session = session_container
    app = FastApiEndpoints(app).register()
    configure_database(session_container, engine)
    return app
