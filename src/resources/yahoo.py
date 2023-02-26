from setup import START_DATE, END_DATE
import pandas as pd
from yahooquery import Ticker
import yahooquery as yq
import streamlit as st
from resources.schemas import StockInfo, Stocks


@st.cache_data(show_spinner=False)
def download_price_data(ticker_list: list[str]) -> pd.DataFrame:
    """Download stock prices"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return tickers.history(start=START_DATE, end=END_DATE)


@st.cache_data(show_spinner=False)
def download_stock_info(ticker_list: pd.Series) -> StockInfo:
    """Download stock info"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    return {
        ticker: StockInfo(**stock_info)
        for ticker, stock_info in tickers.all_modules.items()
    }


@st.cache_data(show_spinner=False)
def download_isin_tickers(isin_list: pd.Series) -> pd.Series:
    """Download ticker based on ISIN codes"""
    return isin_list.apply(lambda isin: yq.search(isin, first_quote=True)["symbol"])
