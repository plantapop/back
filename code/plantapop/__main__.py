import uvicorn
from plantapop import configmap


def main():
    uvicorn.run(
        "plantapop:app",
        host=configmap.HOST,
        port=configmap.PORT,
        reload=configmap.RELOAD,
        workers=configmap.WORKERS,
    )


if __name__ == "__main__":
    main()
