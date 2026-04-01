# src/data_fetch.py
import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())
import yfinance as yf
import pandas as pd
from config import STOCK_SYMBOL, PERIOD, INTERVAL


def fetch_data():
    """
    Download historical stock data
    """

    df = yf.download(
        STOCK_SYMBOL,
        period=PERIOD,
        interval=INTERVAL
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.dropna(inplace=True)

    return df