
from fastapi import FastAPI

from plantapop.config import Config
from plantapop.shared.infrastructure.container import SessionContainer, engine
from plantapop.shared.infrastructure.repository.database import Base  # noqa

CONFIGMAP = Config.get_instance()


def get_base():
    from plantapop.shared.infrastructure.token.token_repository import (  # noqa
        RefreshToken,
    )

    return Base


async def init_models():
    Base = get_base()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def create_app():
    app = FastAPI()
    from plantapop.shared.infrastructure.endpoints import FastApiEndpoints

    session_container = SessionContainer()

    app.config = CONFIGMAP
    app.session = session_container
    app = FastApiEndpoints(app).register()
    return app
