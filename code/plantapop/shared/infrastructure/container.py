from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from plantapop.config import Config
from plantapop.shared.infrastructure import endpoints
from plantapop.shared.infrastructure.repository import sqlalchemy_uow

config = Config.get_instance()


engine = create_engine(config.postgres.url, echo=True)


class SessionFactory:
    def __init__(self):
        self.session = orm.scoped_session(
            orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

    def __call__(self):
        return self.session

    def __del__(self):
        self.session.close()


class SessionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[endpoints, sqlalchemy_uow])

    session = providers.Factory(SessionFactory)
