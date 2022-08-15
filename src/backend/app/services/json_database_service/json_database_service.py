import asyncio
from abc import ABC
from typing import Generic, Type, TypeVar
from uuid import UUID

from app.models.base_model import BaseModel
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.utils import json_utils

T = TypeVar("T", bound=BaseModel)


class JsonDatabaseService(DatabaseServiceProtocol[T], Generic[T], ABC):
    def __init__(
        self, io_service: IOServiceProtocol, model_type: Type[T]
    ) -> None:
        self.model_type = model_type
        self._io_service = io_service

    def get_all(self) -> list[T]:
        return asyncio.run(self._get_data())

    def get(self, id: UUID) -> T | None:
        data = asyncio.run(self._get_data())

        for item in data:
            if item.id == id:
                return item

        return None

    def create(self, new: T) -> None:
        data = asyncio.run(self._get_data())

        data.append(new)

        asyncio.run(self._save_file(data))

    def delete(self, id: UUID) -> None:
        data = asyncio.run(self._get_data())

        data = [item for item in data if item.id != id]

        asyncio.run(self._save_file(data))

    def put(self, id: UUID, new: T) -> None:
        data = asyncio.run(self._get_data())

        for i, item in enumerate(data):
            if item.id == id:
                data[i] = new
                break

        asyncio.run(self._save_file(data))

    async def _get_data(self) -> list[T]:
        files_contents = await self._io_service.read()

        data = json_utils.loads(files_contents)

        return [self.model_type(**item) for item in data]

    async def _save_file(self, data: list) -> None:
        file_contents = json_utils.dumps(data, indent=4)

        await self._io_service.write(file_contents)
