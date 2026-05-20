"""
gpr.py
========================
Load and process Geopolitical Risk (GPR) index
"""

import pandas as pd
import numpy as np


# =========================================
# LOAD GPR (CSV)
# =========================================
def load_gpr(file_path):
    """
    Expect CSV with columns:
    Date, GPR
    """
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df = df.set_index("Date")
    df = df.sort_index()

    return df


# =========================================
# NORMALIZE GPR
# =========================================
def normalize_gpr(gpr):
    return (gpr - gpr.mean()) / gpr.std()


# =========================================
# ALIGN WITH RETURNS
# =========================================
def align_gpr_returns(returns, gpr):
    """
    Align GPR with returns (same time index)
    """

    # đảm bảo index là datetime
    returns = returns.copy()
    gpr = gpr.copy()

    returns.index = pd.to_datetime(returns.index)
    gpr.index = pd.to_datetime(gpr.index)

    # align theo returns
    gpr_aligned = gpr.reindex(returns.index)

    # forward fill (giữ thông tin gần nhất)
    gpr_aligned = gpr_aligned.ffill()

    # drop nếu vẫn còn NaN (đầu chuỗi)
    mask = gpr_aligned.notna().all(axis=1)

    returns = returns.loc[mask]
    gpr_aligned = gpr_aligned.loc[mask]

    return returns, gpr_aligned


# =========================================
# BUILD STATES (N / C / W)
# =========================================
def build_states(gpr):
    gpr_series = gpr["GPR"] 

    q33 = gpr_series.quantile(0.33)
    q66 = gpr_series.quantile(0.66)

    states = pd.Series(index=gpr.index, dtype="object")

    states[gpr_series < q33] = "N"
    states[(gpr_series >= q33) & (gpr_series < q66)] = "C"
    states[gpr_series >= q66] = "W"

    return states