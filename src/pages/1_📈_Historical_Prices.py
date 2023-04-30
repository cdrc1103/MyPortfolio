import streamlit as st
from setup import register_session_state_variable
from constants import ORDERS
from sidebar import setup_sidebar
from setup import START_DATE, END_DATE
from portfolio.status import portfolio_stock_allocation
from portfolio.graphs import orchestrate_price_plot

# Page config
st.set_page_config(
    page_title="Historical Prices",
    layout="wide",
)

# Set session state variables
register_session_state_variable(ORDERS)

# Header and Intro
st.header("Historical Prices")

# Sidebar
with st.sidebar:
    setup_sidebar()

# Content
orders = st.session_state[ORDERS]
if orders is not None:
    balance = portfolio_stock_allocation(orders, START_DATE, END_DATE).copy()
    stocks = orders[["Ticker", "Full Name"]].drop_duplicates().set_index(["Ticker"])
    tickers = stocks.index.to_list()
    selected_tickers = st.multiselect(
        "Select tickers to show historical prices:", tickers, balance.index.tolist()
    )
    if selected_tickers:
        ticker_map = {
            ticker: full_name
            for ticker, full_name in stocks.loc[selected_tickers, "Full Name"].items()
        }
        orchestrate_price_plot(orders, ticker_map, START_DATE, END_DATE)
