from test.accounts.infrastructure.in_memory_event_bus import InMemoryEventBus
from test.accounts.infrastructure.in_memory_repository import InMemoryRepository

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from plantapop.accounts.application.command.create_user import CreateUserCommandHandler
from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.accounts.infrastructure.dto import registration
from plantapop.shared.application.token.create_tokens import CreateToken

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/registration/")
def registration(body: registration.RegistrationDto):
    command = CreateUserCommandHandler(
        user_repository=InMemoryRepository(), event_bus=InMemoryEventBus()
    )
    try:
        command.execute(body)
    except (EmailAlreadyExistsException, UserAlreadyExistsException) as e:
        if isinstance(e, EmailAlreadyExistsException):
            return JSONResponse(
                {"data": {"Error": "EMAIL_ALREADY_EXISTS"}}, status_code=409
            )
        if isinstance(e, UserAlreadyExistsException):
            return JSONResponse(
                {"data": {"Error": "USER_ALREADY_EXISTS"}}, status_code=409
            )

    token_creator = CreateToken()
    token = token_creator.execute(body.uuid, "web")

    return JSONResponse(
        {
            "token": token,
            "registration": {
                "uuid": str(body.uuid),
                "name": body.name,
                "surnames": body.surnames,
                "email": body.email,
                "prefered_language": body.prefered_language,
                "timezone": body.timezone,
            },
        },
        status_code=201,
    )
