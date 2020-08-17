import unittest
from pylot.domain import MeasurementsRow
from pylot.measurements_accumulator import MeasurementsAccumulator
from pylot.utils.datetime_ex import parse_local_date_time


class TestAccumulation(unittest.TestCase):
    def test(self):
        acc = MeasurementsAccumulator("DemoKubo", lambda x: x)
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:30:25"), metric=1, metric_value=27.3)
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:30:25"), metric=2, metric_value=12)
        acc.accumulate(node="Zone 1", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric="CustomMetric", metric_value=133)
        acc.accumulate(node="Zone 2", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric="CustomMetric", metric_value=144)
        acc.accumulate(node="Zone 2", greenhouse_timestamp=parse_local_date_time("2017-04-05T14:31:01"), metric=1, metric_value=12)

        rows = acc._get_accumulated_measurements_rows()
        self.assertEqual(
            rows[0],
            MeasurementsRow(
                adapter="DemoKubo",
                node="Zone 1",
                timestamp=parse_local_date_time("2017-04-05T14:30:25"),
                data={"1": 27.3, "2": 12.0}
            ))
        self.assertEqual(
            rows[1],
            MeasurementsRow(
                adapter="DemoKubo",
                node="Zone 1",
                timestamp=parse_local_date_time("2017-04-05T14:31:01"),
                data={"CustomMetric": 133}
            ))
        self.assertEqual(
            rows[2],
            MeasurementsRow(
                adapter="DemoKubo",
                node="Zone 2",
                timestamp=parse_local_date_time("2017-04-05T14:31:01"),
                data={"CustomMetric": 144, "1": 12}
            ))


if __name__ == '__main__':
    unittest.main()
