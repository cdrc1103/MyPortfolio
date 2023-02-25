import streamlit as st
import pandas as pd
from setup import START_DATE, END_DATE
from portfolio.status import calculate_portfolio_balance
from portfolio.graphs import orchestrate_price_plot, plot_portfolio_balance


def my_portfolio_content(orders: pd.DataFrame) -> None:
    """Render content for My_Portfolio page"""
    portfolio_balance = calculate_portfolio_balance(orders, START_DATE, END_DATE).copy()
    st.plotly_chart(plot_portfolio_balance(END_DATE, portfolio_balance))


def historical_prices_content(orders: pd.DataFrame) -> None:
    """Render content for Historical Prices page"""
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
        orchestrate_price_plot(orders, ticker_map, START_DATE, END_DATE)
