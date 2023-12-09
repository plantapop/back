from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from plantapop.shared.domain.token.exceptions import InvalidTokenException


class InvalidTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except InvalidTokenException:
            return JSONResponse({"data": {"Error": "INVALID_TOKEN"}}, status_code=401)
