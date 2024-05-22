from fastapi.responses import JSONResponse
from pydantic import BaseModel


class PydanticModelResponse(JSONResponse):
    def __init__(self, content_model: BaseModel, **kwargs):
        super().__init__(content=content_model.model_dump(), **kwargs)
