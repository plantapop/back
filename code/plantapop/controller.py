from fastapi import FastAPI, Response


async def health_check() -> Response:
    return Response(status_code=200)


class Controller:
    def __init__(self, app: FastAPI):
        self.app = app

    def register(self):
        self._chat()
        self._discovery()
        self._geolocation()
        self._labeling()
        self._plantory()
        self.app.add_api_route("/health_check", health_check, methods=["GET"])

    def _chat(self):
        pass

    def _discovery(self):
        pass

    def _geolocation(self):
        pass

    def _labeling(self):
        pass

    def _plantory(self):
        pass
