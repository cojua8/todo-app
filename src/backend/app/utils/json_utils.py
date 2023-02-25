import datetime as dt
import json
from dataclasses import is_dataclass
from uuid import UUID


class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.date):
            return dt.date.isoformat(o)
        elif isinstance(o, UUID):
            return o.hex
        elif is_dataclass(o):
            return o.__dict__
        return super().default(o)


class _EnhanchedJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        super().__init__(object_hook=self.object_hook, **kwargs)

    def object_hook(self, dict_):
        for key, value in dict_.items():
            if key == "id" or "_id" in key:
                dict_[key] = UUID(value)
            elif isinstance(value, str):
                if date := (
                    self.try_convert_date_to_string(value)
                    or self.try_convert_datetime_to_string(value)
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


# # pass
# def object_hook(self, dict_):
#     for key in dict_:
#         if key == "id" or "_id" in key:
#             dict_[key] = UUID(dict_[key])

#     return dict_


def loads(data: str, **kwargs):
    # return json.loads(data, object_hook=_id_as_uuid, **kwargs)
    return json.loads(data, cls=_EnhanchedJSONDecoder, **kwargs)


def dumps(data, **kwargs):
    return json.dumps(data, cls=_EnhancedJSONEncoder, **kwargs)
