"""Pure timeframe metadata: canonical names -> pandas resample frequency and
bar duration. No MetaTrader5 import, so it's usable in the backtester and tests.

(data.py keeps its own name->MT5-constant map separately, since that one needs
the MetaTrader5 package.)
"""
from __future__ import annotations

from datetime import timedelta

PANDAS_FREQ = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1h",
    "H4": "4h",
    "D1": "1D",
}

DURATION = {
    "M1": timedelta(minutes=1),
    "M5": timedelta(minutes=5),
    "M15": timedelta(minutes=15),
    "M30": timedelta(minutes=30),
    "H1": timedelta(hours=1),
    "H4": timedelta(hours=4),
    "D1": timedelta(days=1),
}


def freq(name: str) -> str:
    try:
        return PANDAS_FREQ[name.upper()]
    except KeyError:
        raise ValueError(f"Unknown timeframe '{name}'. Use one of {sorted(PANDAS_FREQ)}.")


def duration(name: str) -> timedelta:
    try:
        return DURATION[name.upper()]
    except KeyError:
        raise ValueError(f"Unknown timeframe '{name}'. Use one of {sorted(DURATION)}.")
