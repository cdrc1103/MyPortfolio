from io import BufferedReader
from constants import ORDERS
from resources.utils import load_csv_file
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def load_orders(order_file: UploadedFile | BufferedReader, filename: str) -> None:
    "Load order file to data frame"
    if order_file is not None:
        orders = load_csv_file(order_file)
        orders["Order Date"] = pd.to_datetime(orders["Order Date"]).dt.date
        st.session_state[ORDERS] = orders
    if st.session_state[ORDERS] is not None:
        st.success(f"{filename} loaded!")
