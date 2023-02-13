from datetime import date
from io import BufferedReader
from pandas.errors import ParserError
from constants import ORDERS

import pandas as pd
import yfinance as yf
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def load_csv_file(file: UploadedFile | BufferedReader) -> pd.DataFrame:
    """Load data from csv file"""
    try:
        df = pd.read_csv(file)
    except ParserError:
        st.warning("Uploaded file is corrupted.")
        return None
    return df


def update_file(file_name: str, data_frame: pd.DataFrame) -> pd.DataFrame:
    """Update order file"""
    file_path = file_path.joinpath(f"{file_name}.csv")
    data_frame.to_csv(file_path)
    data_frame = load_csv_file(file_path)
    return data_frame


@st.cache(show_spinner=False)
def download_price_data(
    ticker_list: list[str], start_date: date, end_date: date
) -> pd.DataFrame:
    """Download stock prices"""
    data = yf.download(
        tickers=" ".join(ticker_list),
        start=start_date,
        end=end_date,
        group_by="column",
        actions=True,
    )
    return data


@st.cache(show_spinner=False)
def download_info_data(ticker: str) -> dict:
    """Download stock info"""
    try:
        return yf.Ticker(ticker).info
    except KeyError:
        return None


def load_orders(order_file: UploadedFile | BufferedReader) -> None:
    "Load order file to data frame"
    if order_file is not None and st.session_state[ORDERS] is None:
        orders = load_csv_file(order_file)
        orders["Order Date"] = pd.to_datetime(orders["Order Date"]).dt.date
        st.session_state[ORDERS] = orders
    if st.session_state[ORDERS] is not None:
        st.success("Orders available!")


def setup_sidebar() -> None:
    """Setup sidebar widgets"""
    order_file = st.file_uploader("Upload your order .csv file:", type=["csv"])
    load_example = st.button("Load example data.")
    if load_example:
        with open("files/example_orders.csv", "rb") as file:
            load_orders(file)
    else:
        load_orders(order_file)
