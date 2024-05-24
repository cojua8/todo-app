from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request

from app.containers import Container
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.register_data import RegisterData
from app.presentation.models.register_error import RegisterError
from app.presentation.models.user import User as ApiUser

register_blueprint = Blueprint("register", __name__)


@register_blueprint.route("/register", methods=["POST"])
@inject
async def post(
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    register_data = RegisterData.model_validate(request.json)
    result, user = await authentication_service.register(
        username=register_data.username,
        email=register_data.email,
        password=register_data.password,
        confirm_password=register_data.confirm_password,
    )

    if result != RegistrationResult.SUCCESS:
        return PydanticModelResponse(
            content_model=RegisterError(result=result),
            status_code=HTTPStatus.BAD_REQUEST,
        )

    return PydanticModelResponse(
        content_model=ApiUser.model_validate(user, from_attributes=True),
        status_code=HTTPStatus.CREATED,
    )
