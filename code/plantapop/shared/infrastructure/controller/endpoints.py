import aio_pika
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text

from plantapop.accounts.infrastructure.controller import router as accounts_router

base_router = APIRouter()


@base_router.get("/readiness")
@inject
async def readiness(
    channel_pool=Depends(Provide["channel"]),
    session=Depends(Provide["session"]),
) -> JSONResponse:
    async with channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(("Channel: %r" % channel).encode()),
            "pool_queue",
        )

    async with session.begin():
        await session.execute(text("SELECT 1"))

    return JSONResponse(content={"status": "OK"}, status_code=200)


ROUTES = [base_router, accounts_router]


class FastApiEndpoints:
    def __init__(self, app: FastAPI):
        self.app = app

    def register(self):
        for router in ROUTES:
            self.app.include_router(router)
        return self.app
