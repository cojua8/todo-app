from typing import Generic, Protocol, TypeVar
from uuid import UUID

from app.domain.models.base_model import BaseModel

BMT = TypeVar("BMT", bound=BaseModel)


class DatabaseServiceProtocol(Protocol, Generic[BMT]):
    async def get_all(self) -> list[BMT]:
        ...

    async def get(self, id_: UUID) -> BMT | None:
        ...

    async def create(self, new: BMT) -> BMT:
        ...

    async def delete(self, id_: UUID) -> bool:
        ...

    async def put(self, id_: UUID, new: BMT) -> BMT | None:
        ...
