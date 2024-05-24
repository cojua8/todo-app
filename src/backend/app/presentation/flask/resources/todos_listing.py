from http import HTTPStatus
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request

from app.containers import Container
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.flask.utils import PydanticListModelResponse
from app.presentation.models.todo import Todo as ApiTodo

todos_listing_blueprint = Blueprint("todos", __name__)


@todos_listing_blueprint.get("/todos")
@inject
async def get(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> Any:  # noqa: ANN401
    user_id = UUID(request.args["user_id"])

    todos = await todo_service.get_all_by_user_id(user_id)

    return PydanticListModelResponse(
        item_type=ApiTodo, items=todos, status_code=HTTPStatus.OK
    )
