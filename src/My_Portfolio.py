import streamlit as st
from constants import SECTOR, ORDERS, COUNTRY
from setup import START_DATE, END_DATE
from portfolio.status import portfolio_stock_allocation, portfolio_value_development
from portfolio.graphs import plot_stock_allocation, plot_portfolio_development

from setup import register_session_state_variable
from sidebar import setup_sidebar

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
    col1, col2 = st.columns(2)
    with col1:
        portfolio_sorter = st.selectbox(
            "Sort by industry or country:", (SECTOR, COUNTRY, "None"), index=2
        )
        stock_allocation = portfolio_stock_allocation(orders, START_DATE, END_DATE)
        st.plotly_chart(
            plot_stock_allocation(stock_allocation, END_DATE, sort_by=portfolio_sorter)
        )
    with col2:
        portfolio_values, transaction_values = portfolio_value_development(
            orders, START_DATE, END_DATE
        )
        st.plotly_chart(
            plot_portfolio_development(portfolio_values, transaction_values),
            use_container_width=True,
        )
        st.info("Test")
