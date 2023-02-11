import pandas as pd
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from math import ceil
import numpy as np

from data.utils import download_stock_data

def plot_portfolio_balance(end_date, portfolio_balance):
    """"""
    return px.pie(portfolio_balance, values='Value', names='Full Name', title=f"Portfolio at {end_date.strftime('%d-%m-%Y')}", width=600, height=600)


def plot_historic_prices(start_date: datetime, end_date: datetime, order_book: pd.DataFrame, ticker_names: list[str]):
    """"""

    color_code = {"Buy": "green", "Sell": "red"}

    filter = (order_book["Order Date"] >= start_date.date()) & (order_book["Order Date"] <= end_date.date())
    orders = order_book.loc[filter].copy()

    complete_data = download_stock_data(ticker_names, start_date.date(), end_date.date()).copy()
    complete_data.index = complete_data.index.tz_localize(None)
    filter = (complete_data.index >= start_date) & (complete_data.index <= end_date)
    history = complete_data.loc[filter].copy()

    cols = 2
    rows = ceil(len(ticker_names) / cols)
    grid = np.mgrid[1: rows + 1, 1: cols + 1]
    col_index = np.ravel(grid[1])
    row_index = np.ravel(grid[0])

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=tuple(ticker_names)
    )
    fig.layout.template = "plotly_white"

    for i, ticker in enumerate(ticker_names):
        ticker_history = pd.DataFrame()
        ticker_history["sma"] = history["Close"][ticker].rolling(30).mean()
        ticker_history["std"] = history["Close"][ticker].rolling(30).std(ddof=0)
        ticker_history["close"] = history["Close"][ticker]
        ticker_history["volume"] = history["Volume"][ticker]
        
        fig.append_trace(
            go.Scatter(
                x=ticker_history.index,
                y=ticker_history["sma"] + (ticker_history["std"] * 2),
                line_color="gray",
                line = {"dash": "dash"},
                opacity = 0.3,
                showlegend=False
            ),
            row=row_index[i],
            col=col_index[i]
        )
                    
        fig.append_trace(
            go.Scatter(
                x=ticker_history.index,
                y=ticker_history["sma"] - (ticker_history["std"] * 2),
                line_color="gray",
                line = {"dash": "dash"},
                fill = 'tonexty',
                opacity = 0.3,
                showlegend=False
            ),
            row=row_index[i],
            col=col_index[i]
        )
        
        fig.append_trace(
            go.Scatter(
                x=ticker_history.index,
                y=ticker_history["close"],
                name=ticker,
                showlegend=False
            ),
            row=row_index[i],
            col=col_index[i]
        )
        
        ticker_orders = orders[orders["Ticker"]==ticker]
        for _, order in ticker_orders.iterrows():
            fig.add_vline(
                x=order["Order Date"],
                line_width=1.5,
                line_dash="dash",
                line_color=color_code[order["Order Type"]],
                row=row_index[i],
                col=col_index[i],
            )
        
        fig.append_trace(
            go.Scatter(
                x=ticker_history.index,
                y=ticker_history["sma"],
                line_color="gray",
                showlegend=False
            ),
            row=row_index[i],
            col=col_index[i]
        )

    fig.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
            )
        )

    fig.update_layout(
        height=rows*400, 
        width=cols*600, 
        title_text=""
    )

    return fig
