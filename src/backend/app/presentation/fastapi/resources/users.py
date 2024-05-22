from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.fastapi.exceptions.user_not_found_error import (
    UserNotFoundError,
)
from app.presentation.fastapi.models.user import User as ApiUser
from app.presentation.fastapi.models.user_create_data import UserCreateData
from app.presentation.fastapi.models.user_update_data import UserUpdateData

users_router = APIRouter()


@users_router.get("/user/{id_}", response_model=ApiUser)
@inject
async def get(
    id_: UUID,
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> Any:  # noqa: ANN401
    user = await user_service.get(id_)

    if not user:
        raise UserNotFoundError

    return user


@users_router.post(
    "/user", status_code=HTTPStatus.CREATED, response_model=ApiUser
)
@inject
async def post(
    user_create_data: Annotated[UserCreateData, Body()],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> Any:  # noqa: ANN401
    new_user = User(
        username=user_create_data.username,
        email=user_create_data.email,
        password=user_create_data.password,
    )
    return await user_service.create(new_user)


@users_router.delete("/user/{id_}", status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete(
    id_: UUID,
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> None:
    result = await user_service.delete(id_)

    if not result:
        raise UserNotFoundError


@users_router.put("/user/{id_}", response_model=ApiUser)
@inject
async def put(
    id_: UUID,
    user_update_data: Annotated[UserUpdateData, Body()],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> Any:  # noqa: ANN401
    new = User(
        id=id_,
        username=user_update_data.username,
        email=user_update_data.email,
        password=user_update_data.password,
    )
    user = await user_service.put(id_, new)

    if not user:
        raise UserNotFoundError

    return user
