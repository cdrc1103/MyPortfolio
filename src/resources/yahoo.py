from setup import START_DATE, END_DATE
import pandas as pd
from yahooquery import Ticker
import streamlit as st


@st.cache_data(show_spinner=False)
def download_price_data(ticker_list: list[str]) -> pd.DataFrame:
    """Download stock prices"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return tickers.history(start=START_DATE, end=END_DATE)
