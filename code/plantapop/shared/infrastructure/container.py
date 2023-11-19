from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from plantapop.config import Config
from plantapop.shared.infrastructure import endpoints
from plantapop.shared.infrastructure.token import token_repository

config = Config.get_instance()


engine = create_engine(config.postgres.url, echo=True)


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[endpoints, token_repository]
    )

    session = providers.Singleton(
        orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        )
    )
