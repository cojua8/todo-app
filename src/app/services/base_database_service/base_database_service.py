from typing import Generic, Protocol, TypeVar


T = TypeVar("T")


class IDatabaseService(Protocol, Generic[T]):
    def get_all(self) -> list[T]:
        ...

    def create(self, new: T) -> None:
        ...

    def delete(self, id: int) -> None:
        ...

    def put(self, id: int, new: T) -> None:
        ...
