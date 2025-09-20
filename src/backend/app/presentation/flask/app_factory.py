from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS
from flask_openapi3 import OpenAPI

from app.containers import Container
from app.presentation.flask.resources.login import login_blueprint
from app.presentation.flask.resources.register import register_blueprint
from app.presentation.flask.resources.todos import todo_blueprint
from app.presentation.flask.resources.todos_listing import (
    todos_listing_blueprint,
)
from app.presentation.flask.resources.user_listing import (
    users_listing_blueprint,
)
from app.presentation.flask.resources.users import user_blueprint
from app.settings import CorsSettings


def app_factory() -> WsgiToAsgi:
    app = OpenAPI(__name__, doc_prefix="/docs")
    app.container = Container()  # type:ignore[reportAttributeAccessIssue]

    add_cors_policy(app)
    add_routers(app)

    app.route("/")(lambda: "Up and running")

    return WsgiToAsgi(app)


def add_cors_policy(app: Flask) -> None:
    settings = CorsSettings()  # type:ignore[reportCallIssue]
    CORS(
        app,
        origins=settings.origins,
        supports_credentials=settings.supports_credentials,
        methods=settings.methods,
        allow_headers=settings.allow_headers,
    )


def add_routers(app: OpenAPI) -> None:
    app.register_api(login_blueprint)
    app.register_api(register_blueprint)
    app.register_api(todos_listing_blueprint)
    app.register_api(users_listing_blueprint)
    app.register_api(todo_blueprint)
    app.register_api(user_blueprint)
