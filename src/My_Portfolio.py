import streamlit as st
from constants import ORDERS

from settings import START_DATE, END_DATE
from data.utils import setup_sidebar
from constants import ORDERS
from portfolio.status import calculate_portfolio_balance
from portfolio.graphs import plot_portfolio_balance

# Page config
st.set_page_config(
    page_title="My Portfolio",
    layout="wide",
)

# Set session state variables
if ORDERS not in st.session_state:
    st.session_state[ORDERS] = None

# Header and Intro
st.header("My Portfolio")

# Sidebar
with st.sidebar:
    setup_sidebar()


# Content
orders = st.session_state[ORDERS]
if orders is not None:
    # Portfolio Balance
    portfolio_balance = calculate_portfolio_balance(orders, START_DATE, END_DATE).copy()
    st.plotly_chart(plot_portfolio_balance(END_DATE, portfolio_balance))
