import pandas as pd
import streamlit as st

from inputfiles.stock_symbols import DAX_SYMBOLS, MSCI_WORLD_SYMBOLS
from lib.data_stats import DataStats
from lib.stock_controller import StockController

st.title('Stock Analyzer')


def main():
    sc = StockController()
    # find the symbol for each stock at de.finance.yahoo.com. This symbol is also known by alpha-vantage.
    stock_symbols = MSCI_WORLD_SYMBOLS + DAX_SYMBOLS

    stock_symbols = st.sidebar.multiselect('Select stocks:', stock_symbols)

    all_data = sc.download_data(stock_symbols)
    mvg_avg = DataStats.add_mvavg_to_stocks(list(all_data.keys()))

    for stock in stock_symbols:
        st.markdown(f"## {stock}")
        df = pd.DataFrame({"adj_close": all_data[stock.upper()].adj_close[::-1],
                           "MovingAVG": mvg_avg[stock.upper()][::-1]},
                          columns=["adj_close", "MovingAVG"]).astype(float)
        st.write(df)
        st.line_chart(df)


if __name__ == "__main__":
    main()
