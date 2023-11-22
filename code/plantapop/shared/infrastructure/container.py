from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from plantapop.config import Config
from plantapop.shared.infrastructure import endpoints
from plantapop.shared.infrastructure.repository import sqlalchemy_uow

config = Config.get_instance()


engine = create_engine(config.postgres.url, echo=False)


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[endpoints, sqlalchemy_uow])

    session = providers.Factory(
        lambda: orm.sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )()
    )
