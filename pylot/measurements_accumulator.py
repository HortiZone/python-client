from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List, Callable
from pylot.domain import MeasurementsRow
from pylot.utils import flatmap


class MeasurementsAccumulator:
    def __init__(self, adapter: str, flush_callback:Callable[[List[MeasurementsRow]], Any]) -> None:
        self.adapter = adapter
        self._flush_callback = flush_callback
        self._by_node: Dict[str, Dict[datetime, Dict[str, float]]] = defaultdict(lambda: defaultdict(dict))

    def accumulate(self, node: str, greenhouse_timestamp: datetime, metric: Any, metric_value: float):
        self._by_node[node][greenhouse_timestamp][str(metric)] = metric_value

    def flush(self):
        self._flush_callback(self._get_accumulated_measurements_rows())
        self._by_node = defaultdict(lambda: defaultdict(dict))

    def _get_accumulated_measurements_rows(self) -> List[MeasurementsRow]:
        return flatmap(
            lambda node__dict_by_timestamp: (
                MeasurementsRow(adapter=self.adapter, node=node__dict_by_timestamp[0], timestamp=timestamp, data=measurements)
                for (timestamp, measurements)
                in node__dict_by_timestamp[1].items()
            ),
            self._by_node.items()
        )
