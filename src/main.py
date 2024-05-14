import uvicorn
from fastapi import FastAPI

from src.config import APP_HOST, APP_PORT

from .app.routes import router

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT)
