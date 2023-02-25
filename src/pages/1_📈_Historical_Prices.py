import streamlit as st
from portfolio.page_content import historical_prices_content
from setup import register_session_state_variable
from constants import ORDERS
from sidebar import setup_sidebar

# Page config
st.set_page_config(
    page_title="Historical Prices",
    layout="wide",
)

# Set session state variables
register_session_state_variable(ORDERS)

# Header and Intro
st.header("Historical Prices")

# Sidebar
with st.sidebar:
    setup_sidebar()

# Content
orders = st.session_state[ORDERS]
if orders is not None:
    historical_prices_content(orders)
