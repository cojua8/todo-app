import dataclasses
from io import TextIOWrapper
from typing import Generic, TypeVar
import json

from utils.enhanced_json_encoder import EnhancedJSONEncoder


T = TypeVar("T")


class JsonDatabaseService(Generic[T]):
    def __init__(self, filepath: str) -> None:
        self.jsonfilepath = filepath

    def get_all(self) -> list[T]:
        with open(self.jsonfilepath, "r") as jsonfile:
            data = json.load(jsonfile)

        return data

    def create(self, new: T) -> None:
        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            data.append(dataclasses.asdict(new))

            self.__save_file(data, jsonfile)

    def delete(self, id: int) -> None:
        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            data = [item for item in data if item["id"] != id]

            self.__save_file(data, jsonfile)

    def put(self, id: int, new: T) -> None:
        with open(self.jsonfilepath, "r+") as jsonfile:
            data = json.load(jsonfile)

            new_value = dataclasses.asdict(new)

            for i, item in enumerate(data):
                if item["id"] == id:
                    data[i] = new_value
                    break

            self.__save_file(data, jsonfile)

    def __save_file(self, data: list, file: TextIOWrapper) -> None:
        file.truncate(0)
        file.seek(0)
        json.dump(data, file, indent=4, cls=EnhancedJSONEncoder)
