from fastapi.openapi.models import Response

from plantapop.account.application.command.signup import SignUp
from plantapop.account.application.command.update_password import (
    ForgotPassword,
    ResetPassword,
)
from plantapop.account.application.query.availability import AvailableEmail
from plantapop.account.application.query.login import Login
from plantapop.account.application.query.refresh import Refresh


async def signup(username: str, email: str, password: str) -> Response:
    access, refresh = SignUp().execute(
        username=username, email=email, password=password
    )
    return Response(status_code=200, content={"access": access, "refresh": refresh})


async def login(email: str, password: str) -> Response:
    access, refresh = Login().execute(email=email, password=password)
    return Response(status_code=200, content={"access": access, "refresh": refresh})


async def forgot_password(email: str) -> Response:
    ForgotPassword().execute(email=email)
    return Response(status_code=200)


async def reset_password(token: str, password: str) -> Response:
    ResetPassword().execute(token=token, password=password)
    return Response(status_code=200)


async def refresh_token(token: str) -> Response:
    access, refresh = Refresh().execute(refresh_token=token)
    return Response(status_code=200, content={"access": access, "refresh": refresh})


async def available_email(email: str) -> Response:
    available = AvailableEmail().execute(email=email)
    return Response(status_code=200, content={"available": available})
