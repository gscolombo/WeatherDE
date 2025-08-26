from typing import Literal, TypedDict

from shared.collection import _Collection


class TimeSeriesOptions(TypedDict):
    timeField: str
    metaField: str
    granularity: Literal["seconds", "minutes", "hours"]
    expireAfterSeconds: int


class TimeSeries(_Collection):
    def __init__(self, name, timeseries: TimeSeriesOptions, **kwargs):
        super().__init__(name, timeseries=timeseries, **kwargs)
