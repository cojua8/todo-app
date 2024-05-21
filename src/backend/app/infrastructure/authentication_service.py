from app.domain.models.user import User
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.exceptions.login_exception import LoginError


class AuthenticationService(AuthenticationServiceProtocol):
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self.user_service = user_service

    async def register(
        self, username: str, email: str, password: str, confirm_password: str
    ) -> tuple[RegistrationResult, User | None]:
        registration_result = RegistrationResult.SUCCESS
        new_user = None

        if password != confirm_password:
            registration_result = RegistrationResult.PASSWORD_NOT_MATCHING
        elif await self.user_service.get_by_username(username):
            registration_result = RegistrationResult.USERNAME_ALREADY_EXISTS
        elif await self.user_service.get_by_email(email):
            registration_result = RegistrationResult.EMAIL_ALREADY_EXISTS

        if registration_result == RegistrationResult.SUCCESS:
            new_user = User(username=username, email=email, password=password)
            await self.user_service.create(new_user)

        return registration_result, new_user

    async def login(self, username: str, password: str) -> User:
        user = await self.user_service.get_by_username(username)

        if not user or password != user.password:
            raise LoginError

        return user
