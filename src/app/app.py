import json
import os

import dotenv
from flask import Flask, make_response
from flask_restful import Api

from app.resources.todos import Todos
from app.resources.user_listing import UserListing
from app.resources.users import Users
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)
from app.utils.enhanced_json_encoder import EnhancedJSONEncoder

dotenv.load_dotenv()

app = Flask(__name__)
api = Api(app)


@api.representation("application/json")
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, cls=EnhancedJSONEncoder), code)
    resp.headers.extend(headers or {})
    return resp


users_database = UsersJsonDatabaseService(os.environ["DATABASE_PATH"])
todos_database = TodosJsonDatabaseService(os.environ["DATABASE_PATH"])


api.add_resource(
    Users, "/user", resource_class_kwargs={"db_service": users_database}
)

api.add_resource(
    Todos, "/todos", resource_class_kwargs={"db_service": todos_database}
)

api.add_resource(
    UserListing, "/users", resource_class_kwargs={"db_service": users_database}
)
