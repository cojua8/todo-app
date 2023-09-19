import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.containers import Container
from app.resources.login import login_router
from app.resources.register import register_router
from app.resources.todos import todo_router
from app.resources.todos_listing import todo_listing_router
from app.resources.user_listing import user_listing_router
from app.resources.users import users_router

dotenv.load_dotenv()


def app_factory() -> FastAPI:
    fastapi = FastAPI()
    fastapi.add_middleware(
        CORSMiddleware, allow_origins=["http://localhost:3000"]
    )
    fastapi.container = Container()  # type: ignore[container]

    fastapi.get("/")(lambda: "Up and running")

    fastapi.include_router(register_router)
    fastapi.include_router(users_router)
    fastapi.include_router(user_listing_router)
    fastapi.include_router(todo_router)
    fastapi.include_router(todo_listing_router)
    fastapi.include_router(login_router)

    return fastapi


app = app_factory()
