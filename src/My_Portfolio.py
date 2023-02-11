import streamlit as st
import plotly.express as px
from constants import ORDER_BOOK
from datetime import datetime

from style import max_page_width, streamlit_style
from settings import START_DATE
from data.utils import load_file
from portfolio.status import calculate_portfolio_balance

END_DATE = datetime.today().date()

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

with st.sidebar:
    # Load order book
    order_book_file = st.file_uploader("Upload order_book.csv")
    if order_book_file is not None:
        order_book = load_file(order_book_file)
        st.session_state[ORDER_BOOK] = order_book


if order_book is not None:

    # Portfolio Balance
    portfolio_balance = calculate_portfolio_balance(order_book, START_DATE, END_DATE)
    fig = px.pie(portfolio_balance, values='Value', names='Full Name', title=f"Portfolio at {END_DATE.strftime('%d-%m-%Y')}", width=600, height=600)
    st.plotly_chart(fig)
