from plantapop.accounts.infrastructure.repository import SQLUser
from plantapop.shared.infrastructure.event.sqlalchemy_failover_event_bus import (
    SQLDomainEvent,
)
from plantapop.shared.infrastructure.repository.database import Base
from plantapop.shared.infrastructure.token.token_repository import SQLRefreshToken

all_models = [SQLRefreshToken, SQLDomainEvent, SQLUser]


def get_base():
    return Base
