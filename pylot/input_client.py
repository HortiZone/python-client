from typing import Iterable
from pylot.api_helper import send_measurements_in_batches
from pylot.security import SecurityContext
from pylot.utils.design_by_contract import ensure_precondition
from .domain import MeasurementsRow
from .measurements_accumulator import MeasurementsAccumulator
from .security import authenticated_by_login_password


class InputClient:
    security_context: SecurityContext

    def __init__(self, adapter: str):
        self.adapter = adapter

    def authenticate_by_login_password(self, login, password):
        self.security_context = authenticated_by_login_password(login, password)

    def new_measurements_accumulator(self):
        return MeasurementsAccumulator(self.adapter, lambda rows: self.send(rows))

    def send(self, measurements_rows: Iterable[MeasurementsRow]):
        ensure_precondition(self.security_context, "method 'authenticate_by_login_password' was not called on the client")
        with self.security_context:
            send_measurements_in_batches(measurements_rows)
