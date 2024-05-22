from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    id: UUID = Field(default_factory=uuid4)
