from http import HTTPStatus
from typing import Any

from flask_restful import Resource

from app.models.user import User
from app.services.base_database_service.base_database_service import \
    IDatabaseService


class UserListing(Resource):
    def __init__(self, db_service: IDatabaseService[User]) -> None:
        super().__init__()
        self.user_db_service = db_service
        self.T = User

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
