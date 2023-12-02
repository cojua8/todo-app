import datetime as dt
import json
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:  # noqa: ANN401
        ret_val = None
        if isinstance(o, dt.date):
            ret_val = dt.date.isoformat(o)
        elif isinstance(o, UUID):
            ret_val = o.hex
        elif isinstance(o, BaseModel):
            ret_val = o.model_dump()

        return ret_val or super().default(o)


class _EnhanchedJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        super().__init__(object_hook=self.object_hook, **kwargs)

    def object_hook(self, dict_: dict) -> dict:
        for key, value in dict_.items():
            if key == "id" or "_id" in key:
                dict_[key] = UUID(value)
            elif isinstance(value, str) and (
                date := (
                    self.try_convert_date_to_string(value)
                    or self.try_convert_datetime_to_string(value)
                )
            ):
                dict_[key] = date

        return dict_

    def try_convert_date_to_string(self, v: str) -> dt.date | None:
        try:
            return dt.date.fromisoformat(v)
        except ValueError:
            return None

    def try_convert_datetime_to_string(self, v: str) -> dt.datetime | None:
        try:
            return dt.datetime.fromisoformat(v)
        except ValueError:
            return None


def loads(data: str, **kwargs) -> dict:
    return json.loads(data, cls=_EnhanchedJSONDecoder, **kwargs)


def dumps(data: Any, **kwargs) -> str:  # noqa: ANN401
    return json.dumps(data, cls=_EnhancedJSONEncoder, **kwargs)
