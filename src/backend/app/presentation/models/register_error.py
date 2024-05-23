from pydantic import BaseModel

from app.domain.services.authentication_service_protocol import (
    RegistrationResult,
)


class RegisterError(BaseModel):
    result: RegistrationResult
