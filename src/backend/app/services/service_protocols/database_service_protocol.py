from typing import Generic, Iterable, Protocol, TypeVar
from uuid import UUID

from app.models.base_model import BaseModel

BMT = TypeVar("BMT", bound=BaseModel)


class DatabaseServiceProtocol(Protocol, Generic[BMT]):
    def get_all(self) -> Iterable[BMT]:
        ...

    def get(self, id: UUID) -> BMT | None:
        ...

    def create(self, new: BMT) -> None:
        ...

    def delete(self, id: UUID) -> None:
        ...

    def put(self, id: UUID, new: BMT) -> None:
        ...
