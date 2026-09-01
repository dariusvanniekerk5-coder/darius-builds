"""Backtester: replay historical bars through the SAME strategy + risk + scorecard
code the live bot uses, so a strategy can be validated before it touches the demo
account.

Design notes (this is where backtests usually lie to you — so we're explicit):

  * No lookahead on signals: at each bar we only feed the strategy bars that have
    already closed, and the higher-timeframe trend only includes trend bars whose
    period has fully closed by the decision time.
  * No lookahead on fills: an entry signal at the close of bar i is filled at the
    OPEN of bar i+1 (you can't trade at a price you only knew after the bar closed).
  * Pessimistic intrabar exits: if a single bar's range touches both the stop and
    the target, we assume the STOP was hit first.
  * Costs are modeled: a configurable spread and per-lot commission are charged on
    every round trip.
  * Same code path: strategy signals, position sizing, the daily-loss kill switch,
    and the metrics all come from src/strategy.py, src/risk.py and src/journal.py.

Past performance does not predict future results. A good backtest is necessary, not
sufficient.

Run:
    python -m src.backtest --synthetic 5000          # quick smoke test, no data file
    python -m src.backtest --csv path/to/EURUSD_M15.csv
    python -m src.backtest --from-mt5 --bars 20000   # pull history from MT5 (Windows)
"""
from __future__ import annotations

import argparse
import csv as csv_mod
from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import journal, risk, strategy, timeframes
from .config import load_config
from .news import overlay as news_overlay
from .strategy import Direction


@dataclass
class SymbolSpec:
    tick_size: float = 0.00001
    tick_value: float = 1.0       # account-currency value of one tick for 1.0 lot
    volume_step: float = 0.01
    volume_min: float = 0.01
    volume_max: float = 100.0


@dataclass
class CostModel:
    spread: float = 0.00010            # price spread, charged once per round trip
    commission_per_lot: float = 0.0    # account currency per lot, round trip


@dataclass
class Position:
    direction: Direction
    entry: float
    stop_loss: float
    take_profit: float
    lots: float
    entry_time: pd.Timestamp


@dataclass
class BacktestResult:
    metrics: journal.Metrics
    trades: list[dict]
    equity_curve: list[tuple]
    initial_balance: float
    final_equity: float

    @property
    def total_return_pct(self) -> float:
        if self.initial_balance <= 0:
            return 0.0
        return (self.final_equity - self.initial_balance) / self.initial_balance * 100.0


# --- data ------------------------------------------------------------------
def resample_ohlc(df: pd.DataFrame, tf_name: str) -> pd.DataFrame:
    """Aggregate a lower-timeframe OHLC frame up to `tf_name`. Bar timestamp is the
    period START (MT5 convention)."""
    s = df.set_index("time").sort_index()
    out = (
        s.resample(timeframes.freq(tf_name), label="left", closed="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    return out.reset_index()


def load_csv(path: str) -> pd.DataFrame:
    """Load OHLC from CSV. Requires columns time, open, high, low, close
    (case-insensitive); extra columns are ignored."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    required = {"time", "open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}")
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df[list(required)].sort_values("time").reset_index(drop=True)


def make_synthetic(n: int = 5000, seed: int = 42, start_price: float = 1.1000,
                   tf: str = "M15") -> pd.DataFrame:
    """A reproducible random-walk price series. It has NO real edge by
    construction — useful to confirm the harness works and to show that a
    no-edge strategy nets out slightly negative after costs (an honest baseline)."""
    rng = np.random.default_rng(seed)
    close = start_price + np.cumsum(rng.normal(0, 0.0006, size=n))
    open_ = np.concatenate([[start_price], close[:-1]])
    high = np.maximum(open_, close) + np.abs(rng.normal(0, 0.0003, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(0, 0.0003, n))
    times = pd.date_range("2024-01-01", periods=n, freq=timeframes.freq(tf), tz="UTC")
    return pd.DataFrame({"time": times, "open": open_, "high": high, "low": low,
                         "close": close})


# --- simulation primitives -------------------------------------------------
def check_exit(pos: Position, high: float, low: float):
    """Return (exit_price, reason) if this bar's range hits the stop or target,
    else None. If both are touched in one bar, the STOP is assumed hit first."""
    if pos.direction == Direction.LONG:
        if low <= pos.stop_loss:
            return pos.stop_loss, "sl"
        if high >= pos.take_profit:
            return pos.take_profit, "tp"
    else:  # SHORT
        if high >= pos.stop_loss:
            return pos.stop_loss, "sl"
        if low <= pos.take_profit:
            return pos.take_profit, "tp"
    return None


def trade_pnl(direction: Direction, entry: float, exit_price: float, lots: float,
              spec: SymbolSpec, costs: CostModel) -> float:
    """Round-trip P/L in account currency, net of spread and commission."""
    diff = (exit_price - entry) if direction == Direction.LONG else (entry - exit_price)
    gross = (diff / spec.tick_size) * spec.tick_value * lots
    spread_cost = (costs.spread / spec.tick_size) * spec.tick_value * lots
    return gross - spread_cost - costs.commission_per_lot * lots


# --- engine ----------------------------------------------------------------
def run_backtest(
    df: pd.DataFrame,
    *,
    strat: strategy.Strategy,
    risk_cfg: risk.RiskConfig,
    entry_tf: str,
    trend_tf: str,
    spec: SymbolSpec,
    costs: CostModel,
    initial_balance: float,
    risk_pct: float,
    warmup: int = 300,
    symbol: str = "EURUSD",
    news_provider=None,
    news_cfg=None,
) -> BacktestResult:
    df = df.sort_values("time").reset_index(drop=True)
    news_on = news_provider is not None and news_cfg is not None and news_cfg.enabled
    currencies = news_overlay.currencies_for(symbol) if news_on else set()
    trend_full = resample_ohlc(df, trend_tf)
    trend_full["close_time"] = trend_full["time"] + timeframes.duration(trend_tf)
    entry_dur = timeframes.duration(entry_tf)

    rm = risk.RiskManager(risk_cfg)
    equity = initial_balance
    pos: Position | None = None
    trades: list[dict] = []
    profits: list[float] = []
    equity_curve = [(df["time"].iloc[0], equity)]

    n = len(df)
    for i in range(n):
        bar = df.iloc[i]
        t = bar["time"]

        # 1) manage an open position against THIS bar's range.
        if pos is not None:
            ex = check_exit(pos, float(bar["high"]), float(bar["low"]))
            if ex is not None:
                exit_price, reason = ex
                pnl = trade_pnl(pos.direction, pos.entry, exit_price, pos.lots,
                                spec, costs)
                equity += pnl
                profits.append(pnl)
                trades.append({
                    "direction": pos.direction.value,
                    "entry_time": pos.entry_time.isoformat(),
                    "exit_time": t.isoformat(),
                    "entry": round(pos.entry, 5),
                    "exit": round(exit_price, 5),
                    "lots": pos.lots,
                    "reason": reason,
                    "pnl": round(pnl, 2),
                    "equity": round(equity, 2),
                })
                equity_curve.append((t, equity))
                pos = None

        # 2) if flat, decide at this bar's close; fill at the NEXT bar's open.
        if pos is None and i + 1 < n:
            decision_time = t + entry_dur
            rm.mark_day(t.to_pydatetime(), equity)
            entry_slice = df.iloc[max(0, i + 1 - warmup): i + 1]
            trend_slice = trend_full[trend_full["close_time"] <= decision_time].tail(warmup)
            sig = strat.generate(entry_slice, trend_slice)
            # News overlay (same logic as the live bot): can only veto, replayed
            # deterministically from the CSV calendar + sentiment cache.
            if news_on and sig.is_actionable:
                at = decision_time.to_pydatetime()
                event_risk = news_provider.event_risk(currencies, at)
                sentiment = news_provider.sentiment(symbol, at)
                sig, _ = news_overlay.apply_news(sig, event_risk, sentiment, news_cfg)
            if sig.is_actionable:
                allowed, _ = rm.can_open_new(
                    equity=equity, open_positions_total=0, open_positions_symbol=0)
                if allowed:
                    lots = risk.position_size(
                        equity=equity, risk_pct=risk_pct,
                        entry=sig.price, stop_loss=sig.stop_loss,
                        tick_size=spec.tick_size, tick_value=spec.tick_value,
                        volume_step=spec.volume_step, volume_min=spec.volume_min,
                        volume_max=spec.volume_max)
                    if lots > 0:
                        nxt = df.iloc[i + 1]
                        pos = Position(
                            direction=sig.direction, entry=float(nxt["open"]),
                            stop_loss=sig.stop_loss, take_profit=sig.take_profit,
                            lots=lots, entry_time=nxt["time"])

    return BacktestResult(
        metrics=journal.compute_metrics(profits),
        trades=trades, equity_curve=equity_curve,
        initial_balance=initial_balance, final_equity=equity)


# --- config glue + CLI -----------------------------------------------------
def spec_from_config(cfg: dict) -> SymbolSpec:
    b = cfg.get("backtest", {})
    return SymbolSpec(
        tick_size=b.get("tick_size", 0.00001),
        tick_value=b.get("tick_value", 1.0),
        volume_step=cfg.get("risk", {}).get("min_lot", 0.01),
        volume_min=cfg.get("risk", {}).get("min_lot", 0.01),
        volume_max=cfg.get("risk", {}).get("max_lot", 100.0),
    )


def costs_from_config(cfg: dict) -> CostModel:
    b = cfg.get("backtest", {})
    return CostModel(
        spread=b.get("spread", 0.00010),
        commission_per_lot=b.get("commission_per_lot", 0.0),
    )


def _load_from_mt5(symbol: str, tf: str, bars: int) -> pd.DataFrame:
    """Pull recent closed bars from a running MT5 terminal (Windows). Imported
    lazily so the rest of the backtester works without MetaTrader5 installed."""
    from . import connection, data
    from .config import load_credentials
    connection.connect(load_credentials())
    try:
        return data.get_bars(symbol, tf, bars)
    finally:
        connection.shutdown()


def _write_csv(path: str, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv_mod.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description="Backtest the strategy on historical data")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="path to an OHLC CSV (time,open,high,low,close)")
    src.add_argument("--synthetic", type=int, metavar="N",
                     help="generate N bars of reproducible random-walk data")
    src.add_argument("--from-mt5", action="store_true",
                     help="pull history from a running MT5 terminal (Windows)")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--bars", type=int, default=20000, help="bars to pull for --from-mt5")
    ap.add_argument("--calendar-csv", help="economic-calendar CSV (time,currency,impact,"
                    "title) to apply the news risk filter and measure its effect")
    ap.add_argument("--trades-out", default="backtest_trades.csv")
    ap.add_argument("--equity-out", default="backtest_equity.csv")
    args = ap.parse_args()

    try:
        cfg = load_config(args.config)
    except FileNotFoundError:
        cfg = {}  # synthetic runs fine on defaults without a config file

    entry_tf = cfg.get("timeframe", "M15")
    trend_tf = cfg.get("trend_timeframe", "H1")
    warmup = int(cfg.get("warmup_bars", 300))
    symbol = cfg.get("symbol", "EURUSD")
    initial_balance = float(cfg.get("backtest", {}).get("initial_balance", 10_000))
    risk_pct = float(cfg.get("risk", {}).get("risk_per_trade_pct", 0.5))

    if args.csv:
        df = load_csv(args.csv)
    elif args.synthetic:
        df = make_synthetic(args.synthetic, tf=entry_tf)
    else:
        df = _load_from_mt5(symbol, entry_tf, args.bars)

    # Calendar risk filter, replayed from a CSV (sentiment is out of scope for
    # historical replay, so the overlay runs in event-filter-only mode here).
    news_provider = news_cfg = None
    if args.calendar_csv:
        from .news.calendar import CsvCalendar
        nc = news_overlay.news_config_from(cfg)
        news_provider = CsvCalendar(
            args.calendar_csv, pre_minutes=nc.pre_minutes,
            post_minutes=nc.post_minutes, threshold=nc.impact_threshold)
        news_cfg = news_overlay.NewsConfig(
            enabled=True, event_filter_enabled=True, sentiment_mode="off",
            pre_minutes=nc.pre_minutes, post_minutes=nc.post_minutes,
            impact_threshold=nc.impact_threshold)

    result = run_backtest(
        df, strat=strategy.from_config(cfg), risk_cfg=risk.from_config(cfg),
        entry_tf=entry_tf, trend_tf=trend_tf, spec=spec_from_config(cfg),
        costs=costs_from_config(cfg), initial_balance=initial_balance,
        risk_pct=risk_pct, warmup=warmup, symbol=symbol,
        news_provider=news_provider, news_cfg=news_cfg)

    print(f"Backtested {len(df)} bars ({entry_tf}, trend {trend_tf}) from "
          f"{df['time'].iloc[0]} to {df['time'].iloc[-1]}")
    print("Scorecard:", result.metrics.summary())
    print(f"Initial {initial_balance:.2f} -> Final {result.final_equity:.2f} "
          f"({result.total_return_pct:+.2f}%)")
    _write_csv(args.trades_out, result.trades)
    _write_csv(args.equity_out,
               [{"time": t.isoformat(), "equity": e} for t, e in result.equity_curve])
    print(f"Wrote {args.trades_out} and {args.equity_out}")
    print("Reminder: a backtest is necessary, not sufficient. Past != future.")


if __name__ == "__main__":
    main()
