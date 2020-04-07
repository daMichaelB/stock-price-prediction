import datetime
import os
import time
from typing import List

import requests

from lib.dtos.stock_api_params_dto import StockApiParams
from lib.dtos.symbol_data_dto import SymbolDataDaily

DATETIME_FORMAT = "%Y-%m-%d"


class StockApi(object):
    """
    API to interact with external data provider to download historical stock data.
    """

    def __init__(self):
        self.url = "https://www.alphavantage.co/query"
        self.api_key = os.environ["API_KEY"]
        self.timeout = 30

    def get_historical(self, symbol: str, start_date: str, end_date: str) -> List[SymbolDataDaily]:
        start_date = datetime.datetime.strptime(start_date, DATETIME_FORMAT)
        end_date = datetime.datetime.strptime(end_date, DATETIME_FORMAT)
        if start_date >= end_date:
            return []

        # TODO: if end_date == start_date: download latest stock price instead of close-price.
        outputsize = "compact" if end_date - start_date < datetime.timedelta(days=20) else "full"

        param_dict = StockApiParams(symbol=symbol, outputsize=outputsize, apikey=self.api_key)

        response = self._get_stock_for_params(param_dict)
        while 'Time Series (Daily)' not in response:
            print("API Limit reached - have to wait until we have access again")
            time.sleep(60)
            response = self._get_stock_for_params(param_dict)

        day_list = self._get_day_list(start_date, end_date)
        ts_daily = response['Time Series (Daily)']
        historical_data = [SymbolDataDaily(adj_close=ts_daily[day]["4. close"], date=day) for day, value in
                           ts_daily.items() if day in day_list]

        return historical_data

    def _get_stock_for_params(self, params: StockApiParams):
        return requests.get(self.url, params=params.__dict__, timeout=self.timeout).json()

    @staticmethod
    def _get_day_list(start_date, end_date):
        return [(start_date + datetime.timedelta(days=x)).strftime(DATETIME_FORMAT) for x in
                range(0, (end_date - start_date).days + 1)]
