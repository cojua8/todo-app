from typing import TypeVar

from pydantic import BaseModel, RootModel

T = TypeVar("T", bound=BaseModel)


class ListOf(RootModel[list[T]]): ...
