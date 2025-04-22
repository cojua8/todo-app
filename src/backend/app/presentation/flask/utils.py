from http import HTTPStatus
from typing import TypeVar

from flask import Response, request
from pydantic import BaseModel, TypeAdapter

T = TypeVar("T", bound=BaseModel)


class PydanticModelResponse(Response):
    def __init__(
        self,
        content: object,
        content_model: type | None = None,
        status_code: HTTPStatus = HTTPStatus.OK,
        **kwargs,
    ):
        if content_model is None:
            content_model = type(content)

        super().__init__(
            response=self.adapt_content(content_model, content),
            status=status_code,
            mimetype=kwargs.pop("mimetype", "application/json"),
            **kwargs,
        )

    def adapt_content(self, content_model: type, content: object) -> bytes:
        adapter = TypeAdapter(content_model)

        adapted = adapter.validate_python(content, from_attributes=True)

        return adapter.dump_json(adapted, by_alias=True)


def get_body(model: type[T]) -> T:
    return model.model_validate(request.json)
