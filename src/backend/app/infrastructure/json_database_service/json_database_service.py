from abc import ABC
from typing import Generic
from uuid import UUID

from app.domain.services.database_service_protocol import (
    BMT,
    DatabaseServiceProtocol,
)
from app.infrastructure.io_service import IOServiceProtocol
from app.utils import json_utils


class JsonDatabaseService(DatabaseServiceProtocol[BMT], Generic[BMT], ABC):
    def __init__(
        self, io_service: IOServiceProtocol, model_type: type[BMT]
    ) -> None:
        self.model_type = model_type
        self._io_service = io_service

    async def get_all(self) -> list[BMT]:
        return await self._get_data()

    async def get(self, id_: UUID) -> BMT | None:
        data = await self._get_data()
        return next((item for item in data if item.id == id_), None)

    async def create(self, new: BMT) -> BMT:
        data = await self._get_data()

        data.append(new)

        await self._save_data(data)

        return new

    async def delete(self, id_: UUID) -> bool:
        data = await self._get_data()

        new_data = [item for item in data if item.id != id_]

        if len(new_data) == len(data):
            return False

        await self._save_data(new_data)

        return True

    async def put(self, id_: UUID, new: BMT) -> BMT | None:
        data = await self._get_data()
        updated = False

        for i, item in enumerate(data):
            if item.id == id_:
                data[i] = new
                updated = True
                break

        if updated:
            await self._save_data(data)
            return new

    async def _get_data(self) -> list[BMT]:
        files_contents = await self._io_service.read()

        data = json_utils.loads(files_contents)

        return [self.model_type(**item) for item in data]

    async def _save_data(self, data: list) -> None:
        file_contents = json_utils.dumps(data, indent=4)

        await self._io_service.write(file_contents)
