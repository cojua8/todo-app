from http import HTTPStatus
import os
from typing import Any
from flask_restful import Resource

from app.models.user import User
from app.services.base_database_service.base_database_service import (
    IDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)


class UserListing(Resource):
    T = User
    user_db_service: IDatabaseService[User] = UsersJsonDatabaseService(
        os.environ["DATABASE_PATH"]
    )

    def get(self):
        response: dict[str, Any] = {}
        try:
            users = self.user_db_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response
