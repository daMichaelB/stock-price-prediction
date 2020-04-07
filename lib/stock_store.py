import csv
import datetime
import os
from typing import Dict, Tuple

from lib.dtos.symbol_data_dto import SymbolData
from lib.stock_api import DATETIME_FORMAT


class StockStore(object):

    def __init__(self):
        pass

    @classmethod
    def load_data_from_file(cls, symbol: str) -> SymbolData:
        filename = os.path.dirname(os.path.realpath(__file__)) + '/../data/csv/' + str(symbol).lower() + '.csv'
        date_list, adj_close_list = list(), list()
        if os.path.isfile(filename):
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    adj_close_list.append(row['adj_close'])
                    date_list.append(row['date'])
            return SymbolData(date=date_list, adj_close=adj_close_list)
        else:
            return SymbolData()

    @staticmethod
    def update_stock_file(symbol: str, data: Dict[str, SymbolData]):
        with open('data/csv/' + symbol.lower() + '.csv', 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['date', 'adj_close'])
            writer.writeheader()
            for i in range(0, len(data[symbol.upper()].date)):
                writer.writerow({'date': data[symbol.upper()].date[i],
                                 'adj_close': data[symbol.upper()].adj_close[i]})

    @staticmethod
    def get_last_available_date(symbol: str) -> str:
        filename = os.path.dirname(os.path.realpath(__file__)) + '/../data/csv/' + str(symbol).lower() + '.csv'
        if os.path.isfile(filename):
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                row = next(reader)
                start_date_time = datetime.datetime.strptime(row['date'], DATETIME_FORMAT)
                start_date = start_date_time + datetime.timedelta(days=1)
                start_date = datetime.datetime.strftime(start_date, DATETIME_FORMAT)

            return start_date
        else:
            return ""
