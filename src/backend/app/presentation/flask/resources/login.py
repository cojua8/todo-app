from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container
from app.domain.exceptions.login_exception import LoginError
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from app.presentation.flask.utils import PydanticModelResponse, get_body
from app.presentation.models.login_data import LoginData
from app.presentation.models.login_error import LoginError as ApiLoginError
from app.presentation.models.user import User as ApiUser

login_blueprint = Blueprint("login", __name__)


@login_blueprint.post("/login")
@inject
async def login(
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    login_data = get_body(LoginData)
    try:
        user = await authentication_service.login(
            username=login_data.username, password=login_data.password
        )
    except LoginError:
        return PydanticModelResponse(
            content=ApiLoginError(), status_code=HTTPStatus.BAD_REQUEST
        )
    else:
        return PydanticModelResponse(
            content=user, content_model=ApiUser, status_code=HTTPStatus.OK
        )
