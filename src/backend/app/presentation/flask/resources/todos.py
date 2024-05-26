from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.models.todo import Todo
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.path_id import PathId
from app.presentation.models.todo import Todo as ApiTodo
from app.presentation.models.todo_create_data import TodoCreateData
from app.presentation.models.todo_not_found_error import TodoNotFoundError
from app.presentation.models.todo_update_data import TodoUpdateData

todo_blueprint = APIBlueprint("todo", __name__)


@todo_blueprint.get(
    "/todo/<uuid:id_>",
    responses={
        HTTPStatus.OK: ApiTodo,
        HTTPStatus.NOT_FOUND: TodoNotFoundError,
    },
)
@inject
async def get(
    path: PathId,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    todo = await todo_service.get(path.id)

    if not todo:
        return PydanticModelResponse(
            content=TodoNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )

    return PydanticModelResponse(
        content=todo, content_model=ApiTodo, status_code=HTTPStatus.OK
    )


@todo_blueprint.post("/todo", responses={HTTPStatus.CREATED: ApiTodo})
@inject
async def post(
    body: TodoCreateData,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    new_todo = Todo(
        owner_id=body.owner_id,
        description=body.description,
        due_date=body.due_date,
    )
    todo = await todo_service.create(new_todo)

    return PydanticModelResponse(
        content=todo, content_model=ApiTodo, status_code=HTTPStatus.CREATED
    )


@todo_blueprint.delete(
    "/todo/<uuid:id_>",
    responses={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: TodoNotFoundError,
    },
)
@inject
async def delete(
    path: PathId,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> Any:  # noqa: ANN401
    result = await todo_service.delete(path.id)

    if not result:
        return PydanticModelResponse(
            content=TodoNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )


@todo_blueprint.put(
    "/todo/<uuid:id_>",
    responses={
        HTTPStatus.OK: ApiTodo,
        HTTPStatus.NOT_FOUND: TodoNotFoundError,
    },
)
@inject
async def put(
    path: PathId,
    body: TodoUpdateData,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> PydanticModelResponse:
    new = Todo(
        id=path.id,
        owner_id=body.owner_id,
        description=body.description,
        date_created=body.date_created,
        due_date=body.due_date,
        completed=body.completed,
    )

    todo = await todo_service.put(path.id, new)
    if not todo:
        return PydanticModelResponse(
            content=TodoNotFoundError(), status_code=HTTPStatus.NOT_FOUND
        )

    return PydanticModelResponse(
        content=todo, content_model=ApiTodo, status_code=HTTPStatus.OK
    )
