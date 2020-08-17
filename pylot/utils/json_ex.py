import json
from datetime import date, datetime
from enum import Enum

from pylot.utils.datetime_ex import local_date_time_to_json


def encoder():
    return _Encoder


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=encoder(), **kwargs)


class _Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (set, frozenset)):
            return list(o)
        elif isinstance(o, datetime):
            return local_date_time_to_json(o)
        elif isinstance(o, date):
            return str(o)
        elif isinstance(o, Enum):
            return o.name
        # elif dataclasses.is_dataclass(o):
        #     return o.__dict__  # not dataclasses.asdict(o) - since it make deep conversion to dict not considering our JsonSerializable interface
        elif getattr(o, "__dict__", None): #dataclass is also handled here
            return o.__dict__
        return super().default(o)