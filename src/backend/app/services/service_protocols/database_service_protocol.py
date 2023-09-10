from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from collections.abc import Iterable
    from uuid import UUID

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
