from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.path_id import PathId
from app.presentation.models.user import User as ApiUser
from app.presentation.models.user_create_data import UserCreateData
from app.presentation.models.user_not_found_error import UserNotFoundError
from app.presentation.models.user_update_data import UserUpdateData

user_blueprint = APIBlueprint("user", __name__)


@user_blueprint.get(
    "/user/<uuid:id_>",
    responses={
        HTTPStatus.OK: ApiUser,
        HTTPStatus.NOT_FOUND: UserNotFoundError,
    },
)
@inject
async def get(
    path: PathId,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> PydanticModelResponse:
    user = await user_service.get(path.id)

    if not user:
        return PydanticModelResponse(
            content=UserNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )

    return PydanticModelResponse(
        content=user, content_model=ApiUser, status_code=HTTPStatus.OK
    )


@user_blueprint.post("/user", responses={HTTPStatus.CREATED: ApiUser})
@inject
async def post(
    body: UserCreateData,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> PydanticModelResponse:
    new_user = User(
        username=body.username, email=body.email, password=body.password
    )
    user = await user_service.create(new_user)

    return PydanticModelResponse(
        content=user, content_model=ApiUser, status_code=HTTPStatus.CREATED
    )


@user_blueprint.delete(
    "/user/<uuid:id_>",
    responses={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: UserNotFoundError,
    },
)
@inject
async def delete(
    path: PathId,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    result = await user_service.delete(path.id)

    if not result:
        return PydanticModelResponse(
            content=UserNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )


@user_blueprint.put(
    "/user/<uuid:id_>",
    responses={
        HTTPStatus.OK: ApiUser,
        HTTPStatus.NOT_FOUND: UserNotFoundError,
    },
)
@inject
async def put(
    path: PathId,
    body: UserUpdateData,
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> Any:  # noqa: ANN401
    new = User(
        id=path.id,
        username=body.username,
        email=body.email,
        password=body.password,
    )
    user = await user_service.put(path.id, new)

    if not user:
        return PydanticModelResponse(
            content=UserNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )

    return PydanticModelResponse(
        content=user, content_model=ApiUser, status_code=HTTPStatus.OK
    )
