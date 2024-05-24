from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

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
    app = Flask(__name__)
    app.container = Container()  # type:ignore[reportAttributeAccessIssue]

    add_cors_policy(app)
    add_instrumentation(app)
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


def add_instrumentation(app: Flask) -> None:
    PrometheusMetrics(app)


def add_routers(app: Flask) -> None:
    app.register_blueprint(login_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(todos_listing_blueprint)
    app.register_blueprint(users_listing_blueprint)
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(user_blueprint)
