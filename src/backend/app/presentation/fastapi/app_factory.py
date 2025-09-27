import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.containers import Container
from app.presentation.fastapi.resources.login import login_router
from app.presentation.fastapi.resources.register import register_router
from app.presentation.fastapi.resources.todos import todo_router
from app.presentation.fastapi.resources.todos_listing import (
    todo_listing_router,
)
from app.presentation.fastapi.resources.user_listing import user_listing_router
from app.presentation.fastapi.resources.users import users_router
from app.settings import CorsSettings

logger = logging.getLogger(__name__)


def app_factory() -> FastAPI:
    fastapi = FastAPI()
    fastapi.container = Container()  # type:ignore [reportAttributeAccessIssue]

    add_cors_policy(fastapi)
    add_routers(fastapi)

    fastapi.get("/")(lambda: "Up and running")
    return fastapi


def add_cors_policy(app: FastAPI) -> None:
    logger.debug("Adding CORS middleware")
    settings = CorsSettings()  # type:ignore[reportCallIssue]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=settings.supports_credentials,
        allow_methods=settings.methods,
        allow_headers=settings.allow_headers,
    )


def add_routers(app: FastAPI) -> None:
    logger.debug("Adding routers")
    app.include_router(register_router)
    app.include_router(users_router)
    app.include_router(user_listing_router)
    app.include_router(todo_router)
    app.include_router(todo_listing_router)
    app.include_router(login_router)
