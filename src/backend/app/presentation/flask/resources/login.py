from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint

from app.containers import Container
from app.domain.exceptions.login_exception import LoginError
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.login_data import LoginData
from app.presentation.models.login_error import LoginError as ApiLoginError
from app.presentation.models.user import User as ApiUser

login_blueprint = APIBlueprint("login", __name__)


@login_blueprint.post(
    "/login",
    responses={HTTPStatus.OK: ApiUser, HTTPStatus.BAD_REQUEST: ApiLoginError},
)
@inject
async def login(
    body: LoginData,
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    try:
        user = await authentication_service.login(
            username=body.username, password=body.password
        )
    except LoginError:
        return PydanticModelResponse(
            content=ApiLoginError(), status_code=HTTPStatus.BAD_REQUEST
        )
    else:
        return PydanticModelResponse(
            content=user, content_model=ApiUser, status_code=HTTPStatus.OK
        )
