import uvicorn

from plantapop.config import Config
from plantapop.shared.infrastructure.controller.app import create_app
from plantapop.shared.infrastructure.repository.models import init_models

configmap = Config.get_instance()
app = create_app()


@app.on_event("startup")
async def startup():
    await init_models()


def main():
    uvicorn.run(
        "plantapop.__main__:app",
        host=configmap.fastapi.deploy.host,
        port=configmap.fastapi.deploy.port,
        reload=configmap.fastapi.deploy.reload,
        workers=configmap.fastapi.deploy.workers,
    )


if __name__ == "__main__":
    main()
