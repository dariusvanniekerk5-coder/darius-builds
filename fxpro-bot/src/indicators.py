"""Small, dependency-light indicator helpers (pandas/numpy only).

Kept separate from strategy logic so they can be unit-tested in isolation and
reused by any future strategy.
"""
from __future__ import annotations

import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    """Exponential moving average. `adjust=False` matches the recursive form
    used by most trading platforms (incl. MT5)."""
    if period <= 0:
        raise ValueError("EMA period must be positive")
    return series.ewm(span=period, adjust=False).mean()


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range. Expects columns: high, low, close.

    True range is max of (high-low, |high-prev_close|, |low-prev_close|);
    ATR is the Wilder-smoothed (RMA) average of that.
    """
    if not {"high", "low", "close"}.issubset(df.columns):
        raise ValueError("ATR requires high, low, close columns")
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    # Wilder smoothing == EMA with alpha = 1/period.
    return tr.ewm(alpha=1.0 / period, adjust=False).mean()


def crossed_above(fast: pd.Series, slow: pd.Series) -> bool:
    """True if `fast` crossed from at-or-below to strictly-above `slow` on the
    most recent bar."""
    if len(fast) < 2 or len(slow) < 2:
        return False
    return fast.iloc[-2] <= slow.iloc[-2] and fast.iloc[-1] > slow.iloc[-1]


def crossed_below(fast: pd.Series, slow: pd.Series) -> bool:
    """True if `fast` crossed from at-or-above to strictly-below `slow` on the
    most recent bar."""
    if len(fast) < 2 or len(slow) < 2:
        return False
    return fast.iloc[-2] >= slow.iloc[-2] and fast.iloc[-1] < slow.iloc[-1]
