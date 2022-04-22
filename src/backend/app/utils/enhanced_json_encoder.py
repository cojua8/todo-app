import json
from dataclasses import is_dataclass
from datetime import date
from uuid import UUID


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return date.isoformat(o)
        elif isinstance(o, UUID):
            return o.hex
        elif is_dataclass(o):
            return o.__dict__
        return super().default(o)
