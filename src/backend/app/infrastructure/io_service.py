import asyncio
from typing import Protocol

import aiopath


class IOServiceProtocol(Protocol):
    async def read(self) -> str: ...

    async def write(self, content: str) -> None: ...


class FileIOService(IOServiceProtocol):
    def __init__(self, file_path: aiopath.AsyncPath) -> None:
        self._file_path = file_path
        self.lock = asyncio.Lock()

    @classmethod
    async def create_service(
        cls, directory: str, filename: str
    ) -> "FileIOService":
        file_path = aiopath.AsyncPath(directory).joinpath(filename)

        if not await file_path.is_file():
            await file_path.parent.mkdir(parents=True, exist_ok=True)

            async with file_path.open("w") as file:
                await file.write("[]")

        return cls(file_path)

    async def read(self) -> str:
        async with self.lock, self._file_path.open("r") as file:
            content = await file.read()

        return str(content)

    async def write(self, content: str) -> None:
        async with self.lock, self._file_path.open("w") as file:
            await file.write(content)
