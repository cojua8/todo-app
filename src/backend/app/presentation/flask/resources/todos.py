from http import HTTPStatus
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container
from app.domain.models.todo import Todo
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse, get_body
from app.presentation.models.todo import Todo as ApiTodo
from app.presentation.models.todo_create_data import TodoCreateData
from app.presentation.models.todo_not_found_error import TodoNotFoundError
from app.presentation.models.todo_update_data import TodoUpdateData

todo_blueprint = Blueprint("todo", __name__)


@todo_blueprint.get("/todo/<uuid:id_>")
@inject
async def get(
    id_: UUID,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    todo = await todo_service.get(id_)

    if not todo:
        return PydanticModelResponse(
            content_model=TodoNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )

    return PydanticModelResponse(
        content_model=ApiTodo.model_validate(todo, from_attributes=True),
        status_code=HTTPStatus.OK,
    )


@todo_blueprint.post("/todo")
@inject
async def post(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    todo_create_data = get_body(TodoCreateData)
    new_todo = Todo(
        owner_id=todo_create_data.owner_id,
        description=todo_create_data.description,
        due_date=todo_create_data.due_date,
    )
    todo = await todo_service.create(new_todo)

    return PydanticModelResponse(
        content_model=ApiTodo.model_validate(todo, from_attributes=True),
        status_code=HTTPStatus.CREATED,
    )


@todo_blueprint.delete("/todo/<uuid:id_>")
@inject
async def delete(
    id_: UUID,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> Any:  # noqa: ANN401
    result = await todo_service.delete(id_)

    if not result:
        return PydanticModelResponse(
            content_model=TodoNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )


@todo_blueprint.put("/todo/<uuid:id_>")
@inject
async def put(
    id_: UUID,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    todo_update_data = get_body(TodoUpdateData)
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
        return PydanticModelResponse(
            status_code=HTTPStatus.NOT_FOUND, content_model=TodoNotFoundError()
        )

    return PydanticModelResponse(
        content_model=ApiTodo.model_validate(todo, from_attributes=True),
        status_code=HTTPStatus.OK,
    )
