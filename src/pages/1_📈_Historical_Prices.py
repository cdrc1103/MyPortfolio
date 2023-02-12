import streamlit as st
from settings import START_DATE, END_DATE
from constants import ORDER_BOOK
from data.utils import load_order_book
from portfolio.graphs import orchestrate_price_plot, plot_historic_prices
from portfolio.status import calculate_portfolio_balance
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
    balance = calculate_portfolio_balance(order_book, START_DATE, END_DATE).copy()
    ticker_map = (
        order_book[["Ticker", "Full Name"]].drop_duplicates().set_index(["Ticker"])
    )
    tickers = ticker_map.index.to_list()
    selected_tickers = st.multiselect(
        "Select tickers to show historical prices:", tickers, balance.index.tolist()
    )
    selected_tickers = {
        ticker: full_name
        for ticker, full_name in ticker_map.loc[selected_tickers, "Full Name"].items()
    }

    fig = orchestrate_price_plot(order_book, selected_tickers, START_DATE, END_DATE)
