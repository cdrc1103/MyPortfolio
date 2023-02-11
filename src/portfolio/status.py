from datetime import datetime
import pandas as pd


from data.utils import download_stock_data


def calculate_portfolio_balance(order_book: pd.DataFrame, start_date: datetime, end_date: datetime) -> tuple[pd.DataFrame, pd.DataFrame]:
    start_date = start_date.date()
    end_date = end_date.date()
    filter = (order_book["Order Date"] >= start_date) & (order_book["Order Date"] <= end_date)
    portfolio = order_book.loc[filter].copy()
    full_names = portfolio[["Full Name", "Ticker"]].drop_duplicates().set_index(["Ticker"])
    buys = portfolio[portfolio["Order Type"]=="Buy"]
    buys = buys.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    sells = portfolio[portfolio["Order Type"]=="Sell"]
    sells = sells.groupby(["Ticker"]).sum(numeric_only=True)["Number"]
    balance = pd.DataFrame({"buys": buys, "sells": sells}).fillna(0)
    balance["Number"] = balance["buys"] - balance["sells"]
    balance = pd.DataFrame(balance[balance["Number"] != 0]["Number"].astype(int))
    balance = balance.merge(full_names, left_on=balance.index, right_on="Ticker").sort_values("Full Name").set_index("Ticker")


    stock_prices = download_stock_data(balance.index.to_list(), start_date, end_date).copy()
    balance["Closing Price"] = pd.DataFrame(stock_prices["Close"].iloc[-1,:])
    balance["Value"] = balance["Number"] * balance["Closing Price"]
    return balance, stock_prices
