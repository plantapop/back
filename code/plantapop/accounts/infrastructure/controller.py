from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from plantapop.accounts.application.command.create_user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from plantapop.accounts.application.command.delete_user import (
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from plantapop.accounts.application.query.login_user import (
    LogInUserQuery,
    LogInUserQueryHandler,
)
from plantapop.accounts.domain.exceptions import (
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from plantapop.shared.application.token.create_tokens import CreateToken
from plantapop.shared.application.token.refresh_token import RefreshToken
from plantapop.shared.application.token.revoke import Revoke
from plantapop.shared.infrastructure.controller.security import get_user

router = APIRouter(prefix="/user", tags=["user"])


class CreateUserSchema(CreateUserCommand):
    pass


@router.post("/signup")
async def registration(body: CreateUserSchema):
    command = CreateUserCommandHandler()
    try:
        await command.execute(body)
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
    token = await token_creator.execute(body.uuid, body.device)

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


class LogInSchema(LogInUserQuery):
    pass


@router.post("/login")
async def login(body: LogInSchema):
    query = LogInUserQueryHandler()
    response = await query.execute(body)

    if response is None:
        return JSONResponse({"data": {"Error": "INVALID_CREDENTIALS"}}, status_code=401)

    return JSONResponse(
        {"token": {"access": response.access_token, "refresh": response.refresh_token}},
        status_code=200,
    )


class LogoutSchema(BaseModel):
    device: str


@router.post("/logout")  # Validate the option of a revoked access tokens redis store
async def logout(schema: LogoutSchema, uuid: str = Depends(get_user)):
    revoke = Revoke()
    await revoke.execute(user_uuid=uuid, device=schema.device)

    return JSONResponse(status_code=204, content="")


class RefreshSchema(BaseModel):
    token: str


@router.post("/refresh")
async def refresh(schema: RefreshSchema):
    refresh = RefreshToken()
    response = await refresh.execute(schema.token)

    return JSONResponse(
        {"token": {"access": response["access"], "refresh": response["refresh"]}},
        status_code=200,
    )


class DeleteSchema(BaseModel):
    password: str


@router.post("/delete")
async def delete(schema: DeleteSchema, uuid: str = Depends(get_user)):
    delete = DeleteUserCommandHandler()
    revoke = Revoke()

    await revoke.execute(user_uuid=uuid, rall=True)
    await delete.execute(DeleteUserCommand(uuid=uuid, password=schema.password))

    return JSONResponse(status_code=204, content="")
