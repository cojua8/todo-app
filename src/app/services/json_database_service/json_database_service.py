import dataclasses
from io import TextIOWrapper
import os
from typing import Generic, TypeVar
import json
from uuid import UUID

from app.utils.enhanced_json_encoder import EnhancedJSONEncoder


T = TypeVar("T")


class JsonDatabaseService(Generic[T]):
    filename: str
    model_type: Type[T]

    def __init__(self, directory_path: str) -> None:
        self.jsonfilepath = os.path.join(directory_path, self.filename)

        self.__setup()

    def __setup(self):
        if not os.path.exists(self.jsonfilepath):
            os.makedirs(os.path.dirname(self.jsonfilepath), exist_ok=True)

            with open(self.jsonfilepath, "w") as jsonfile:
                self.__save_file([], jsonfile)

    def get_all(self) -> list[T]:
        with open(self.jsonfilepath, "r") as jsonfile:
            data = json.load(jsonfile)

        return data

    def create(self, new: T) -> None:
        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            data.append(dataclasses.asdict(new))

            self.__save_file(data, jsonfile)

    def delete(self, id: UUID) -> None:
        id_hex = id.hex

        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            data = [item for item in data if item["id"] != id_hex]

            self.__save_file(data, jsonfile)

    def put(self, id: UUID, new: T) -> None:
        id_hex = id.hex

        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            new_value = dataclasses.asdict(new)

            for i, item in enumerate(data):
                if item["id"] == id_hex:
                    data[i] = new_value
                    break

            self.__save_file(data, jsonfile)

    def __save_file(self, data: list, file: TextIOWrapper) -> None:
        file.truncate(0)
        file.seek(0)
        json.dump(data, file, indent=4, cls=EnhancedJSONEncoder)
