from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

base_router = APIRouter()


@base_router.get("/readiness")
@inject
async def readiness(session: Session = Depends(Provide["session"])) -> JSONResponse:
    assert isinstance(session, Session)
    try:
        session.execute(text("SELECT 1"))
        response_data = {"status": "OK"}
        status_code = 200
    except Exception as e:
        response_data = {"status": "Error", "error": str(e)}
        status_code = 500

    return JSONResponse(content=response_data, status_code=status_code)


class FastApiEndpoints:
    def __init__(self, app: FastAPI):
        self.app = app

    def register(self):
        for router in ROUTES:
            self.app.include_router(router)
        return self.app


ROUTES = [
    base_router,
]
