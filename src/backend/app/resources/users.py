from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body
from pydantic import EmailStr

from app.containers import Container
from app.models.user import User
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)

users_router = APIRouter()


@users_router.get("/user")
@inject
async def get(
    id_: Annotated[UUID, Body(embed=True, alias="id")],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        user = await user_service.get(id_)

        response["status"] = HTTPStatus.OK
        response["response"] = user
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_router.post("/user")
@inject
async def post(
    username: Annotated[str, Body()],
    email: Annotated[EmailStr, Body()],
    password: Annotated[str, Body()],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    user = User(username=username, email=email, password=password)
    try:
        await user_service.create(user)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_router.delete("/user")
@inject
async def delete(
    id_: Annotated[UUID, Body(embed=True, alias="id")],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        await user_service.delete(id_)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_router.put("/user")
@inject
async def put(
    id_: Annotated[UUID, Body(alias="id")],
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    password: Annotated[str, Body()],
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    new = User(id=id_, username=username, email=email, password=password)
    try:
        await user_service.put(id_, new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response
