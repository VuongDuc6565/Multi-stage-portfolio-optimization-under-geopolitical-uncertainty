"""
data.py
========================
Robust data pipeline for portfolio optimization thesis

Features:
- Download multi-asset data (yfinance)
- Retry & fallback for network issues
- Clean & align time series
- Compute returns
- Optional normalization
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time

# =========================================
# CONFIG
# =========================================
DEFAULT_TICKERS = [
    "VTI", "IWM", "AGG", "LQD", "MUB", "DBC", "GLD"
]

START_DATE = "2010-01-01"
END_DATE   = "2024-06-30"

MAX_RETRIES = 3
SLEEP_TIME = 2


# =========================================
# DOWNLOAD SINGLE TICKER (ROBUST)
# =========================================
def download_single(ticker, start, end):
    for attempt in range(MAX_RETRIES):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,
                progress=False,
                threads=False
            )

            if df.empty:
                raise ValueError("Empty dataframe")

            # Safe extraction
            if "Close" in df.columns:
                series = df["Close"]
            elif "Adj Close" in df.columns:
                series = df["Adj Close"]
            else:
                raise KeyError("No Close column")

            series.name = ticker
            return series

        except Exception as e:
            print(f"[WARN] {ticker} attempt {attempt+1} failed: {e}")
            time.sleep(SLEEP_TIME)

    print(f"[ERROR] Failed completely: {ticker}")
    return None


# =========================================
# DOWNLOAD ALL TICKERS
# =========================================
def download_prices(tickers=DEFAULT_TICKERS,
                    start=START_DATE,
                    end=END_DATE):

    prices_list = []

    for ticker in tickers:
        series = download_single(ticker, start, end)

        if series is not None:
            prices_list.append(series)

    if not prices_list:
        raise ValueError("No data downloaded. Check internet or tickers.")

    prices = pd.concat(prices_list, axis=1)

    return prices


# =========================================
# CLEAN DATA
# =========================================
def clean_data(prices: pd.DataFrame):
    prices = prices.sort_index()

    # forward fill (holiday mismatch)
    prices = prices.ffill()

    # drop NaN
    prices = prices.dropna(how="any")

    return prices


# =========================================
# RETURNS
# =========================================
def compute_returns(prices: pd.DataFrame, method="log"):
    if method == "log":
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()

    return returns.dropna()


# =========================================
# NORMALIZATION
# =========================================
def normalize(data: pd.DataFrame):
    return (data - data.mean()) / data.std()


# =========================================
# FULL PIPELINE
# =========================================
def load_data(tickers=DEFAULT_TICKERS,
              start=START_DATE,
              end=END_DATE,
              normalize_data=False):

    prices = download_prices(tickers, start, end)
    prices = clean_data(prices)

    returns = compute_returns(prices)

    if normalize_data:
        returns = normalize(returns)

    return prices, returns


# =========================================
# QUICK TEST
# =========================================
if __name__ == "__main__":
    prices, returns = load_data()

    print("=== PRICES ===")
    print(prices.head())

    print("\n=== RETURNS ===")
    print(returns.head())

    print("\nShape:", returns.shape)
    