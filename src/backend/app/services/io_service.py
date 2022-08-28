import aiopath
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)


class IOService(IOServiceProtocol):
    def __init__(self, file_path: aiopath.AsyncPath) -> None:
        self._file_path = file_path

    @classmethod
    async def create_service(
        cls, directory: str, filename: str
    ) -> "IOService":
        file_path = aiopath.AsyncPath(directory).joinpath(filename)

        if not await file_path.is_file():
            await file_path.parent.mkdir(parents=True, exist_ok=True)

            async with file_path.open("w") as file:
                await file.write("[]")

        return cls(file_path)

    async def read(self) -> str:
        async with self._file_path.open("r") as file:
            content = await file.read()

        return str(content)

    async def write(self, content: str):
        async with self._file_path.open("w") as file:
            await file.write(content)
