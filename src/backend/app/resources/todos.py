import datetime as dt
from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body

from app.containers import Container
from app.models.todo import Todo
from app.services.service_protocols.todo_service_protocol import (
    TodoServiceProtocol,
)

todo_router = APIRouter()


@todo_router.get("/todo/{id_}")
@inject
async def get(
    id_: UUID,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        todo = await todo_service.get(id_)

        response["status"] = HTTPStatus.OK
        response["response"] = todo
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_router.post("/todo")
@inject
async def post(
    owner_id: Annotated[UUID, Body(alias="ownerId")],
    description: Annotated[str, Body()],
    due_date: Annotated[dt.date, Body(alias="dueDate")],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    new = Todo(owner_id=owner_id, description=description, due_date=due_date)

    try:
        await todo_service.create(new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_router.delete("/todo/{id_}")
@inject
async def delete(
    id_: UUID,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        await todo_service.delete(id_)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_router.put("/todo/{id_}")
@inject
async def put(  # noqa: PLR0913
    id_: UUID,
    owner_id: Annotated[UUID, Body(alias="ownerId")],
    description: Annotated[str, Body()],
    date_created: Annotated[dt.date, Body(alias="dateCreated")],
    due_date: Annotated[dt.date, Body(alias="dueDate")],
    completed: Annotated[bool, Body()],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    new = Todo(
        id=id_,
        owner_id=owner_id,
        description=description,
        date_created=date_created,
        due_date=due_date,
        completed=completed,
    )
    try:
        await todo_service.put(id_, new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response
