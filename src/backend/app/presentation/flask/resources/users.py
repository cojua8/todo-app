from http import HTTPStatus
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse, get_body
from app.presentation.models.user import User as ApiUser
from app.presentation.models.user_create_data import UserCreateData
from app.presentation.models.user_not_found_error import UserNotFoundError
from app.presentation.models.user_update_data import UserUpdateData

user_blueprint = Blueprint("user", __name__)


@user_blueprint.get("/user/<uuid:id_>")
@inject
async def get(
    id_: UUID,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> PydanticModelResponse:
    user = await user_service.get(id_)

    if not user:
        return PydanticModelResponse(
            status_code=HTTPStatus.NOT_FOUND, content_model=UserNotFoundError()
        )

    return PydanticModelResponse(
        content_model=ApiUser.model_validate(user, from_attributes=True),
        status_code=HTTPStatus.OK,
    )


@user_blueprint.post("/user")
@inject
async def post(
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> PydanticModelResponse:
    user_create_data = get_body(UserCreateData)
    new_user = User(
        username=user_create_data.username,
        email=user_create_data.email,
        password=user_create_data.password,
    )
    user = await user_service.create(new_user)

    return PydanticModelResponse(
        content_model=ApiUser.model_validate(user, from_attributes=True),
        status_code=HTTPStatus.CREATED,
    )


@user_blueprint.delete("/user/<uuid:id_>")
@inject
async def delete(
    id_: UUID,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    result = await user_service.delete(id_)

    if not result:
        return PydanticModelResponse(
            status_code=HTTPStatus.NOT_FOUND, content_model=UserNotFoundError()
        )


@user_blueprint.put("/user/<uuid:id_>")
@inject
async def put(
    id_: UUID,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    user_update_data = get_body(UserUpdateData)
    new = User(
        id=id_,
        username=user_update_data.username,
        email=user_update_data.email,
        password=user_update_data.password,
    )
    user = await user_service.put(id_, new)

    if not user:
        return PydanticModelResponse(
            status_code=HTTPStatus.NOT_FOUND, content_model=UserNotFoundError()
        )

    return PydanticModelResponse(
        content_model=ApiUser.model_validate(user, from_attributes=True),
        status_code=HTTPStatus.OK,
    )
