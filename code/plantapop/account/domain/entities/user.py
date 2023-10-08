import datetime
from uuid import UUID, uuid4

from jose import jwt

from plantapop import CONFIGMAP
from plantapop.account.domain.events.created_user_event import CreatedUserEvent
from plantapop.account.domain.events.deleted_user_event import DeletedUserEvent
from plantapop.account.domain.events.updated_password_event import UpdatedPasswordEvent
from plantapop.account.domain.vos.email import Email
from plantapop.account.domain.vos.password import Password
from plantapop.account.domain.vos.username import Username
from plantapop.shared_kernel.auth.jwt_validator import JWTValidator  # TODO: This dependency should be removed


class User:
    def __init__(
        self,
        user_uuid: UUID,
        email: str,
        password: str,
        username: str,
        surnames: str,
        email_validated: bool = False,
        active: bool = True,
    ):
        self.user_uuid = user_uuid
        self.email = Email(value=email)
        self.password = Password.make(password)
        self.name = Username(value=username)
        self.surnames = surnames
        self.email_validated = email_validated
        self.is_active = active

        self.events = []

    @staticmethod
    def create(email: str, password: str, username: str, surnames: str) -> "User":
        user = User(
            user_uuid=uuid4(),
            email=email,
            password=password,
            username=username,
            surnames=surnames,
        )
        user.events.append(CreatedUserEvent(user.user_uuid, user.email, user.name))

        return user

    def get_token(self) -> tuple[str, str]:
        access = jwt.encode(
            {
                "user_uuid": self.user_uuid,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(seconds=CONFIGMAP.JWT.TTL),
            },
            CONFIGMAP.JWT.SECRET,
            algorithm=CONFIGMAP.JWT.ALGORITHM,
        )

        refresh = jwt.encode(
            {
                "user_uuid": self.user_uuid,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(seconds=CONFIGMAP.JWT.REFRESH_TTL),
            },
            CONFIGMAP.JWT.SECRET,
            algorithm=CONFIGMAP.JWT.ALGORITHM,
        )
        return access, refresh

    def refresh_token(self, ref_token: str) -> tuple[str, str]:
        if not self.is_active:
            raise Exception("User is not active")  # TODO: Create custom exception

        JWTValidator.validate(ref_token)
        return self.get_token()

    def update_password(self, password: str) -> None:
        self.password = Password.make(password)
        self.events.append(UpdatedPasswordEvent(self.user_uuid, self.email))

    def validate_email(self) -> None:
        self.email_validated = True

    def delete(self) -> None:
        self.events.append(DeletedUserEvent(self.user_uuid))
