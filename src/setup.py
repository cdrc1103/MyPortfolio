from datetime import datetime
import streamlit as st

START_DATE = datetime(2020, 1, 1)
END_DATE = datetime.today()


def register_session_state_variable(variable_name: str) -> None:
    """Register session state variable with None value"""
    if variable_name not in st.session_state:
        st.session_state[variable_name] = None
