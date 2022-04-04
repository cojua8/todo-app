import json
import os
from typing import Generic, Type, TypeVar
from uuid import UUID

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

            self.__save_file([])

    def get_all(self) -> list[T]:
        return self.__get_data()

    def get(self, id: UUID) -> T | None:
        id_hex = id.hex

        data = self.__get_data()

        for item in data:
            if item.id == id_hex:
                return item

        return None

    def create(self, new: T) -> None:
        data = self.__get_data()

        data.append(new)

        self.__save_file(data)

    def delete(self, id: UUID) -> None:
        id_hex = id.hex

        data = self.__get_data()

        data = [item for item in data if item.id != id_hex]

        self.__save_file(data)

    def put(self, id: UUID, new: T) -> None:
        id_hex = id.hex

        data = self.__get_data()

        for i, item in enumerate(data):
            if item.id == id_hex:
                data[i] = new
                break

            self.__save_file(data)

    def __get_data(self) -> list[T]:
        with open(self.jsonfilepath, "r") as jsonfile:
            data = json.load(jsonfile)

        return [self.model_type(**item) for item in data]

    def __save_file(self, data: list) -> None:
        with open(self.jsonfilepath, "w") as jsonfile:
            json.dump(data, jsonfile, indent=4, cls=EnhancedJSONEncoder)
