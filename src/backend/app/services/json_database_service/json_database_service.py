import asyncio
from abc import ABC
from typing import Generic, Type
from uuid import UUID

from app.services.service_protocols.database_service_protocol import (
    BMT,
    DatabaseServiceProtocol,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.utils import json_utils


class JsonDatabaseService(DatabaseServiceProtocol[BMT], Generic[BMT], ABC):
    def __init__(
        self, io_service: IOServiceProtocol, model_type: Type[BMT]
    ) -> None:
        self.model_type = model_type
        self._io_service = io_service

    def get_all(self) -> list[BMT]:
        return asyncio.run(self._get_data())

    def get(self, id: UUID) -> BMT | None:
        data = asyncio.run(self._get_data())
        return next((item for item in data if item.id == id), None)

    def create(self, new: BMT) -> None:
        data = asyncio.run(self._get_data())

        data.append(new)

        asyncio.run(self._save_file(data))

    def delete(self, id: UUID) -> None:
        data = asyncio.run(self._get_data())

        data = [item for item in data if item.id != id]

        asyncio.run(self._save_file(data))

    def put(self, id: UUID, new: BMT) -> None:
        data = asyncio.run(self._get_data())

        for i, item in enumerate(data):
            if item.id == id:
                data[i] = new
                break

        asyncio.run(self._save_file(data))

    async def _get_data(self) -> list[BMT]:
        files_contents = await self._io_service.read()

        data = json_utils.loads(files_contents)

        return [self.model_type(**item) for item in data]

    async def _save_file(self, data: list) -> None:
        file_contents = json_utils.dumps(data, indent=4)

        await self._io_service.write(file_contents)
