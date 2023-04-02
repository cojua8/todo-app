from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.services.sql_database_service.todos_service import TodosService
from app.services.sql_database_service.users_service import UsersService


@pytest.fixture
def todos_service(db_engine):
    yield TodosService(db_engine)


@pytest.fixture
def users_service(db_engine):
    yield UsersService(db_engine)


@pytest.fixture
def user(users_service, user_factory):
    user = user_factory.create()
    users_service.create(user)
    yield user


def test_get_all(todo_factory, todos_service, user):
    # Arrange
    expected_todos = todo_factory.create_batch(2, owner_id=user.id)
    for todo in expected_todos:
        todos_service.create(todo)

    # Act
    actual_todos = todos_service.get_all()

    # Assert
    assert actual_todos == expected_todos


def test_get_returns_todo(todo_factory, todos_service, user):
    # Arrange
    expected_todo = todo_factory(owner_id=user.id)
    todos_service.create(expected_todo)

    # Act
    actual_todos = todos_service.get(expected_todo.id)

    # Assert
    assert actual_todos == expected_todo


def test_get_returns_none(todos_service):
    # Arrange
    id_ = uuid4()

    # Act
    actual_todo = todos_service.get(id_)

    # Assert
    assert actual_todo is None


def test_create_ok(todo_factory, todos_service, user):
    # Arrange
    todo = todo_factory.create(owner_id=user.id)

    # Act
    todos_service.create(todo)

    # Assert
    actual_todo = todos_service.get(todo.id)
    assert actual_todo == todo


def test_create_fails_on_non_existent_owner_id(todo_factory, todos_service):
    # Arrange
    todo = todo_factory.create()

    # Act
    with pytest.raises(IntegrityError):
        todos_service.create(todo)


def test_delete(todo_factory, todos_service, user):
    # Arrange
    todo = todo_factory.create(owner_id=user.id)
    todos_service.create(todo)

    # Act
    todos_service.delete(todo.id)

    # Assert
    assert todos_service.get_all() == []


def test_put(todo_factory, todos_service, user):
    # Arrange
    id_ = uuid4()
    original_todo = todo_factory.create(id=id_, owner_id=user.id)
    todos_service.create(original_todo)

    # modified the created user
    modified_todo = todo_factory.create(id=id_, owner_id=user.id)
    # Act
    todos_service.put(id_, modified_todo)

    # Assert
    assert todos_service.get_all() == [modified_todo]


def test_get_all_by_user_id(
    todo_factory, todos_service, user, users_service, user_factory
):
    # Arrange
    expected_todos = todo_factory.create_batch(2, owner_id=user.id)

    second_user = user_factory.create()
    users_service.create(second_user)

    all_todos = [*expected_todos, todo_factory.create(owner_id=second_user.id)]
    for todo in all_todos:
        todos_service.create(todo)

    # Act
    actual_todos = todos_service.get_all_by_user_id(user.id)

    # Assert
    assert actual_todos == expected_todos
