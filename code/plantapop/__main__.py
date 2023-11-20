import uvicorn

from plantapop import CONFIGMAP, create_app


def main():
    app = create_app()
    uvicorn.run(
        app,
        host=CONFIGMAP.HOST,
        port=CONFIGMAP.PORT,
        reload=CONFIGMAP.RELOAD,
        workers=CONFIGMAP.WORKERS,
    )


if __name__ == "__main__":
    main()
