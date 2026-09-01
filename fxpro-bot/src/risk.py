"""Risk management — the part that keeps the account alive.

Everything here is pure Python (no MetaTrader5 import) so it can be fully unit
tested. The bot pulls live numbers from MT5 and feeds them in.

Three jobs:
  1. Position sizing from a fixed % of equity and the stop distance.
  2. A daily max-loss kill switch that halts NEW trades for the rest of the day.
  3. Exposure limits (max open positions, one-position-per-symbol).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class RiskConfig:
    risk_per_trade_pct: float = 0.5
    max_open_positions: int = 1
    one_position_per_symbol: bool = True
    daily_max_loss_pct: float = 2.0
    min_lot: float = 0.01
    max_lot: float = 1.0


def from_config(cfg: dict) -> RiskConfig:
    r = cfg.get("risk", {})
    return RiskConfig(
        risk_per_trade_pct=r.get("risk_per_trade_pct", 0.5),
        max_open_positions=r.get("max_open_positions", 1),
        one_position_per_symbol=r.get("one_position_per_symbol", True),
        daily_max_loss_pct=r.get("daily_max_loss_pct", 2.0),
        min_lot=r.get("min_lot", 0.01),
        max_lot=r.get("max_lot", 1.0),
    )


def _round_down_to_step(volume: float, step: float) -> float:
    """Round a lot size DOWN to the broker's volume step (conservative — never
    rounds risk up)."""
    if step <= 0:
        return volume
    # Add a tiny epsilon so values already on a step boundary aren't nudged down
    # by floating point error (e.g. 0.30 -> 0.29).
    return math.floor(volume / step + 1e-9) * step


def position_size(
    *,
    equity: float,
    risk_pct: float,
    entry: float,
    stop_loss: float,
    tick_size: float,
    tick_value: float,
    volume_step: float,
    volume_min: float,
    volume_max: float,
) -> float:
    """Lots to trade so that hitting the stop loses ~`risk_pct`% of equity.

    `tick_size` is the price increment of one tick; `tick_value` is the money
    (account currency) gained/lost per tick for one lot. These come from MT5's
    symbol_info (trade_tick_size / trade_tick_value).

    Returns 0.0 when a trade can't be sized within the risk budget (e.g. the
    minimum lot would risk more than allowed) — we skip rather than over-risk.
    """
    if equity <= 0 or risk_pct <= 0:
        return 0.0
    stop_distance = abs(entry - stop_loss)
    if stop_distance <= 0 or tick_size <= 0 or tick_value <= 0:
        return 0.0

    risk_amount = equity * (risk_pct / 100.0)
    money_per_lot = (stop_distance / tick_size) * tick_value
    if money_per_lot <= 0:
        return 0.0

    raw_lots = risk_amount / money_per_lot
    capped = min(raw_lots, volume_max)
    lots = _round_down_to_step(capped, volume_step)

    # If even the rounded size is below the broker minimum, taking it would
    # break the risk budget — skip the trade instead.
    if lots < volume_min:
        return 0.0
    return round(lots, 8)


class RiskManager:
    """Stateful gatekeeper for opening new trades. One instance per bot run."""

    def __init__(self, config: RiskConfig):
        self.config = config
        self._day: date | None = None
        self._day_start_equity: float | None = None

    def mark_day(self, now: datetime, equity: float) -> None:
        """Record day-start equity, resetting at each new calendar day (UTC).
        Call once per loop with the current time and equity."""
        today = now.date()
        if self._day != today:
            self._day = today
            self._day_start_equity = equity

    def daily_loss_pct(self, equity: float) -> float:
        """How far equity is below the day's starting equity, in percent
        (0 if flat or up)."""
        if not self._day_start_equity:
            return 0.0
        drop = self._day_start_equity - equity
        if drop <= 0:
            return 0.0
        return drop / self._day_start_equity * 100.0

    def daily_loss_hit(self, equity: float) -> bool:
        return self.daily_loss_pct(equity) >= self.config.daily_max_loss_pct

    def can_open_new(
        self,
        *,
        equity: float,
        open_positions_total: int,
        open_positions_symbol: int,
    ) -> tuple[bool, str]:
        """Decide whether a new position may be opened. Returns (allowed, reason)."""
        if self.daily_loss_hit(equity):
            return False, (
                f"daily loss limit reached "
                f"({self.daily_loss_pct(equity):.2f}% >= {self.config.daily_max_loss_pct}%)"
            )
        if open_positions_total >= self.config.max_open_positions:
            return False, (
                f"max open positions reached ({open_positions_total}"
                f"/{self.config.max_open_positions})"
            )
        if self.config.one_position_per_symbol and open_positions_symbol > 0:
            return False, "already have a position in this symbol"
        return True, "ok"
