import json
from dataclasses import is_dataclass
from datetime import date
from uuid import UUID


class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return date.isoformat(o)
        elif isinstance(o, UUID):
            return o.hex
        elif is_dataclass(o):
            return o.__dict__
        return super().default(o)


def _id_as_uuid(dict_):
    for key in dict_:
        if key == "id" or "_id" in key:
            dict_[key] = UUID(dict_[key])

    return dict_


def loads(data: str, **kwargs):
    return json.loads(data, object_hook=_id_as_uuid, **kwargs)


def dumps(data, **kwargs):
    return json.dumps(data, cls=_EnhancedJSONEncoder, **kwargs)
