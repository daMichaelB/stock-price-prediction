from dataclasses import dataclass


@dataclass
class StockApiParams(object):
    symbol: str
    outputsize: str
    apikey: str
    function: str = "TIME_SERIES_DAILY"
