import streamlit as st

from constants import ORDER_BOOK
from data.utils import load_order_book
from portfolio.graphs import plot_historic_prices
from settings import START_DATE, END_DATE

# Page config
st.set_page_config(
    page_title="Historical Prices",
    layout="wide",
)

# Set session state variables
if ORDER_BOOK not in st.session_state:
    st.session_state[ORDER_BOOK] = None

# Header and Intro
st.header("Historical Prices")

# Sidebar
with st.sidebar:
    load_order_book()

# Content
order_book = st.session_state[ORDER_BOOK]
if order_book is not None:
    ticker_map = (
        order_book[["Ticker", "Full Name"]].drop_duplicates().set_index(["Ticker"])
    )
    tickers = ticker_map.index.to_list()
    selected_tickers = st.multiselect(
        "Select tickers to show historical prices:", tickers, tickers[0:4]
    )
    selected_fullnames = ticker_map.loc[selected_tickers, "Full Name"].to_list()

    fig = plot_historic_prices(
        START_DATE, END_DATE, order_book, selected_tickers, selected_fullnames
    )
    st.plotly_chart(fig)
