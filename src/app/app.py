from app.resources.todos import Todos
from app.resources.users import Users
from flask import Flask
from flask_restful import Api
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, "/users")

api.add_resource(Todos, "/todos")
