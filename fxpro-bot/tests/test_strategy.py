"""Strategy + indicator tests. No MetaTrader5 needed."""
import numpy as np
import pandas as pd

from src import indicators
from src.strategy import Direction, EmaCrossStrategy


def build_df(closes, spread=0.0010):
    """OHLC frame from a list of closes, with a fixed high/low spread so ATR>0."""
    closes = np.asarray(closes, dtype=float)
    return pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=len(closes), freq="15min", tz="UTC"),
        "open": closes,
        "high": closes + spread,
        "low": closes - spread,
        "close": closes,
    })


def test_crossed_above_and_below():
    # fast equals slow then jumps above on the last bar -> crossed_above
    fast = pd.Series([1.0, 1.0, 1.5])
    slow = pd.Series([1.0, 1.0, 1.0])
    assert indicators.crossed_above(fast, slow)
    assert not indicators.crossed_below(fast, slow)

    fast_d = pd.Series([1.0, 1.0, 0.5])
    assert indicators.crossed_below(fast_d, slow)
    assert not indicators.crossed_above(fast_d, slow)


def test_atr_positive_with_spread():
    df = build_df([1.10] * 20)
    a = indicators.atr(df, 14)
    assert a.iloc[-1] > 0


def test_long_signal_on_upcross_in_uptrend():
    strat = EmaCrossStrategy(ema_fast=3, ema_slow=10, trend_ema=5, atr_period=3)
    # flat then a jump up on the final bar -> fast crosses above slow
    entry = build_df([1.1000] * 30 + [1.1080])
    # gently rising higher timeframe -> last close above its EMA -> uptrend
    trend = build_df(list(np.linspace(1.0900, 1.1200, 30)))

    sig = strat.generate(entry, trend)
    assert sig.direction == Direction.LONG
    assert sig.stop_loss < sig.price < sig.take_profit
    assert sig.atr > 0


def test_short_signal_on_downcross_in_downtrend():
    strat = EmaCrossStrategy(ema_fast=3, ema_slow=10, trend_ema=5, atr_period=3)
    entry = build_df([1.1000] * 30 + [1.0920])
    trend = build_df(list(np.linspace(1.1200, 1.0900, 30)))  # falling

    sig = strat.generate(entry, trend)
    assert sig.direction == Direction.SHORT
    assert sig.take_profit < sig.price < sig.stop_loss


def test_no_signal_when_flat():
    strat = EmaCrossStrategy(ema_fast=3, ema_slow=10, trend_ema=5, atr_period=3)
    entry = build_df([1.1000] * 31)
    trend = build_df([1.1000] * 30)
    assert strat.generate(entry, trend).direction == Direction.FLAT


def test_flat_on_insufficient_history():
    strat = EmaCrossStrategy(ema_fast=3, ema_slow=10)
    entry = build_df([1.1] * 5)
    trend = build_df([1.1] * 5)
    sig = strat.generate(entry, trend)
    assert sig.direction == Direction.FLAT
    assert "insufficient" in sig.reason


def test_upcross_ignored_against_trend():
    # bullish crossover but higher timeframe is in a downtrend -> no long
    strat = EmaCrossStrategy(ema_fast=3, ema_slow=10, trend_ema=5, atr_period=3)
    entry = build_df([1.1000] * 30 + [1.1080])
    trend = build_df(list(np.linspace(1.1200, 1.0900, 30)))  # downtrend
    assert strat.generate(entry, trend).direction == Direction.FLAT
