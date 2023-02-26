import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from math import ceil
import random
import streamlit as st
from constants import HISTORICAL_PRICES
from resources.utils import download_spinner
from resources.yahoo import download_price_data

qualitative_color_scale = px.colors.qualitative.Plotly


@st.cache_data(show_spinner=False)
def plot_portfolio_balance(end_date, portfolio_balance):
    """Plot balance of portfolio as pie chart"""
    return px.pie(
        portfolio_balance,
        values="Value",
        names="Full Name",
        title=f"Portfolio Balance at {end_date.strftime('%d-%m-%Y')}",
        width=600,
        height=600,
    )


@st.cache_data(show_spinner=False)
def plot_historic_prices(
    orders: pd.DataFrame, prices: pd.Series, ticker_name: str, full_name: str
):
    """Plot historical prices with bollinger bands"""

    color_code = {"Buy": "green", "Sell": "red"}

    ticker_history = pd.DataFrame()
    ticker_history["sma"] = prices.rolling(30).mean()
    ticker_history["std"] = prices.rolling(30).std(ddof=0)
    ticker_history["200d"] = prices.rolling(200).mean()
    ticker_history["close"] = prices

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ticker_history.index,
            y=ticker_history["200d"],
            line_color="white",
            line={"dash": "dash"},
            showlegend=False,
            name="200 Days MA",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ticker_history.index,
            y=ticker_history["sma"] + (ticker_history["std"] * 2),
            line_color="gray",
            line={"dash": "dash"},
            opacity=0.3,
            showlegend=False,
            name="Upper BB",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ticker_history.index,
            y=ticker_history["sma"] - (ticker_history["std"] * 2),
            line_color="gray",
            line={"dash": "dash"},
            fill="tonexty",
            opacity=0.3,
            showlegend=False,
            name="Lower BB",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ticker_history.index,
            y=ticker_history["close"],
            line_color=random.choice(qualitative_color_scale),
            name=ticker_name,
            showlegend=False,
        )
    )

    for _, order in orders.iterrows():
        fig.add_vline(
            x=datetime.combine(order["Order Date"], datetime.min.time()).timestamp()
            * 1000,
            line_width=1.5,
            line_dash="dash",
            line_color=color_code[order["Order Type"]],
        )

    fig.add_trace(
        go.Scatter(
            x=ticker_history.index,
            y=ticker_history["sma"],
            line_color="gray",
            showlegend=False,
            name="SMA",
        )
    )

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            ),
        ),
    )

    fig.update_layout(height=400, width=600, title_text=full_name)

    return fig


def make_grid(number_of_plots: int, cols: int = 2) -> tuple[list[int], int, int]:
    """Make plot grid"""
    rows = ceil(number_of_plots / cols)

    grid = [0] * rows
    for i in range(rows):
        with st.container():
            grid[i] = st.columns(cols)
    return grid, rows, cols


def orchestrate_price_plot(
    orders: pd.DataFrame,
    ticker_map: dict[str, str],
    start_date: datetime,
    end_date: datetime,
) -> None:
    """Orchestrate generated historical prices plots into grid"""
    filter = (orders["Order Date"] >= start_date.date()) & (
        orders["Order Date"] <= end_date.date()
    )
    filtered_orders = orders.loc[filter]
    with download_spinner(HISTORICAL_PRICES):
        historical_prices = download_price_data(list(ticker_map.keys()))
    # historical_prices.index = historical_prices.index.tz_localize(None)
    grid, rows, cols = make_grid(len(ticker_map.keys()))
    ticker_iterator = iter(ticker_map.items())

    for row in range(rows):
        for col in range(cols):
            ticker, full_name = next(ticker_iterator, (None, None))
            if ticker is None:
                continue

            grid[row][col].plotly_chart(
                plot_historic_prices(
                    filtered_orders[filtered_orders["Ticker"] == ticker],
                    historical_prices.loc[ticker, "close"],
                    ticker,
                    full_name,
                )
            )
