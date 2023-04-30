from datetime import datetime, date
import pandas as pd
import numpy as np
import streamlit as st
from constants import HISTORICAL_PRICES
from resources.utils import download_spinner
from resources.yahoo import download_price_data


@st.cache_data(show_spinner=False)
def portfolio_stock_allocation(
    orders: pd.DataFrame, start_date: datetime, end_date: datetime
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate the value of each stock in a portfolio from list of orders over a given timeframe"""
    start_date = start_date.date()
    end_date = end_date.date()

    filter = (orders["Order Date"] >= start_date) & (orders["Order Date"] <= end_date)
    orders = orders.loc[filter]
    buys = orders[orders["Order Type"] == "Buy"]
    buys = buys.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    sells = orders[orders["Order Type"] == "Sell"]
    sells = sells.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    portfolio = pd.DataFrame({"buys": buys, "sells": sells}).fillna(0)
    portfolio["Number"] = portfolio["buys"] - portfolio["sells"]
    portfolio = pd.DataFrame(portfolio[portfolio["Number"] != 0]["Number"].astype(int))
    stock_identifiers = (
        orders[["Full Name", "Ticker", "ISIN"]]
        .drop_duplicates()
        .set_index(["Ticker"])
    )
    portfolio = (
        portfolio.merge(stock_identifiers, left_on=portfolio.index, right_on="Ticker")
        .sort_values("Full Name")
        .set_index("Ticker")
    )

    stock_prices = get_stock_prices(portfolio.index.to_list(), start_date, end_date)
    portfolio["Closing Price"] = stock_prices[stock_prices.index <= end_date].iloc[-1, :]
    portfolio["Value"] = portfolio["Number"] * portfolio["Closing Price"]
    return portfolio


@st.cache_data(show_spinner=False)
def portfolio_value_development(orders: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """"""
    start_date = start_date.date()
    end_date = end_date.date()

    stock_prices = get_stock_prices(orders["Ticker"].unique(), start_date, end_date)
    stock_prices = stock_prices[stock_prices.index <= end_date]

    orders["Type Sign"] = orders["Order Type"].apply(lambda x: -1 if x=="Sell" else 1)
    orders["Number"] = orders["Number"] * orders["Type Sign"]
    orders = pd.pivot_table(orders, values="Number", index="Order Date", columns="Ticker")
    date_index = pd.date_range(start_date, end_date)
    orders = orders.reindex(date_index)
    orders = orders.fillna(0)
    orders = orders.cumsum()
    portfolio_value = orders * stock_prices
    portfolio_value = portfolio_value.fillna(method="ffill")
    return portfolio_value.sum(axis=1).replace(0, np.nan)


def get_stock_prices(ticker_list: list, start_date: date, end_date: date) -> pd.DataFrame:
    """"""
    with download_spinner(HISTORICAL_PRICES):
        stock_prices = download_price_data(ticker_list, start_date, end_date)
    stock_prices = stock_prices.pivot_table(
        index="date", columns="symbol", values="close"
    )
    return stock_prices