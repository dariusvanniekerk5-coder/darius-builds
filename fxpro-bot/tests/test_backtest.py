"""Backtest engine tests. No MetaTrader5 needed."""
import numpy as np
import pandas as pd

from src import backtest, risk, strategy
from src.backtest import (CostModel, Position, SymbolSpec, check_exit,
                          make_synthetic, resample_ohlc, run_backtest, trade_pnl)
from src.strategy import Direction, EmaCrossStrategy, Signal

SPEC = SymbolSpec(tick_size=0.00001, tick_value=1.0, volume_step=0.01,
                  volume_min=0.01, volume_max=100.0)
NO_COST = CostModel(spread=0.0, commission_per_lot=0.0)


def _df(closes, spread=0.0002, freq="15min"):
    closes = np.asarray(closes, dtype=float)
    return pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=len(closes), freq=freq, tz="UTC"),
        "open": closes,
        "high": closes + spread,
        "low": closes - spread,
        "close": closes,
    })


# --- exit logic ---
def test_check_exit_long_tp_and_sl():
    pos = Position(Direction.LONG, entry=1.10, stop_loss=1.09, take_profit=1.12,
                   lots=0.1, entry_time=pd.Timestamp("2024-01-01", tz="UTC"))
    assert check_exit(pos, high=1.125, low=1.10) == (1.12, "tp")
    assert check_exit(pos, high=1.11, low=1.085) == (1.09, "sl")
    assert check_exit(pos, high=1.115, low=1.095) is None
    # both touched in one bar -> stop assumed first (pessimistic)
    assert check_exit(pos, high=1.13, low=1.08) == (1.09, "sl")


def test_check_exit_short():
    pos = Position(Direction.SHORT, entry=1.10, stop_loss=1.11, take_profit=1.08,
                   lots=0.1, entry_time=pd.Timestamp("2024-01-01", tz="UTC"))
    assert check_exit(pos, high=1.10, low=1.075) == (1.08, "tp")
    assert check_exit(pos, high=1.115, low=1.10) == (1.11, "sl")
    assert check_exit(pos, high=1.12, low=1.07) == (1.11, "sl")  # both -> sl


# --- pnl math ---
def test_trade_pnl_long_and_short():
    # long 0.0010 (10 pip) gain on 1 lot EURUSD -> ~$100
    assert trade_pnl(Direction.LONG, 1.1000, 1.1010, 1.0, SPEC, NO_COST) == \
        __import__("pytest").approx(100.0)
    # short profits when price falls
    assert trade_pnl(Direction.SHORT, 1.1000, 1.0990, 1.0, SPEC, NO_COST) == \
        __import__("pytest").approx(100.0)


def test_trade_pnl_applies_costs():
    gross = trade_pnl(Direction.LONG, 1.1000, 1.1010, 1.0, SPEC, NO_COST)
    netted = trade_pnl(Direction.LONG, 1.1000, 1.1010, 1.0, SPEC,
                       CostModel(spread=0.00010, commission_per_lot=5.0))
    # spread 1 pip ~= $10, plus $5 commission -> ~$15 less
    assert netted == __import__("pytest").approx(gross - 15.0)


# --- resample / no-lookahead ---
def test_resample_ohlc_aggregates():
    df = _df(list(range(8)), spread=0.5, freq="15min")  # 8 M15 bars = 2 H1 bars
    h1 = resample_ohlc(df, "H1")
    assert len(h1) == 2
    # first H1 bar aggregates the first four M15 bars (closes 0..3)
    assert h1["open"].iloc[0] == 0
    assert h1["close"].iloc[0] == 3
    assert h1["high"].iloc[0] == 3 + 0.5
    assert h1["low"].iloc[0] == 0 - 0.5


def test_trend_close_time_prevents_lookahead():
    # The H1 bar covering 00:00-01:00 must NOT be usable as "closed" for an M15
    # decision made within that hour.
    df = _df(list(range(8)), spread=0.5, freq="15min")
    h1 = resample_ohlc(df, "H1")
    from src import timeframes
    h1["close_time"] = h1["time"] + timeframes.duration("H1")
    decision = df["time"].iloc[1] + timeframes.duration("M15")  # 00:30 close = decision
    usable = h1[h1["close_time"] <= decision]
    assert len(usable) == 0  # first H1 bar only closes at 01:00, after the decision


# --- end to end ---
class _StubStrategy(strategy.Strategy):
    """Fires one LONG signal the first time it sees >= `fire_at_len` bars, with
    fixed SL/TP. Lets us test the engine's fill/exit/P&L path deterministically,
    independent of EMA-crossover timing (which is covered in test_strategy.py)."""

    def __init__(self, fire_at_len, stop_loss, take_profit):
        self.fire_at_len = fire_at_len
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.fired = False

    def generate(self, df, trend_df):
        if not self.fired and len(df) >= self.fire_at_len:
            self.fired = True
            return Signal(Direction.LONG, price=float(df["close"].iloc[-1]),
                          stop_loss=self.stop_loss, take_profit=self.take_profit,
                          atr=0.001, reason="stub")
        return Signal(Direction.FLAT)


def test_run_backtest_winning_trade_via_engine():
    # Rising prices: a long opened mid-series rides up to its take-profit.
    df = _df(list(np.linspace(1.1000, 1.1300, 60)), spread=0.0001)
    # fires ~bar 19 (price ~1.1097, filled ~1.1102): stop below, target above.
    strat = _StubStrategy(fire_at_len=20, stop_loss=1.0950, take_profit=1.1250)
    res = run_backtest(
        df, strat=strat, risk_cfg=risk.RiskConfig(daily_max_loss_pct=100.0),
        entry_tf="M15", trend_tf="H1", spec=SPEC, costs=NO_COST,
        initial_balance=10_000, risk_pct=0.5, warmup=300)
    assert res.metrics.closed_trades == 1
    assert res.metrics.wins == 1
    assert res.metrics.net_profit > 0
    assert res.trades[0]["reason"] == "tp"
    # equity bookkeeping is consistent with reported net profit
    assert res.final_equity == __import__("pytest").approx(
        res.initial_balance + res.metrics.net_profit)


def test_run_backtest_losing_trade_via_engine():
    # Falling prices: the same long gets stopped out.
    df = _df(list(np.linspace(1.1000, 1.0700, 60)), spread=0.0001)
    # fires ~bar 19 (price ~1.0903, filled ~1.0898): stop below, target above.
    strat = _StubStrategy(fire_at_len=20, stop_loss=1.0800, take_profit=1.1100)
    res = run_backtest(
        df, strat=strat, risk_cfg=risk.RiskConfig(daily_max_loss_pct=100.0),
        entry_tf="M15", trend_tf="H1", spec=SPEC, costs=NO_COST,
        initial_balance=10_000, risk_pct=0.5, warmup=300)
    assert res.metrics.closed_trades == 1
    assert res.metrics.losses == 1
    assert res.metrics.net_profit < 0
    assert res.trades[0]["reason"] == "sl"


def test_run_backtest_runs_on_synthetic():
    # The REAL strategy integrates and produces trades on a (fixed-seed) series.
    df = make_synthetic(1500, seed=7)
    res = run_backtest(
        df, strat=EmaCrossStrategy(), risk_cfg=risk.RiskConfig(),
        entry_tf="M15", trend_tf="H1", spec=SPEC,
        costs=CostModel(spread=0.00010), initial_balance=10_000,
        risk_pct=0.5, warmup=300)
    assert res.metrics.closed_trades >= 1
    # Bookkeeping is consistent. We do NOT assert a profit sign — a random walk has
    # no edge, so any P/L here is luck of the seed, not skill.
    assert res.final_equity == __import__("pytest").approx(
        res.initial_balance + res.metrics.net_profit)
    assert np.isfinite(res.final_equity)
