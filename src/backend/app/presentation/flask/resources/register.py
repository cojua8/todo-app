from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.presentation.flask.utils import PydanticModelResponse, get_body
from app.presentation.models.register_data import RegisterData
from app.presentation.models.register_error import RegisterError
from app.presentation.models.user import User as ApiUser

register_blueprint = Blueprint("register", __name__)


@register_blueprint.post("/register")
@inject
async def post(
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    register_data = get_body(RegisterData)
    result, user = await authentication_service.register(
        username=register_data.username,
        email=register_data.email,
        password=register_data.password,
        confirm_password=register_data.confirm_password,
    )

    if result != RegistrationResult.SUCCESS:
        return PydanticModelResponse(
            content=RegisterError(result=result),
            status_code=HTTPStatus.BAD_REQUEST,
        )

    return PydanticModelResponse(
        content=user, content_model=ApiUser, status_code=HTTPStatus.CREATED
    )
