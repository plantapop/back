from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from plantapop.config import Config

config = Config.get_instance()


engine = create_engine(config.postgres.url, echo=True)


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "plantapop.shared.infrastructure.endpoints",
            "plantapop.shared.infrastructure.token.token_repository",
        ]
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
