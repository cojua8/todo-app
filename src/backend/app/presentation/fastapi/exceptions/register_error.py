from http import HTTPStatus

from fastapi import HTTPException

from app.domain.services.authentication_service_protocol import (
    RegistrationResult,
)


class RegisterError(HTTPException):
    def __init__(self, register_result: RegistrationResult):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail=register_result.name
        )
