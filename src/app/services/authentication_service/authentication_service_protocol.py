from enum import Enum, auto
from typing import Protocol


class RegistrationResult(Enum):
    SUCCESS = auto()
    PASSWORD_NOT_MATCHING = auto()
    USERNAME_ALREADY_EXISTS = auto()
    EMAIL_ALREADY_EXISTS = auto()


class AuthenticationServiceProtocol(Protocol):
    def register(
        self, name: str, email: str, password: str, confirm_password: str
    ) -> RegistrationResult:
        ...
