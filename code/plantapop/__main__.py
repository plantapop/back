import uvicorn

from plantapop import CONFIGMAP


def main():
    uvicorn.run(
        "plantapop:app",
        host=CONFIGMAP.HOST,
        port=CONFIGMAP.PORT,
        reload=CONFIGMAP.RELOAD,
        workers=CONFIGMAP.WORKERS,
    )


if __name__ == "__main__":
    main()
