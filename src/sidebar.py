from data.utils import load_orders
import streamlit as st


def setup_sidebar() -> None:
    """Setup sidebar widgets"""
    order_file = st.file_uploader("Upload your order .csv file:", type=["csv"])
    load_example = st.button("Load example data.")
    if load_example:
        with open("files/example_orders.csv", "rb") as file:
            load_orders(file)
    else:
        load_orders(order_file)
