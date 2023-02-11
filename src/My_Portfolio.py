import streamlit as st
from constants import ORDER_BOOK

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

# Set session state variables
if ORDER_BOOK not in st.session_state:
    st.session_state[ORDER_BOOK] = None

# Header and Intro
st.header("My Portfolio")

# Settings
order_book = st.session_state[ORDER_BOOK]
with st.sidebar:
    # Load order book
    order_book_file = st.file_uploader("Upload order book .csv file:", type=["csv"])
    if order_book_file is not None and order_book is None:
        order_book = load_file(order_book_file)
        st.session_state[ORDER_BOOK] = order_book

# Content
if order_book is not None:
    # Portfolio Balance
    portfolio_balance = calculate_portfolio_balance(
        order_book, START_DATE, END_DATE
    ).copy()
    st.plotly_chart(plot_portfolio_balance(END_DATE, portfolio_balance))
