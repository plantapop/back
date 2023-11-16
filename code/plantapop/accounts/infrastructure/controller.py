from fastapi import APIRouter
from fastapi.responses import JSONResponse

from plantapop.accounts.infrastructure.dto import registration

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/registration/")
def registration(body: registration.RegistrationDto):
    return JSONResponse(
        {"token": {"access": {}, "refresh": {}}, "registration": body.dict()},
        status_code=201,
    )
