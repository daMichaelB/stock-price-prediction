from typing import Dict, List

from lib.stock_store import StockStore


class DataStats(object):
    """
    Stock Data Statistics. This class contains computation methods to analyze stock data.
    """

    def __init__(self):
        pass

    @classmethod
    def add_mvavg_to_stocks(cls, symbols: List[str]) -> Dict[str, list]:
        """
        With a given list of several stocks, this function will compute the moving average for each stock
        :param symbols: a list of stock_symbols
        :return: A extended dictionary that also contains lists of mvg average stock prices
        """
        mv_avg = dict()
        for symbol in symbols:
            mvg_avg_list = cls._create_moving_average(symbol)

            mv_avg[symbol] = mvg_avg_list
        return mv_avg

    @staticmethod
    def _create_moving_average(symbol: str, window_size: int = 10, alpha: float = 0.1) -> List[float]:
        """
        Calculates the moving average of the Stock prices
        :param symbol:
        :param window_size: moving average window size
        :return: a list with all moving average values
        """
        stock_list = StockStore.load_data_from_file(symbol).adj_close
        mvg_avg_list = list()
        for i in range(window_size):
            mvg_avg_list.insert(0, float(stock_list[len(stock_list) - i - 1]))

        for price in reversed(stock_list[window_size:]):
            mvg_avg = alpha * float(price) + (1 - alpha) * mvg_avg_list[0]
            mvg_avg_list.insert(0, mvg_avg)

        return mvg_avg_list
