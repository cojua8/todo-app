from http import HTTPStatus

from flask import Response
from pydantic import BaseModel


class PydanticModelResponse(Response):
    def __init__(
        self,
        content_model: BaseModel,
        status_code: HTTPStatus = HTTPStatus.OK,
        **kwargs
    ):
        super().__init__(
            response=content_model.model_dump_json(),
            status=status_code,
            mimetype=kwargs.pop("mimetype", "application/json"),
            **kwargs,
        )
