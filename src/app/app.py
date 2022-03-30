import json
from app.resources.todos import Todos
from app.resources.user_listing import UserListing
from app.resources.users import Users
from flask import Flask, make_response
from flask_restful import Api
import dotenv

from app.utils.enhanced_json_encoder import EnhancedJSONEncoder

dotenv.load_dotenv()

app = Flask(__name__)
api = Api(app)


@api.representation("application/json")
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, cls=EnhancedJSONEncoder), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(Users, "/user")

api.add_resource(Todos, "/todos")

api.add_resource(UserListing, "/users")
