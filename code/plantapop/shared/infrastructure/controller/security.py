from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel

from plantapop.shared.application.token.validate_tokens import ValidateToken

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token")


class LogOutCommand(BaseModel):
    uuid: UUID
    device: str


async def get_user(token: str = Depends(oauth2_scheme)) -> UUID:
    validator = ValidateToken()
    return await validator.execute(token)
