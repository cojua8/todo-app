from typing import cast
from uuid import uuid4

import pytest
from app.models.todo import Todo
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.utils import json_utils
from tests.factories.todo_factory import TodoFactory


@pytest.fixture
def setup(request, todo_factory: TodoFactory):
    expected_values = request.param[0]
    expected_todo = todo_factory.create(**expected_values)

    existing_todo = todo_factory.create_batch(request.param[1])

    db_todos = [expected_todo, *existing_todo]

    yield json_utils.dumps(db_todos), expected_todo


@pytest.mark.parametrize(
    "setup",
    [({}, 4), ({}, 0)],
    indirect=True,
    ids=["return_todo", "return_empty"],
)
def test_get_all_ok(mocker, setup):
    # arrange
    todos, _ = setup
    expected_todos = [Todo(**v) for v in json_utils.loads(todos)]
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = todos

    service = TodosJsonDatabaseService(io_service)
    # act
    actual_todos = service.get_all()

    # assert
    assert actual_todos == expected_todos


@pytest.mark.parametrize(
    "setup",
    [({"id": uuid4()}, 4), ({}, 0)],
    indirect=True,
    ids=["return_todo", "return_none"],
)
def test_get_returns_user(mocker, setup):
    # arrange
    todos, expected_todo = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = todos

    service = TodosJsonDatabaseService(io_service)
    # act
    actual_todo = cast(Todo, service.get(expected_todo.id))

    # assert
    if actual_todo:
        assert actual_todo.id == expected_todo.id


def test_get_returns_none(mocker, todo_factory: TodoFactory):
    # arrange
    id = uuid4()
    todos = todo_factory.create_batch(4)

    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(todos)

    service = TodosJsonDatabaseService(io_service)
    # act
    actual_todo = cast(Todo, service.get(id))

    # assert
    assert actual_todo is None


def test_create_ok(mocker, todo_factory: TodoFactory):
    # arrange
    todo = todo_factory.create()
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = "[]"

    service = TodosJsonDatabaseService(io_service)
    # act
    service.create(todo)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps([todo], indent=4)
    )


@pytest.mark.parametrize("setup", [({}, 4)], indirect=True)
def test_delete_ok(mocker, setup):
    # arrange
    todos, expected_todo = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = todos

    service = TodosJsonDatabaseService(io_service)
    # act
    service.delete(expected_todo.id)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(json_utils.loads(todos)[1:], indent=4)
    )


@pytest.mark.parametrize("setup", [({}, 4)], indirect=True)
def test_put_ok(mocker, setup):
    # arrange
    todos, expected_todo = setup
    updated_todo = TodoFactory.create(id=expected_todo.id)
    expected_todos = [updated_todo, *json_utils.loads(todos)[1:]]

    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = todos

    service = TodosJsonDatabaseService(io_service)
    # act
    service.put(expected_todo.id, updated_todo)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(expected_todos, indent=4)
    )
