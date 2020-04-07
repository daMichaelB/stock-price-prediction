import os
import time
from typing import List, Tuple, Dict

import numpy as np

from lib.dtos.symbol_data_dto import SymbolData
from lib.stock_api import StockApi, DATETIME_FORMAT
from lib.stock_store import StockStore


def date_time_self(x):
    return np.array(x, dtype=np.datetime64)


class StockController:
    datetime_format = "%Y-%m-%d"

    def __init__(self):
        self.stock_api = StockApi()
        pass

    @staticmethod
    def _get_start_end_date(symbol: str) -> Tuple[str, str]:
        print("    open file to check what is already downloaded...")
        end_date = time.strftime(DATETIME_FORMAT)
        start_date = StockStore.get_last_available_date(symbol=symbol)
        if start_date is not None:
            return start_date, end_date
        else:
            return "2012-01-01", end_date

    def download_data(self, symbol_list: List[str]) -> Dict[str, SymbolData]:
        if not os.path.exists('data'):
            os.makedirs('data')

        all_data = dict()
        for symbol in symbol_list:
            start_date, end_date = self._get_start_end_date(symbol)

            print("Downloading " + symbol.upper() + " stocks ... (" + str(start_date) + ", " + str(end_date) + ")")
            all_data[symbol.upper()] = StockStore.load_data_from_file(symbol)

            downloaded_data = self.stock_api.get_historical(symbol.upper(), start_date, end_date)

            if len(all_data[symbol.upper()].date) == 0:
                # no file exists yet
                for day in downloaded_data:
                    all_data[symbol.upper()].adj_close.append(day.adj_close)
                    all_data[symbol.upper()].date.append(day.date)
            else:
                for day in reversed(downloaded_data):
                    all_data[symbol.upper()].adj_close.insert(0, day.adj_close)
                    all_data[symbol.upper()].date.insert(0, day.date)

            StockStore.update_stock_file(symbol, all_data)

        return all_data
