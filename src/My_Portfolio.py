import streamlit as st
from constants import ORDERS
from portfolio.page_content import my_portfolio_content

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
    my_portfolio_content(orders)
