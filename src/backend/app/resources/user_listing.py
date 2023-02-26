from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource

from app.containers import Container

if TYPE_CHECKING:
    from app.services.service_protocols.user_service_protocol import (
        UserServiceProtocol,
    )


class UserListing(Resource):
    @inject
    def __init__(
        self,
        user_service: UserServiceProtocol = (Provide[Container.users_service]),
    ) -> None:
        self.user_service = user_service

    def get(self) -> dict[str, Any]:
        response: dict[str, Any] = {}
        try:
            users = self.user_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response
