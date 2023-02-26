from datetime import datetime
import pandas as pd
import streamlit as st
from constants import HISTORICAL_PRICES
from resources.utils import download_spinner
from resources.yahoo import download_price_data


@st.cache_data(show_spinner=False)
def calculate_portfolio_balance(
    orders: pd.DataFrame, start_date: datetime, end_date: datetime
) -> tuple[pd.DataFrame, pd.DataFrame]:
    start_date = start_date.date()
    end_date = end_date.date()
    filter = (orders["Order Date"] >= start_date) & (orders["Order Date"] <= end_date)
    portfolio = orders.loc[filter].copy()
    buys = portfolio[portfolio["Order Type"] == "Buy"]
    buys = buys.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    sells = portfolio[portfolio["Order Type"] == "Sell"]
    sells = sells.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    balance = pd.DataFrame({"buys": buys, "sells": sells}).fillna(0)
    balance["Number"] = balance["buys"] - balance["sells"]
    balance = pd.DataFrame(balance[balance["Number"] != 0]["Number"].astype(int))
    stock_identifiers = (
        portfolio[["Full Name", "Ticker", "ISIN"]]
        .drop_duplicates()
        .set_index(["Ticker"])
    )
    balance = (
        balance.merge(stock_identifiers, left_on=balance.index, right_on="Ticker")
        .sort_values("Full Name")
        .set_index("Ticker")
    )

    with download_spinner(HISTORICAL_PRICES):
        stock_prices = download_price_data(balance.index.to_list())

    balance["Closing Price"] = stock_prices.pivot_table(
        index="date", columns="symbol", values="close"
    ).iloc[-1, :]
    balance["Value"] = balance["Number"] * balance["Closing Price"]
    return balance
