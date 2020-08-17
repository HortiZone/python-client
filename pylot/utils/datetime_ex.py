import datetime as dt
from datetime import datetime, date, time

_local_date_time_format = "%Y-%m-%dT%H:%M:%S"
_local_date_format = "%Y-%m-%d"


def parse_local_date_time(s: str) -> datetime:
    return datetime.strptime(s, _local_date_time_format)


def parse_local_date(s: str) -> dt.date:
    return datetime.strptime(s, _local_date_format).date()


def local_date_time_to_json(t: dt.datetime) -> str:
    return t.strftime(_local_date_time_format)
