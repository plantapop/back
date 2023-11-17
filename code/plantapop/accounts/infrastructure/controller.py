from fastapi import APIRouter
from fastapi.responses import JSONResponse

from plantapop.accounts.application.command.create_user import CreateUserCommand
from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.accounts.infrastructure.dto import registration

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/registration/")
def registration(body: registration.RegistrationDto):
    command = CreateUserCommand()
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

    return JSONResponse(
        {
            "token": {"access": {}, "refresh": {}},
            "registration": {
                "uuid": body.uuid,
                "name": body.name,
                "surnames": body.surnames,
                "email": body.email,
                "prefered_language": body.prefered_language,
                "timezone": body.timezone,
            },
        },
        status_code=201,
    )
