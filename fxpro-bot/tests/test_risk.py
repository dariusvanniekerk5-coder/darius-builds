"""Risk sizing + kill-switch tests. No MetaTrader5 needed."""
from datetime import datetime, timezone

import pytest

from src import risk
from src.risk import RiskConfig, RiskManager, position_size

# Typical EURUSD-like params for sizing math.
TICK_SIZE = 0.00001
TICK_VALUE = 1.0  # ~$1 per 0.00001 move per 1.0 lot


def test_position_size_basic():
    # risk $100 (1% of 10k), 20-pip stop -> $200 risk/lot -> 0.5 lots
    lots = position_size(
        equity=10_000, risk_pct=1.0, entry=1.1000, stop_loss=1.0980,
        tick_size=TICK_SIZE, tick_value=TICK_VALUE,
        volume_step=0.01, volume_min=0.01, volume_max=10.0,
    )
    assert lots == pytest.approx(0.5, abs=1e-9)


def test_position_size_rounds_down_to_step():
    lots = position_size(
        equity=10_000, risk_pct=1.0, entry=1.1000, stop_loss=1.0982,  # ~18 pip
        tick_size=TICK_SIZE, tick_value=TICK_VALUE,
        volume_step=0.1, volume_min=0.1, volume_max=10.0,
    )
    # raw ~0.555 -> rounded DOWN to 0.5 (never rounds risk up)
    assert lots == pytest.approx(0.5, abs=1e-9)


def test_position_size_skips_when_below_min():
    lots = position_size(
        equity=100, risk_pct=0.5, entry=1.1000, stop_loss=1.0900,  # 100 pip stop
        tick_size=TICK_SIZE, tick_value=TICK_VALUE,
        volume_step=0.01, volume_min=0.01, volume_max=10.0,
    )
    assert lots == 0.0


def test_position_size_caps_at_volume_max():
    lots = position_size(
        equity=1_000_000, risk_pct=5.0, entry=1.1000, stop_loss=1.0995,
        tick_size=TICK_SIZE, tick_value=TICK_VALUE,
        volume_step=0.01, volume_min=0.01, volume_max=1.0,
    )
    assert lots == pytest.approx(1.0, abs=1e-9)


def test_position_size_zero_stop_distance():
    assert position_size(
        equity=10_000, risk_pct=1.0, entry=1.1000, stop_loss=1.1000,
        tick_size=TICK_SIZE, tick_value=TICK_VALUE,
        volume_step=0.01, volume_min=0.01, volume_max=10.0,
    ) == 0.0


def test_daily_loss_kill_switch():
    mgr = RiskManager(RiskConfig(daily_max_loss_pct=2.0))
    day = datetime(2024, 1, 1, 9, 0, tzinfo=timezone.utc)
    mgr.mark_day(day, equity=10_000)

    assert mgr.daily_loss_pct(9_800) == pytest.approx(2.0)
    assert mgr.daily_loss_hit(9_800)
    allowed, reason = mgr.can_open_new(
        equity=9_800, open_positions_total=0, open_positions_symbol=0)
    assert not allowed and "daily loss" in reason

    # not yet at the limit -> allowed
    assert not mgr.daily_loss_hit(9_900)
    allowed, _ = mgr.can_open_new(
        equity=9_900, open_positions_total=0, open_positions_symbol=0)
    assert allowed


def test_daily_loss_resets_next_day():
    mgr = RiskManager(RiskConfig(daily_max_loss_pct=2.0))
    mgr.mark_day(datetime(2024, 1, 1, tzinfo=timezone.utc), equity=10_000)
    assert mgr.daily_loss_hit(9_700)
    # new calendar day resets the day-start equity baseline
    mgr.mark_day(datetime(2024, 1, 2, tzinfo=timezone.utc), equity=9_700)
    assert not mgr.daily_loss_hit(9_700)


def test_exposure_limits():
    mgr = RiskManager(RiskConfig(max_open_positions=1, one_position_per_symbol=True))
    mgr.mark_day(datetime(2024, 1, 1, tzinfo=timezone.utc), equity=10_000)

    allowed, reason = mgr.can_open_new(
        equity=10_000, open_positions_total=1, open_positions_symbol=0)
    assert not allowed and "max open positions" in reason

    mgr2 = RiskManager(RiskConfig(max_open_positions=5, one_position_per_symbol=True))
    mgr2.mark_day(datetime(2024, 1, 1, tzinfo=timezone.utc), equity=10_000)
    allowed, reason = mgr2.can_open_new(
        equity=10_000, open_positions_total=1, open_positions_symbol=1)
    assert not allowed and "symbol" in reason
