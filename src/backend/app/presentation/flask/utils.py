from collections.abc import Sequence
from http import HTTPStatus
from typing import TypeVar

from flask import Response, request
from pydantic import BaseModel, TypeAdapter

T = TypeVar("T", bound=BaseModel)


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


class PydanticListModelResponse(Response):
    def __init__(
        self,
        item_type: type[BaseModel],
        items: Sequence[BaseModel],
        status_code: HTTPStatus = HTTPStatus.OK,
        **kwargs
    ):
        adapted = self.model_list_json(item_type, items)
        super().__init__(
            response=adapted,
            status=status_code,
            mimetype=kwargs.pop("mimetype", "application/json"),
            **kwargs,
        )

    def model_list_json(self, model: type[T], values: object) -> bytes:
        adapter = TypeAdapter(list[model])

        adapted = adapter.validate_python(values, from_attributes=True)

        return adapter.dump_json(adapted)


def get_body(model: type[T]) -> T:
    return model.model_validate(request.json)
