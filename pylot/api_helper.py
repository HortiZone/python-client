from typing import Iterable
from more_itertools import chunked
from . import api
from .domain import MeasurementsRow

_MAX_ROWS_IN_SINGLE_REQUEST = 450


def send_measurements_in_batches(measurements_rows: Iterable[MeasurementsRow]):
    for chunk in chunked(measurements_rows, _MAX_ROWS_IN_SINGLE_REQUEST):
        api.send_measurements(chunk)
