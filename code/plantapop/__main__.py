import os
import uvicorn

HOST = "0.0.0.0"
PORT = 8000
RELOAD = True
WORKERS = 1

if os.getenv("ENVIRONMENT", "") == "production":
    RELOAD = False
    WORKERS = int(os.getenv("WORKERS", "2"))


def main():
    uvicorn.run(
        "plantapop:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        workers=WORKERS)


if __name__ == "__main__":
    main()
