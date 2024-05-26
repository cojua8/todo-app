from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.list_response import ListOf
from app.presentation.models.user import User as ApiUser

users_listing_blueprint = APIBlueprint("users", __name__)


@users_listing_blueprint.get(
    "/users", responses={HTTPStatus.OK: ListOf[ApiUser]}
)
@inject
async def get(
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    users = await user_service.get_all()

    return PydanticModelResponse(
        content=users, content_model=list[ApiUser], status_code=HTTPStatus.OK
    )
