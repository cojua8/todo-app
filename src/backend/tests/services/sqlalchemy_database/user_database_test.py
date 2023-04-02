from uuid import uuid4

import pytest

from app.services.sql_database_service.users_service import UsersService


@pytest.fixture
def users_service(db_engine):
    yield UsersService(db_engine)


def test_get_all(user_factory, users_service):
    # Arrange
    expected_users = user_factory.create_batch(2)
    for user in expected_users:
        users_service.create(user)

    # Act
    actual_users = users_service.get_all()

    # Assert
    assert actual_users == expected_users


def test_get_returns_user(user_factory, users_service):
    # Arrange
    expected_user = user_factory()
    users_service.create(expected_user)

    # Act
    actual_user = users_service.get(expected_user.id)

    # Assert
    assert actual_user == expected_user


def test_get_returns_none(users_service):
    # Arrange
    id_ = uuid4()

    # Act
    actual_user = users_service.get(id_)

    # Assert
    assert actual_user is None


def test_create(user_factory, db_engine):
    # Arrange
    user_service = UsersService(db_engine)
    user = user_factory.create()

    # Act
    user_service.create(user)
    actual_user = user_service.get(user.id)

    # Assert
    assert actual_user == user


def test_delete(user_factory, users_service):
    # Arrange
    user = user_factory.create()
    users_service.create(user)

    # Act
    users_service.delete(user.id)

    # Assert
    assert users_service.get_all() == []


def test_put(user_factory, users_service):
    # Arrange
    id_ = uuid4()
    original_user = user_factory.create(id=id_)
    users_service.create(original_user)

    # modified the created user
    modified_user = user_factory.create(id=id_)
    # Act
    users_service.put(id_, modified_user)

    # Assert
    assert users_service.get_all() == [modified_user]


def test_get_by_email_returns_first_found(user_factory, users_service):
    # Arrange
    email = "some@email.com"
    user = user_factory.create(email=email)
    users_service.create(user)

    # Act
    actual_user = users_service.get_by_email(email)

    # Assert
    assert actual_user == user


def test_get_by_email_returns_none(user_factory, users_service):
    # Arrange
    email = "some@email.com"
    user = user_factory.create(email=email)
    users_service.create(user)

    # Act
    actual_user = users_service.get_by_email("some_other@email.com")

    # Assert
    assert actual_user is None


def test_get_by_username_returns_first_found(user_factory, users_service):
    # Arrange
    username = "some_username"
    user = user_factory.create(username=username)
    users_service.create(user)

    # Act
    actual_user = users_service.get_by_username(username)

    # Assert
    assert actual_user == user


def test_get_by_username_returns_none(user_factory, users_service):
    # Arrange
    username = "some_username"
    user = user_factory.create(username=username)
    users_service.create(user)

    # Act
    actual_user = users_service.get_by_email("some_other_username")

    # Assert
    assert actual_user is None
