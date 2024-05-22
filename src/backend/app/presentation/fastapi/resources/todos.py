from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body

from app.containers import Container
from app.domain.models.todo import Todo
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.fastapi.exceptions.todo_not_found_error import (
    TodoNotFoundError,
)
from app.presentation.fastapi.models.todo import Todo as ApiTodo
from app.presentation.fastapi.models.todo_create_data import TodoCreateData
from app.presentation.fastapi.models.todo_update_data import TodoUpdateData

todo_router = APIRouter()


@todo_router.get("/todo/{id_}", response_model=ApiTodo)
@inject
async def get(
    id_: UUID,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Any:  # noqa: ANN401
    todo = await todo_service.get(id_)

    if not todo:
        raise TodoNotFoundError

    return todo


@todo_router.post(
    "/todo", status_code=HTTPStatus.CREATED, response_model=ApiTodo
)
@inject
async def post(
    todo_create_data: Annotated[TodoCreateData, Body()],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Any:  # noqa: ANN401
    new_todo = Todo(
        owner_id=todo_create_data.owner_id,
        description=todo_create_data.description,
        due_date=todo_create_data.due_date,
    )
    return await todo_service.create(new_todo)


@todo_router.delete("/todo/{id_}", status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete(
    id_: UUID,
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> None:
    result = await todo_service.delete(id_)

    if not result:
        raise TodoNotFoundError


@todo_router.put("/todo/{id_}", response_model=ApiTodo)
@inject
async def put(
    id_: UUID,
    todo_update_data: Annotated[TodoUpdateData, Body()],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Any:  # noqa: ANN401
    new = Todo(
        id=id_,
        owner_id=todo_update_data.owner_id,
        description=todo_update_data.description,
        date_created=todo_update_data.date_created,
        due_date=todo_update_data.due_date,
        completed=todo_update_data.completed,
    )

    todo = await todo_service.put(id_, new)
    if not todo:
        raise TodoNotFoundError

    return todo
