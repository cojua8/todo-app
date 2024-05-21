from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Response
from pydantic import EmailStr

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.user_service_protocol import UserServiceProtocol

users_router = APIRouter()


@users_router.get("/user/{id_}")
@inject
async def get(
    id_: UUID,
    response: Response,
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> User | None:
    user = await user_service.get(id_)

    if not user:
        response.status_code = HTTPStatus.NOT_FOUND
        return None

    return user


@users_router.post("/user", status_code=HTTPStatus.CREATED)
@inject
async def post(
    username: Annotated[str, Body()],
    email: Annotated[EmailStr, Body()],
    password: Annotated[str, Body()],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> User:
    new_user = User(username=username, email=email, password=password)
    return await user_service.create(new_user)


@users_router.delete("/user/{id_}", status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete(
    id_: UUID,
    response: Response,
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> None:
    result = await user_service.delete(id_)

    if not result:
        response.status_code = HTTPStatus.NOT_FOUND


@users_router.put("/user/{id_}")
@inject
async def put(  # noqa: PLR0913
    id_: UUID,
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    password: Annotated[str, Body()],
    response: Response,
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> User | None:
    new = User(id=id_, username=username, email=email, password=password)
    user = await user_service.put(id_, new)

    if not user:
        response.status_code = HTTPStatus.BAD_REQUEST

    return user
