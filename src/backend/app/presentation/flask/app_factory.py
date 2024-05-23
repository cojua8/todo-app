from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from app.settings import CorsSettings


def app_factory() -> WsgiToAsgi:
    app = Flask(__name__)
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


def add_routers(_: Flask) -> None: ...
