import streamlit as st
from constants import SECTOR, ORDERS, COUNTRY
from setup import START_DATE, END_DATE
from portfolio.status import calculate_portfolio_balance
from portfolio.graphs import plot_portfolio_balance

from setup import register_session_state_variable
from sidebar import setup_sidebar
from constants import ORDERS

# Page config
st.set_page_config(
    page_title="My Portfolio",
    layout="wide",
)

# Set session state variables
register_session_state_variable(ORDERS)

# Header and Intro
st.header("My Portfolio")

# Sidebar
with st.sidebar:
    setup_sidebar()

# Content
orders = st.session_state[ORDERS]
if orders is not None:
    portfolio_sorter = st.selectbox("Sort by industry or country:", (SECTOR, COUNTRY, "None"))
    portfolio_balance = calculate_portfolio_balance(orders, START_DATE, END_DATE).copy()
    st.plotly_chart(plot_portfolio_balance(portfolio_balance, END_DATE, sort_by=portfolio_sorter))
