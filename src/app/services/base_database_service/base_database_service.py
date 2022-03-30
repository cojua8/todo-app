from typing import Generic, Protocol, TypeVar
from uuid import UUID


T = TypeVar("T")


class IDatabaseService(Protocol, Generic[T]):
    def get_all(self) -> list[T]:
        ...

    def get(self, id: UUID) -> T | None:
        ...

    def create(self, new: T) -> None:
        ...

    def delete(self, id: UUID) -> None:
        ...

    def put(self, id: UUID, new: T) -> None:
        ...
