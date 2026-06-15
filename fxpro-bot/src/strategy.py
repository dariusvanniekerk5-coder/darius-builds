"""Trading strategy: a transparent EMA-crossover with a higher-timeframe trend
filter and ATR-based stops.

This is a *baseline to iterate on*, not a secret edge. It is deliberately simple
and explainable so that, combined with the journal, we can tell whether any
observed performance is a real edge or just luck.

The `Strategy` base class keeps the interface small so alternative strategies can
be dropped in later without touching the bot loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd

from . import indicators


class Direction(str, Enum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"  # no actionable signal


@dataclass
class Signal:
    direction: Direction
    # Reference price the SL/TP were computed from (last closed bar's close).
    price: float = 0.0
    stop_loss: float = 0.0
    take_profit: float = 0.0
    atr: float = 0.0
    reason: str = ""

    @property
    def is_actionable(self) -> bool:
        return self.direction in (Direction.LONG, Direction.SHORT)


class Strategy:
    """Minimal interface every strategy implements."""

    def generate(self, df: pd.DataFrame, trend_df: pd.DataFrame) -> Signal:
        raise NotImplementedError


@dataclass
class EmaCrossStrategy(Strategy):
    ema_fast: int = 12
    ema_slow: int = 26
    trend_ema: int = 50
    atr_period: int = 14
    atr_stop_mult: float = 2.0
    atr_target_mult: float = 3.0

    def generate(self, df: pd.DataFrame, trend_df: pd.DataFrame) -> Signal:
        """Decide an action from the most recent *closed* bars.

        Caller is responsible for passing OHLC frames whose last row is a closed
        bar (the bot loop only acts on bar close).
        """
        if len(df) < self.ema_slow + 2 or len(trend_df) < self.trend_ema + 1:
            return Signal(Direction.FLAT, reason="insufficient history")

        fast = indicators.ema(df["close"], self.ema_fast)
        slow = indicators.ema(df["close"], self.ema_slow)
        atr_series = indicators.atr(df, self.atr_period)

        close = float(df["close"].iloc[-1])
        atr_val = float(atr_series.iloc[-1])
        if atr_val <= 0 or pd.isna(atr_val):
            return Signal(Direction.FLAT, reason="invalid ATR")

        # Higher-timeframe trend filter: only take trades aligned with the trend.
        trend_line = indicators.ema(trend_df["close"], self.trend_ema)
        trend_close = float(trend_df["close"].iloc[-1])
        uptrend = trend_close > float(trend_line.iloc[-1])
        downtrend = trend_close < float(trend_line.iloc[-1])

        if indicators.crossed_above(fast, slow) and uptrend:
            return Signal(
                direction=Direction.LONG,
                price=close,
                stop_loss=close - self.atr_stop_mult * atr_val,
                take_profit=close + self.atr_target_mult * atr_val,
                atr=atr_val,
                reason="EMA fast crossed above slow in uptrend",
            )

        if indicators.crossed_below(fast, slow) and downtrend:
            return Signal(
                direction=Direction.SHORT,
                price=close,
                stop_loss=close + self.atr_stop_mult * atr_val,
                take_profit=close - self.atr_target_mult * atr_val,
                atr=atr_val,
                reason="EMA fast crossed below slow in downtrend",
            )

        return Signal(Direction.FLAT, price=close, atr=atr_val, reason="no aligned crossover")


def from_config(cfg: dict) -> EmaCrossStrategy:
    """Build a strategy from the `strategy:` section of config.yaml."""
    s = cfg.get("strategy", {})
    return EmaCrossStrategy(
        ema_fast=s.get("ema_fast", 12),
        ema_slow=s.get("ema_slow", 26),
        trend_ema=s.get("trend_ema", 50),
        atr_period=s.get("atr_period", 14),
        atr_stop_mult=s.get("atr_stop_mult", 2.0),
        atr_target_mult=s.get("atr_target_mult", 3.0),
    )
