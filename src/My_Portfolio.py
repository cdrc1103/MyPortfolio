import streamlit as st

from datetime import datetime

from style import max_page_width, streamlit_style
from settings import START_DATE, END_DATE
from data.utils import load_file
from constants import ORDER_BOOK
from portfolio.status import calculate_portfolio_balance
from portfolio.graphs import plot_portfolio_balance

# Page config
st.set_page_config(
    page_title="My Portfolio",
    layout="wide",
)
st.markdown(streamlit_style(), unsafe_allow_html=True)
st.markdown(max_page_width("1400"), unsafe_allow_html=True)


# Header and Intro
st.header("My Portfolio")

# Load order book
order_book = load_file(ORDER_BOOK)

# Portfolio Balance
portfolio_balance = calculate_portfolio_balance(order_book, START_DATE, END_DATE)
st.plotly_chart(plot_portfolio_balance(END_DATE, portfolio_balance))