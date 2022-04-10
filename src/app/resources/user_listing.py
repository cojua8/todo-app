from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource

from app.containers import Container
from app.models.user import User
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class UserListing(Resource):
    @inject
    def __init__(
        self,
        db_service: DatabaseServiceProtocol[User] = (
            Provide[Container.users_database]
        ),
    ) -> None:
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
