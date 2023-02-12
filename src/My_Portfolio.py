import streamlit as st
from constants import ORDER_BOOK

from style import max_page_width, streamlit_style
from settings import START_DATE, END_DATE
from data.utils import load_file, load_order_book
from constants import ORDER_BOOK
from portfolio.status import calculate_portfolio_balance
from portfolio.graphs import plot_portfolio_balance

# Page config
st.set_page_config(
    page_title="My Portfolio",
    layout="wide",
)

# Set session state variables
if ORDER_BOOK not in st.session_state:
    st.session_state[ORDER_BOOK] = None

# Header and Intro
st.header("My Portfolio")

# Sidebar
with st.sidebar:
    load_order_book()


# Content
order_book = st.session_state[ORDER_BOOK]
if order_book is not None:
    # Portfolio Balance
    portfolio_balance = calculate_portfolio_balance(
        order_book, START_DATE, END_DATE
    ).copy()
    st.plotly_chart(plot_portfolio_balance(END_DATE, portfolio_balance))
