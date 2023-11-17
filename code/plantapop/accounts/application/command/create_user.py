from plantapop.accounts.domain.repository import UserRepository
from plantapop.accounts.domain.services import check_email, check_uuid
from plantapop.accounts.domain.user import User
from plantapop.accounts.infrastructure.dto.registration import RegistrationDto
from plantapop.shared.domain.bus.event_bus import EventBus


class CreateUserCommandHandler:
    def __init__(self, user_repository: UserRepository, event_bus: EventBus):
        self.user_repository = user_repository
        self.event_bus = event_bus

    def execute(self, user_dto: RegistrationDto):
        user = User.create(
            uuid=user_dto.uuid,
            name=user_dto.name,
            surnames=user_dto.surnames,
            email=user_dto.email,
            password=user_dto.password,
            timezone=user_dto.timezone,
            language=user_dto.prefered_language,
        )

        check_uuid.check(repository=self.user_repository, uuid=user.uuid)

        check_email.check(repository=self.user_repository, email=user.email)

        self.user_repository.save(user)
        self.event_bus.publish(user.pull_domain_events())
