import pandas as pd
from yahooquery import Ticker
import yahooquery as yq
import streamlit as st
from resources.schemas import StockInfo
from datetime import datetime, date


@st.cache_data(show_spinner=False)
def download_price_data(ticker_list: list[str], start_date: date, end_date: date) -> pd.DataFrame:
    """Download stock prices"""
    tickers = Ticker(" ".join(ticker_list), asynchronous=True)
    price_data = tickers.history(start=start_date, end=end_date)
    price_data.index = pd.MultiIndex.from_tuples([(row[0], row[1].date()) if type(row[1])==datetime else row for row in price_data.index], names=["symbol", "date"])
    return price_data


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
