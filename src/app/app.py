import json

import dotenv
from flask import Flask, make_response
from flask_cors import CORS
from flask_restful import Api

from app.containers import Container
from app.resources.todos import Todos
from app.resources.todos_listing import TodoListing
from app.resources.user_listing import UserListing
from app.resources.users import Users
from app.utils.enhanced_json_encoder import EnhancedJSONEncoder

dotenv.load_dotenv()


def app_factory() -> Flask:
    container = Container()

    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])
    app.container = container
    api = Api(app)

    @api.representation("application/json")
    def output_json(data, code, headers=None):
        resp = make_response(json.dumps(data, cls=EnhancedJSONEncoder), code)
        resp.headers.extend(headers or {})
        return resp

    api.add_resource(Users, "/user")

    api.add_resource(UserListing, "/users")

    api.add_resource(Todos, "/todo")

    api.add_resource(TodoListing, "/todos")
    return app


app = app_factory()
