from resources.todos import Todos
from resources.users import Users
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

api.add_resource(Users, "/users")

api.add_resource(Todos, "/todos")

if __name__ == "__main__":
    app.run(debug=True)
