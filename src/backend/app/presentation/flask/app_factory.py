from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics


def app_factory() -> WsgiToAsgi:
    app = Flask(__name__)
    add_cors_policy(app)
    add_instrumentation(app)
    add_routers(app)

    app.route("/")(lambda: "Up and running")

    return WsgiToAsgi(app)


def add_cors_policy(_: Flask) -> None: ...
def add_instrumentation(app: Flask) -> None:
    PrometheusMetrics(app)


def add_routers(_: Flask) -> None: ...
