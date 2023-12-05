import datetime as dt
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Response

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
    response: Response,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Todo | None:
    todo = await todo_service.get(id_)

    if not todo:
        response.status_code = HTTPStatus.NOT_FOUND

    return todo


@todo_router.post("/todo")
@inject
async def post(
    owner_id: Annotated[UUID, Body(alias="ownerId")],
    description: Annotated[str, Body()],
    due_date: Annotated[dt.date, Body(alias="dueDate")],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Todo:
    new_todo = Todo(
        owner_id=owner_id, description=description, due_date=due_date
    )
    return await todo_service.create(new_todo)


@todo_router.delete("/todo/{id_}", status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete(
    id_: UUID,
    response: Response,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> None:
    result = await todo_service.delete(id_)

    if not result:
        response.status_code = HTTPStatus.NOT_FOUND


@todo_router.put("/todo/{id_}")
@inject
async def put(  # noqa: PLR0913
    id_: UUID,
    owner_id: Annotated[UUID, Body(alias="ownerId")],
    description: Annotated[str, Body()],
    date_created: Annotated[dt.date, Body(alias="dateCreated")],
    due_date: Annotated[dt.date, Body(alias="dueDate")],
    completed: Annotated[bool, Body()],
    response: Response,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Todo | None:
    new = Todo(
        id=id_,
        owner_id=owner_id,
        description=description,
        date_created=date_created,
        due_date=due_date,
        completed=completed,
    )

    todo = await todo_service.put(id_, new)
    if not todo:
        response.status_code = HTTPStatus.NOT_FOUND

    return todo
