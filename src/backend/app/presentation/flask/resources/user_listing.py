from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.flask.utils import PydanticListModelResponse
from app.presentation.models.user import User as ApiUser

users_listing_blueprint = Blueprint("users", __name__)


@users_listing_blueprint.get("/users")
@inject
async def get(
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    users = await user_service.get_all()

    return PydanticListModelResponse(
        item_type=ApiUser, items=users, status_code=HTTPStatus.OK
    )
