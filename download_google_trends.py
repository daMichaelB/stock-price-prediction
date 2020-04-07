import streamlit as st
from pytrends.dailydata import get_daily_data

from inputfiles.stock_symbols import MSCI_WORLD_SYMBOLS, DAX_SYMBOLS

START_YEAR = 2012
START_MONTH = 1
END_YEAR = 2020
END_MONTH = 1


def main():
    stock_symbols = st.sidebar.multiselect('Select stocks:', (MSCI_WORLD_SYMBOLS + DAX_SYMBOLS))

    for stock in stock_symbols:
        # TODO: also search for "{stock} portfolio" or "{stock} stock"
        df = get_daily_data(f"{stock}", START_YEAR, START_MONTH, END_YEAR, END_MONTH, geo="", wait_time=1.0)
        st.write(df)
        st.line_chart(df)
        df.to_csv(f"data/trends/{stock}.csv")


if __name__ == "__main__":
    main()
