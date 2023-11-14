from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from plantapop.config import Config

config = Config.get_instance()


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["plantapop.shared_kernel.infrastructure.endpoints"]
    )

    session = providers.Singleton(
        orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=create_engine(config.postgres.url, echo=True),
            )
        )
    )
