import streamlit as st
from settings import START_DATE, END_DATE
from constants import ORDERS
from sidebar import setup_sidebar
from portfolio.graphs import orchestrate_price_plot
from portfolio.status import calculate_portfolio_balance
from settings import START_DATE, END_DATE

# Page config
st.set_page_config(
    page_title="Historical Prices",
    layout="wide",
)

# Set session state variables
if ORDERS not in st.session_state:
    st.session_state[ORDERS] = None

# Header and Intro
st.header("Historical Prices")

# Sidebar
with st.sidebar:
    setup_sidebar()

# Content
orders = st.session_state[ORDERS]
if orders is not None:
    balance = calculate_portfolio_balance(orders, START_DATE, END_DATE).copy()
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
        fig = orchestrate_price_plot(orders, ticker_map, START_DATE, END_DATE)
