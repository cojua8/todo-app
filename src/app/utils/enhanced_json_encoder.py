import json
from datetime import date


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return date.isoformat(o)
        return super().default(o)
