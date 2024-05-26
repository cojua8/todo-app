from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.register_data import RegisterData
from app.presentation.models.register_error import RegisterError
from app.presentation.models.user import User as ApiUser

register_blueprint = APIBlueprint("register", __name__)


@register_blueprint.post(
    "/register",
    responses={
        HTTPStatus.CREATED: ApiUser,
        HTTPStatus.BAD_REQUEST: RegisterError,
    },
)
@inject
async def post(
    body: RegisterData,
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    result, user = await authentication_service.register(
        username=body.username,
        email=body.email,
        password=body.password,
        confirm_password=body.confirm_password,
    )

    if result != RegistrationResult.SUCCESS:
        return PydanticModelResponse(
            content=RegisterError(result=result),
            status_code=HTTPStatus.BAD_REQUEST,
        )

    return PydanticModelResponse(
        content=user, content_model=ApiUser, status_code=HTTPStatus.CREATED
    )
