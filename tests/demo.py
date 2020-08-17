import unittest
from pylot.api_helper import send_measurements_in_batches
from pylot.domain import MeasurementsRow
from pylot.security import authenticated_by_login_password
from pylot import InputClient
from pylot.utils.datetime_ex import parse_local_date_time
from tests import init_logging

login = "user"
password = "password"

class DemoTest(unittest.TestCase):
    def setUp(self) -> None:
        init_logging()

    def test_api(self):
        """This is first way (a bit more lower level) of sending measurements to PYLOT cloud.
        This method implies that you yourself compose the list of MeasurementsRow objects that are to be sent to PYLOT API"""
        rows = [
            MeasurementsRow(
                adapter="DemoKubo",
                node="Zone 1",
                timestamp=parse_local_date_time("2017-04-05T14:30:25"),
                data={"1": 27.3, "2": 12.0, "CustomMetric": 133}
            )
        ]

        with authenticated_by_login_password(login, password):
            send_measurements_in_batches(rows)

    def test_accumulate_then_send(self):
        """This is another way of sending data to PYLOT. The difference with the first one is that you use an accumulator.
         You collect incoming measurements into accumulator's memory. When you flush it - they are send to PYLOT API and the accumulator is emptied"""
        client = InputClient("DemoKubo")
        client.authenticate_by_login_password(login, password)
        acc = client.new_measurements_accumulator()
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:30:25"), metric=1, metric_value=27.3)
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:30:25"), metric=2, metric_value=12)
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric="CustomMetric", metric_value=133)
        acc.accumulate(node="Zone 2", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric="CustomMetric", metric_value=144)
        acc.accumulate(node="Zone 2", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric=1, metric_value=12)
        acc.flush()

        acc.accumulate(node="Zone 2", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:32:00"), metric=3, metric_value=33)
        acc.flush()

if __name__ == '__main__':
    unittest.main()
