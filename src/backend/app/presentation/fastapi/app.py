from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app as prometheus_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from app.containers import Container
from app.presentation.fastapi.resources.login import login_router
from app.presentation.fastapi.resources.register import register_router
from app.presentation.fastapi.resources.todos import todo_router
from app.presentation.fastapi.resources.todos_listing import (
    todo_listing_router,
)
from app.presentation.fastapi.resources.user_listing import user_listing_router
from app.presentation.fastapi.resources.users import users_router


def app_factory() -> FastAPI:
    fastapi = FastAPI()
    fastapi.container = Container()  # type: ignore[container]

    add_cors_policy(fastapi)
    add_instrumentation(fastapi)
    add_routers(fastapi)

    fastapi.get("/")(lambda: "Up and running")
    return fastapi


def add_cors_policy(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_instrumentation(app: FastAPI) -> None:
    instrumentator = Instrumentator().instrument(app)

    @app.on_event("startup")
    async def _startup() -> None:
        instrumentator.expose(app)

    app.mount("/metrics", prometheus_asgi_app())


def add_routers(app: FastAPI) -> None:
    app.include_router(register_router)
    app.include_router(users_router)
    app.include_router(user_listing_router)
    app.include_router(todo_router)
    app.include_router(todo_listing_router)
    app.include_router(login_router)
