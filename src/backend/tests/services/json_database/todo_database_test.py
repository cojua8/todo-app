from uuid import uuid4

import pytest

from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.utils import json_utils
from tests.factories.todo_factory import TodoFactory


@pytest.fixture
def setup_todos(request, todo_factory: TodoFactory):
    has_params = hasattr(request, "param")
    expected_values = request.param[0] if has_params else {}
    expected_todo = todo_factory.create(**expected_values)

    existing_todo = todo_factory.create_batch(
        request.param[1] if has_params else 1
    )

    db_todos = [expected_todo, *existing_todo]

    yield db_todos, expected_todo


@pytest.fixture
def setup_service(mocker):
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    service = TodosJsonDatabaseService(io_service)

    yield service, io_service


@pytest.mark.parametrize(
    "setup_todos",
    [({}, 4), ({}, 0)],
    indirect=True,
    ids=["return_todo", "return_empty"],
)
async def test_get_all_ok(setup_todos, setup_service):
    # arrange
    todos, _ = setup_todos
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    actual_todos = await todo_service.get_all()

    # assert
    assert actual_todos == todos


@pytest.mark.parametrize("setup_todos", [({"id": uuid4()}, 4)], indirect=True)
async def test_get_returns_todo(setup_todos, setup_service):
    # arrange
    todos, expected_todo = setup_todos
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    actual_todo = await todo_service.get(expected_todo.id)

    # assert
    assert actual_todo.id == expected_todo.id


@pytest.mark.parametrize("setup_todos", [({}, 1)], indirect=True)
async def test_get_returns_none(setup_todos, setup_service):
    # arrange
    todos, _ = setup_todos
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)
    searched_id = uuid4()

    # act
    actual_todo = await todo_service.get(searched_id)

    # assert
    assert actual_todo is None


async def test_create_ok(setup_service, todo_factory):
    # arrange
    todo = todo_factory.create()
    todo_service, io_service = setup_service
    io_service.read.return_value = "[]"

    # act
    await todo_service.create(todo)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps([todo], indent=4)
    )


@pytest.mark.parametrize("setup_todos", [({}, 4)], indirect=True)
async def test_delete_ok(setup_service, setup_todos):
    # arrange
    todos, expected_todo = setup_todos
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    await todo_service.delete(expected_todo.id)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(todos[1:], indent=4)
    )


@pytest.mark.parametrize("setup_todos", [({}, 4)], indirect=True)
async def test_put_updates_record(setup_todos, setup_service, todo_factory):
    # arrange
    todos, expected_todo = setup_todos
    expected_updated_todo = todo_factory.create(id=expected_todo.id)
    expected_todos = [expected_updated_todo, *todos[1:]]

    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    updated_todo = await todo_service.put(
        expected_todo.id, expected_updated_todo
    )

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(expected_todos, indent=4)
    )
    assert updated_todo in expected_todos


@pytest.mark.parametrize("setup_todos", [({}, 4)], indirect=True)
async def test_put_returns_none(setup_todos, setup_service, todo_factory):
    # arrange
    todos, expected_todo = setup_todos
    expected_updated_todo = todo_factory.create(id=expected_todo.id)

    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    updated_todo = await todo_service.put(uuid4(), expected_updated_todo)

    # assert
    assert updated_todo is None


async def test_get_all_by_user_id_ok(setup_service, setup_todos, todo_factory):
    # arrange
    todos, expected_todo = setup_todos
    owner_id = expected_todo.owner_id
    second_todo = todo_factory.create(owner_id=owner_id)
    expected_todos = [second_todo, *todos]

    todos_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(expected_todos)

    # act
    actual_todos = await todos_service.get_all_by_user_id(owner_id)

    # assert
    assert actual_todos == [second_todo, expected_todo]
