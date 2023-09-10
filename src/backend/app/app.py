import dotenv
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask
from flask_cors import CORS

from app.containers import Container
from app.resources.login import login_blueprint
from app.resources.register import register_blueprint
from app.resources.todos import todo_blueprint
from app.resources.todos_listing import todo_listing_blueprint
from app.resources.user_listing import user_listing_blueprint
from app.resources.users import users_blueprint

dotenv.load_dotenv()


def app_factory() -> FastAPI:
    flask_app = Flask(__name__)
    CORS(flask_app, origins=["http://localhost:3000"])

    flask_app.container = Container()  # type: ignore[container]

    @flask_app.route("/")
    def status() -> str:
        return "<h1>Up and running</h1>"

    flask_app.register_blueprint(register_blueprint)
    flask_app.register_blueprint(users_blueprint)
    flask_app.register_blueprint(user_listing_blueprint)
    flask_app.register_blueprint(todo_blueprint)
    flask_app.register_blueprint(todo_listing_blueprint)
    flask_app.register_blueprint(login_blueprint)

    fastapi = FastAPI()

    fastapi.mount("/", WSGIMiddleware(flask_app))

    return fastapi


app = app_factory()
