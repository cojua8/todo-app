from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field


def to_camel(string: str) -> str:
    words = string.split("_")
    capital_words = "".join(word.capitalize() for word in words[1:])
    return words[0] + capital_words


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: UUID = Field(default_factory=uuid4)  # noqa: A003
