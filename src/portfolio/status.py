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
def portfolio_value_development(orders: pd.DataFrame, start_date: datetime, end_date: datetime) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate portfolio value development over time by multiplying order values with stock prices"""
    start_date = start_date.date()
    end_date = end_date.date()

    stock_prices = get_stock_prices(orders["Ticker"].unique(), start_date, end_date)
    stock_prices = stock_prices[stock_prices.index <= end_date]

    orders["Type Sign"] = orders["Order Type"].apply(lambda x: -1 if x=="Sell" else 1)
    orders["Number"] = orders["Number"] * orders["Type Sign"]

    portfolio_values = pd.pivot_table(orders, values="Number", index="Order Date", columns="Ticker")
    portfolio_values = cumulative_sum(portfolio_values, start_date, end_date)
    portfolio_values = portfolio_values * stock_prices
    portfolio_values = clean_nan_values(portfolio_values)

    orders["Order Value"] = orders["Number"] * orders["Order Price"]
    transaction_values = pd.pivot_table(orders, values="Order Value", index="Order Date", columns="Ticker")
    transaction_values = cumulative_sum(transaction_values, start_date, end_date)
    transaction_values = clean_nan_values(transaction_values)

    return portfolio_values, transaction_values



def cumulative_sum(values: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """"""
    date_index = pd.date_range(start_date, end_date)
    values = values.reindex(date_index)
    values = values.fillna(0)
    return values.cumsum()

def clean_nan_values(values: pd.DataFrame) -> pd.DataFrame:
    """"""
    values = values.fillna(method="ffill")
    return values.sum(axis=1).replace(0, np.nan)


def get_stock_prices(ticker_list: list, start_date: date, end_date: date) -> pd.DataFrame:
    """Download and post-process stock prices"""
    with download_spinner(HISTORICAL_PRICES):
        stock_prices = download_price_data(ticker_list, start_date, end_date)
    stock_prices = stock_prices.pivot_table(
        index="date", columns="symbol", values="close"
    )
    return stock_prices