from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request

from app.containers import Container
from app.domain.exceptions.login_exception import LoginError
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from app.presentation.flask.utils import PydanticModelResponse
from app.presentation.models.login_data import LoginData
from app.presentation.models.login_error import LoginError as ApiLoginError
from app.presentation.models.user import User as ApiUser

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login", methods=["POST"])
@inject
async def login(
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> Any:  # noqa: ANN401
    login_data = LoginData.model_validate(request.json)
    try:
        user = await authentication_service.login(
            username=login_data.username, password=login_data.password
        )
    except LoginError:
        return PydanticModelResponse(
            content_model=ApiLoginError(), status_code=HTTPStatus.BAD_REQUEST
        )
    else:
        return PydanticModelResponse(
            content_model=ApiUser.model_validate(user, from_attributes=True),
            status_code=HTTPStatus.OK,
        )
