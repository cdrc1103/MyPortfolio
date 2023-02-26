from io import BufferedReader
from pandas.errors import ParserError
from typing import Iterator

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def load_csv_file(file: UploadedFile | BufferedReader) -> pd.DataFrame:
    """Load data from csv file"""
    try:
        df = pd.read_csv(file)
    except ParserError:
        st.warning("Uploaded file is corrupted.")
        return None
    return df


def download_spinner(resource_name: str) -> Iterator[None]:
    """Generate resource specific spinner object"""
    return st.spinner(f"Downloading {resource_name}...")
