from app.models.user import User
from app.services.authentication_service.authentication_service_protocol import (  # noqa: E501
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)
from dependency_injector.wiring import inject


class AuthenticationService(AuthenticationServiceProtocol):
    @inject
    def __init__(
        self,
        user_service: UserServiceProtocol,
    ) -> None:
        self.user_service = user_service

    def register(
        self, username: str, email: str, password: str, confirm_password: str
    ) -> RegistrationResult:

        result = RegistrationResult.SUCCESS

        if password != confirm_password:
            result = RegistrationResult.PASSWORD_NOT_MATCHING
        elif self.user_service.get_by_username(username):
            result = RegistrationResult.USERNAME_ALREADY_EXISTS
        elif self.user_service.get_by_email(email):
            result = RegistrationResult.EMAIL_ALREADY_EXISTS

        if result == RegistrationResult.SUCCESS:
            new = User(username=username, email=email, password=password)
            print(new.id)
            self.user_service.create(new)

        return result
