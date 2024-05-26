from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.list_response import ListOf
from app.presentation.models.todo import Todo as ApiTodo
from app.presentation.models.todos_query import TodosQuery

todos_listing_blueprint = APIBlueprint("todos", __name__)


@todos_listing_blueprint.get(
    "/todos", responses={HTTPStatus.OK: ListOf[ApiTodo]}
)
@inject
async def get(
    query: TodosQuery,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> Any:  # noqa: ANN401
    todos = await todo_service.get_all_by_user_id(query.user_id)

    return PydanticModelResponse(
        content=todos, content_model=list[ApiTodo], status_code=HTTPStatus.OK
    )
