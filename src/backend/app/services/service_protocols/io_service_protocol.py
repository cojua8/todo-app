from typing import Protocol


class IOServiceProtocol(Protocol):
    async def read(self) -> str:
        ...

    async def write(self, content: str) -> None:
        ...
