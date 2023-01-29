from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf
import streamlit as st

base_path = Path("src/data")

    
def load_file(file_name: str) -> pd.DataFrame:
    """Load order book from file"""
    order_book = pd.read_csv(base_path.joinpath(f"{file_name}.csv"))
    order_book["Order Date"] = pd.to_datetime(order_book["Order Date"]).dt.date
    return order_book


def update_file(file_name: str, data_frame: pd.DataFrame) -> pd.DataFrame:
    """Update order book file"""
    file_path = base_path.joinpath(f"{file_name}.csv")
    data_frame.to_csv(file_path)
    data_frame = load_file(file_path)
    return data_frame


@st.cache
def download_stock_data(ticker_list: list[str], start_date: date, end_date: date) -> pd.DataFrame:
    """Build pipeline to download stock prices"""
    data = yf.download(tickers=" ".join(ticker_list), start=start_date, end=end_date, group_by="column", actions=True)
    return data


# def add_ticker(ticker_de: str, ticker_us: str, currency: str, source_tax: float, db_name: str = db_path):
#     table = load_ticker_base_table().set_index("Ticker")
#     row = pd.DataFrame([{"currency": currency, "source tax": source_tax, "ticker us": ticker_us}], index=[ticker_de])
#     table = pd.concat([table, row], axis=0)
#     db_connection = sl.connect(db_name)
#     table.to_sql("ticker_base_table", db_connection, if_exists="replace", index=True, index_label="Ticker")
    
    
# def load_ticker_base_table(db_name=db_path):
#     """Load order book from database"""
#     db_connection = sl.connect(db_name)
#     return pd.read_sql(
#         f"select * from ticker_base_table", db_connection
#     ).set_index(["Ticker"])