from setup import START_DATE, END_DATE
import pandas as pd
from yahooquery import Ticker
import yahooquery as yq
import streamlit as st
from resources.schemas import Stocks


@st.cache_data(show_spinner=False)
def download_price_data(ticker_list: list[str]) -> pd.DataFrame:
    """Download stock prices"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return tickers.history(start=START_DATE, end=END_DATE)


@st.cache_data(show_spinner=False)
def download_stock_info(ticker_list: list[str]) -> Stocks:
    """Download stock info"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return Stocks(**tickers.all_modules)


@st.cache_data(show_spinner=False)
def download_isin_tickers(isin_list: list[str]) -> dict[str, str]:
    """Download ticker based on ISIN codes"""
    return {isin: yq.search(isin, first_quote=True)["symbol"] for isin in isin_list}
