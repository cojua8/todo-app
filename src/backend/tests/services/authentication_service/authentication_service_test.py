from unittest import mock

from app.models.user import User
from app.services.authentication_service.authentication_service import (
    AuthenticationService,
)
from app.services.authentication_service.authentication_service_protocol import (  # noqa: E501
    RegistrationResult,
)
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)


def test_password_not_matching(faker):
    # arrange
    mock_user_service = mock.MagicMock(spec=UserServiceProtocol)
    auth_service = AuthenticationService(mock_user_service)

    username = faker.user_name()
    email = faker.email()
    password = "password"
    confirm_password = "other_password"

    # act
    result = auth_service.register(username, email, password, confirm_password)

    # assert
    assert result == RegistrationResult.PASSWORD_NOT_MATCHING


def test_username_already_exists(faker):
    # arrange
    username = faker.user_name()
    email = faker.email()
    password = "password"
    confirm_password = "password"

    mock_user = User(username=username, email=email, password=password)

    mock_user_service = mock.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mock.MagicMock(return_value=mock_user)

    auth_service = AuthenticationService(mock_user_service)

    # act
    result = auth_service.register(username, email, password, confirm_password)

    # assert
    assert result == RegistrationResult.USERNAME_ALREADY_EXISTS


def test_email_already_exists(faker):
    # arrange
    username = faker.user_name()
    email = faker.email()
    password = "password"
    confirm_password = "password"

    mock_user = User(username=username, email=email, password=password)

    mock_user_service = mock.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mock.MagicMock(return_value=None)
    mock_user_service.get_by_email = mock.MagicMock(return_value=mock_user)

    auth_service = AuthenticationService(mock_user_service)

    # act
    result = auth_service.register(username, email, password, confirm_password)

    # assert
    assert result == RegistrationResult.EMAIL_ALREADY_EXISTS


def test_success_creates_user(faker):
    # arrange
    username = faker.user_name()
    email = faker.email()
    password = "password"
    confirm_password = "password"

    mock_user_service = mock.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mock.MagicMock(return_value=None)
    mock_user_service.get_by_email = mock.MagicMock(return_value=None)

    auth_service = AuthenticationService(mock_user_service)

    # act
    # expected_user = User(username=username, email=email, password=password)

    result = auth_service.register(username, email, password, confirm_password)

    # assert
    assert result == RegistrationResult.SUCCESS

    mock_user_service.create.assert_called_once()
