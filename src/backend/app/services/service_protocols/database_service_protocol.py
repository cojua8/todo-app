from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from app.models.base_model import BaseModel

BMT = TypeVar("BMT", bound=BaseModel)


class DatabaseServiceProtocol(Protocol, Generic[BMT]):
    async def get_all(self) -> Iterable[BMT]:
        ...

    async def get(self, id_: UUID) -> BMT | None:
        ...

    async def create(self, new: BMT) -> None:
        ...

    async def delete(self, id_: UUID) -> None:
        ...

    async def put(self, id_: UUID, new: BMT) -> None:
        ...
