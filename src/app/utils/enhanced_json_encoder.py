import json
from datetime import date
from uuid import UUID


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return date.isoformat(o)
        elif isinstance(o, UUID):
            return o.hex
        return super().default(o)
