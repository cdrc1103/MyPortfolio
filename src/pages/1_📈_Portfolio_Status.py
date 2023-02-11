import streamlit as st

from data.utils import load_file
from constants import TICKER_BASE, ORDER_BOOK
from portfolio.graphs import plot_historic_prices
from settings import START_DATE, END_DATE

ticker_base = load_file(TICKER_BASE)
order_book = load_file(ORDER_BOOK)


ticker_names = ticker_base["Ticker"].to_list()
ticker_selections = st.multiselect(
    "Pick the tickers for historic prices", ticker_names, ticker_names[0:4]
)
fig = plot_historic_prices(START_DATE, END_DATE, order_book, ticker_selections)
st.plotly_chart(fig)
