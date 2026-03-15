from contextlib import asynccontextmanager
from logging import Logger, getLogger

import uvicorn
from fastapi import FastAPI

import app.config.logging_config
from app.config import server_settings
from app.exceptions.exception_handler import register_exception_handlers
from app.repository import database, repository
from app.routers import candle_router

log: Logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_database()
    repository.create_table_if_not_exists()

    # Whatever written above acts like a @PostConstruct for the entire app
    yield

    # Whatever written here acts like a shutdown hook
    log.info("Shutting down. Miss you :(")


app: FastAPI = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

# LEARN: we must manually register routers
app.include_router(candle_router, tags=["candle"])

if __name__ == '__main__':
    # I don't know why I have to run through hoops like this. Spring Boot has this by default.
    # Maybe I am missing something?
    uvicorn.run(
        app="app.main:app",
        port=server_settings.port
    )
