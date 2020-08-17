from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class MeasurementsRow:
    """
    Represents measurements of a set of metrics in a specific node (greenhouse, climate zone, valve etc) all gathered at the specified timestamp.

    Attributes:

    * adapter: str
        A string unique for each installation of the adapter. This string must be registered in PYLOT cloud and has
        relation to a specific customer location and type of integration.
    * timestamp:
        In ISO 8601 format, represents local time of the greeehouse, NOT UTC
    * node: str
        some string unique for customer nodes. In PYLOT cloud there will be a mapping table that specifies how
        this string maps to a pre-configured customer node. Examples are: "Greenhouse 1", "Valve 2", "AraNet Device 1"
    * data: dict
        Dict key is id of a metric. It should be unique for adapter. Preferably it should be id of the metric in PYLOT.
        Dict value is numeric value of the metric's measurement
    """
    adapter: str
    timestamp: datetime
    node: str
    data: Dict[str, float]
