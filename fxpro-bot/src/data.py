"""Market data access: pull OHLC bars from MT5 into pandas DataFrames.

Imports MetaTrader5 (Windows + running terminal). The DataFrame shape it returns
(columns: time, open, high, low, close, tick_volume, ...) is what strategy.py
expects.
"""
from __future__ import annotations

import pandas as pd
import MetaTrader5 as mt5  # type: ignore

# Map config timeframe strings to MT5 constants.
TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}


def timeframe(name: str) -> int:
    try:
        return TIMEFRAMES[name.upper()]
    except KeyError:
        raise ValueError(
            f"Unknown timeframe '{name}'. Use one of {sorted(TIMEFRAMES)}."
        )


def get_bars(symbol: str, tf_name: str, count: int) -> pd.DataFrame:
    """Return the most recent `count` *closed* bars as a DataFrame.

    MT5's copy_rates_from_pos with start=1 skips the still-forming current bar,
    so every row returned is a closed bar — important for deterministic signals.
    """
    rates = mt5.copy_rates_from_pos(symbol, timeframe(tf_name), 1, count)
    if rates is None or len(rates) == 0:
        raise RuntimeError(
            f"No rates for {symbol} {tf_name}: {mt5.last_error()}. "
            "Is the symbol visible in Market Watch?"
        )
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    return df


def last_closed_bar_time(symbol: str, tf_name: str) -> pd.Timestamp:
    """Timestamp of the most recent closed bar — used to detect a new bar."""
    df = get_bars(symbol, tf_name, 1)
    return df["time"].iloc[-1]
