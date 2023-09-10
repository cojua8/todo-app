from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Generic

from app.services.service_protocols.database_service_protocol import (
    BMT,
    DatabaseServiceProtocol,
)
from app.utils import json_utils

if TYPE_CHECKING:
    from uuid import UUID

    from app.services.service_protocols.io_service_protocol import (
        IOServiceProtocol,
    )


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

    async def create(self, new: BMT) -> None:
        data = await self._get_data()

        data.append(new)

        await self._save_file(data)

    async def delete(self, id_: UUID) -> None:
        data = await self._get_data()

        data = [item for item in data if item.id != id_]

        await self._save_file(data)

    async def put(self, id_: UUID, new: BMT) -> None:
        data = await self._get_data()

        for i, item in enumerate(data):
            if item.id == id_:
                data[i] = new
                break

        await self._save_file(data)

    async def _get_data(self) -> list[BMT]:
        files_contents = await self._io_service.read()

        data = json_utils.loads(files_contents)

        return [self.model_type(**item) for item in data]

    async def _save_file(self, data: list) -> None:
        file_contents = json_utils.dumps(data, indent=4)

        await self._io_service.write(file_contents)
