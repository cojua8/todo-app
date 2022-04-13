import asyncio
import json
import os
from typing import Generic, Type, TypeVar
from uuid import UUID

import aiofiles

from app.models.base_model import BaseModel
from app.utils.enhanced_json_encoder import EnhancedJSONEncoder

T = TypeVar("T", bound=BaseModel)


class JsonDatabaseService(Generic[T]):
    def __init__(
        self, directory_path: str, filename: str, model_type: Type[T]
    ) -> None:
        self.model_type = model_type
        self.filename = filename
        self.jsonfilepath = os.path.join(directory_path, self.filename)

        self.__setup()

    def __setup(self):
        if not os.path.exists(self.jsonfilepath):
            os.makedirs(os.path.dirname(self.jsonfilepath), exist_ok=True)

            asyncio.run(self.__save_file([]))

    def get_all(self) -> list[T]:
        return asyncio.run(self.__get_data())

    def get(self, id: UUID) -> T | None:
        id_hex = id.hex

        data = asyncio.run(self.__get_data())

        for item in data:
            if item.id == id_hex:
                return item

        return None

    def create(self, new: T) -> None:
        data = asyncio.run(self.__get_data())

        data.append(new)

        asyncio.run(self.__save_file(data))

    def delete(self, id: UUID) -> None:
        id_hex = id.hex

        data = asyncio.run(self.__get_data())

        data = [item for item in data if item.id != id_hex]

        asyncio.run(self.__save_file(data))

    def put(self, id: UUID, new: T) -> None:
        id_hex = id.hex

        data = asyncio.run(self.__get_data())

        for i, item in enumerate(data):
            if item.id == id_hex:
                data[i] = new
                break

        asyncio.run(self.__save_file(data))

    async def __get_data(self) -> list[T]:
        async with aiofiles.open(self.jsonfilepath, "r") as jsonfile:
            files_contents = await jsonfile.read()

        data = json.loads(files_contents)

        return [self.model_type(**item) for item in data]

    async def __save_file(self, data: list) -> None:
        file_contents = json.dumps(data, indent=4, cls=EnhancedJSONEncoder)

        async with aiofiles.open(self.jsonfilepath, "w") as jsonfile:
            await jsonfile.write(file_contents)
