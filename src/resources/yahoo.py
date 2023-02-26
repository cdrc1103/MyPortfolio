from setup import START_DATE, END_DATE
import pandas as pd
from yahooquery import Ticker
import streamlit as st
from resources.schemas import StockInfo


@st.cache_data(show_spinner=False)
def download_price_data(ticker_list: list[str]) -> pd.DataFrame:
    """Download stock prices"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return tickers.history(start=START_DATE, end=END_DATE)


@st.cache_data(show_spinner=False)
def download_stock_info(ticker_list: list[str]) -> StockInfo:
    """Download stock info"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return StockInfo(**tickers.all_modules)
