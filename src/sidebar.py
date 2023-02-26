from resources.file import load_orders
import streamlit as st


def setup_sidebar() -> None:
    """Setup sidebar widgets"""
    order_file = st.file_uploader("Upload your order .csv file:", type=["csv"])
    if order_file:
        load_orders(order_file, order_file.name)
    else:
        example_orders = "example_orders.csv"
        with open(f"example_data/{example_orders}", "rb") as file:
            load_orders(file, example_orders)
