import dotenv
from app.containers import Container
from app.resources.register import Register
from app.resources.todos import Todos
from app.resources.todos_listing import TodoListing
from app.resources.user_listing import UserListing
from app.resources.users import Users
from app.utils import json_utils
from flask import Flask, make_response
from flask_cors import CORS
from flask_restful import Api

dotenv.load_dotenv()


def app_factory() -> Flask:
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])

    @app.route("/")
    def status():
        return "<h1>Up and running</h1>"

    container = Container()
    app.container = container

    api = Api(app)

    @api.representation("application/json")
    def output_json(data, code, headers=None):
        resp = make_response(json_utils.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    api.add_resource(Users, "/user")

    api.add_resource(UserListing, "/users")

    api.add_resource(Todos, "/todo")

    api.add_resource(TodoListing, "/todos")

    api.add_resource(Register, "/register")

    return app


app = app_factory()
