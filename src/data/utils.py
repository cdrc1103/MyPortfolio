from datetime import date
from pandas.errors import ParserError
from constants import ORDER_BOOK

import pandas as pd
import yfinance as yf
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def load_file(file: UploadedFile) -> pd.DataFrame:
    """Load order book from file"""
    try:
        order_book = pd.read_csv(file)
    except ParserError:
        st.warning("Uploaded file is corrupted.")
        return None

    order_book["Order Date"] = pd.to_datetime(order_book["Order Date"]).dt.date
    return order_book


def update_file(file_name: str, data_frame: pd.DataFrame) -> pd.DataFrame:
    """Update order book file"""
    file_path = file_path.joinpath(f"{file_name}.csv")
    data_frame.to_csv(file_path)
    data_frame = load_file(file_path)
    return data_frame


@st.cache(show_spinner=False)
def download_stock_data(
    ticker_list: list[str], start_date: date, end_date: date
) -> pd.DataFrame:
    """Build pipeline to download stock prices"""
    data = yf.download(
        tickers=" ".join(ticker_list),
        start=start_date,
        end=end_date,
        group_by="column",
        actions=True,
    )
    return data


def load_order_book() -> None:
    "Load order book file to data frame"
    order_book_file = st.file_uploader("Upload order book .csv file:", type=["csv"])
    if order_book_file is not None and st.session_state[ORDER_BOOK] is None:
        st.session_state[ORDER_BOOK] = load_file(order_book_file)
    if st.session_state[ORDER_BOOK] is not None:
        st.success("Order book available")
