"""News & sentiment layer tests. No network or API key — Claude is stubbed."""
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest

from src import risk
from src.backtest import SymbolSpec, CostModel, run_backtest
from src.news import calendar as cal
from src.news.overlay import NewsConfig, apply_news
from src.news.provider import (EventRisk, Impact, NullNewsProvider, Sentiment,
                               currencies_for)
from src.news.sentiment import (CachedSentiment, ClaudeSentiment,
                                RuleBasedSentiment, SentimentEngine)
from src.strategy import Direction, Signal

UTC = timezone.utc


# --- helpers ---------------------------------------------------------------
def long_signal():
    return Signal(Direction.LONG, price=1.1, stop_loss=1.09, take_profit=1.12,
                  atr=0.001, reason="tech")


# --- pure helpers ----------------------------------------------------------
def test_currencies_for():
    assert currencies_for("EURUSD") == {"EUR", "USD"}
    assert currencies_for("eurusd.m") == {"EUR", "USD"}
    assert currencies_for("XAU") == set()


def test_impact_parse():
    assert Impact.parse("High") == Impact.HIGH
    assert Impact.parse("medium") == Impact.MEDIUM
    assert Impact.parse("Holiday") is None
    assert Impact.HIGH >= Impact.MEDIUM


# --- calendar --------------------------------------------------------------
def _calendar_csv(tmp_path):
    p = tmp_path / "cal.csv"
    p.write_text(
        "time,currency,impact,title\n"
        "2024-01-05T13:30:00+00:00,USD,High,Non-Farm Payrolls\n"
        "2024-01-05T10:00:00+00:00,EUR,Low,Minor speech\n"
    )
    return str(p)


def test_calendar_blocks_within_window(tmp_path):
    c = cal.CsvCalendar(_calendar_csv(tmp_path), pre_minutes=30, post_minutes=30,
                        threshold=Impact.HIGH)
    nfp = datetime(2024, 1, 5, 13, 30, tzinfo=UTC)
    assert c.event_risk({"EUR", "USD"}, nfp).blocked            # at the event
    assert c.event_risk({"EUR", "USD"}, nfp - timedelta(minutes=20)).blocked
    assert not c.event_risk({"EUR", "USD"}, nfp - timedelta(hours=2)).blocked
    # low-impact EUR event is below threshold -> no block
    assert not c.event_risk({"EUR", "USD"},
                            datetime(2024, 1, 5, 10, 0, tzinfo=UTC)).blocked
    # currency not in the pair -> no block
    assert not c.event_risk({"GBP", "JPY"}, nfp).blocked


def test_calendar_fail_safe_on_bad_path():
    c = cal.CsvCalendar.__new__(cal.CsvCalendar)  # bypass load
    cal._BaseCalendar.__init__(c)
    c._cache = []
    # _events raising should yield no block (covered via LiveCalendar path); here
    # an empty calendar simply never blocks:
    assert not c.event_risk({"EUR", "USD"}, datetime.now(UTC)).blocked


# --- overlay ---------------------------------------------------------------
def test_apply_news_event_veto():
    cfg = NewsConfig(enabled=True, event_filter_enabled=True, sentiment_mode="off")
    er = EventRisk(blocked=True, impact=Impact.HIGH, titles=["USD NFP"])
    out, reason = apply_news(long_signal(), er, Sentiment(), cfg)
    assert out.direction == Direction.FLAT and "blocked" in reason


def test_apply_news_gate_vetoes_conflict():
    cfg = NewsConfig(enabled=True, sentiment_mode="gate", min_confidence=0.6)
    bearish = Sentiment(Direction.SHORT, 0.8, "risk-off")
    out, reason = apply_news(long_signal(), EventRisk(), bearish, cfg)
    assert out.direction == Direction.FLAT and "vetoed" in reason


def test_apply_news_gate_keeps_when_weak_or_aligned():
    cfg = NewsConfig(enabled=True, sentiment_mode="gate", min_confidence=0.6)
    weak = Sentiment(Direction.SHORT, 0.3, "weak")          # below confidence
    assert apply_news(long_signal(), EventRisk(), weak, cfg)[0].direction == Direction.LONG
    aligned = Sentiment(Direction.LONG, 0.9, "risk-on")
    assert apply_news(long_signal(), EventRisk(), aligned, cfg)[0].direction == Direction.LONG


def test_apply_news_confirm_requires_agreement():
    cfg = NewsConfig(enabled=True, sentiment_mode="confirm", min_confidence=0.6)
    assert apply_news(long_signal(), EventRisk(),
                      Sentiment(Direction.LONG, 0.9), cfg)[0].direction == Direction.LONG
    # neutral sentiment -> no confirmation -> vetoed
    assert apply_news(long_signal(), EventRisk(),
                      Sentiment(), cfg)[0].direction == Direction.FLAT


def test_apply_news_off_passes_through():
    cfg = NewsConfig(enabled=True, sentiment_mode="off")
    out, _ = apply_news(long_signal(), EventRisk(), Sentiment(Direction.SHORT, 0.9), cfg)
    assert out.direction == Direction.LONG


# --- sentiment engines -----------------------------------------------------
def test_rule_based_sentiment():
    eng = RuleBasedSentiment()
    bull = eng.score("EURUSD", ["Euro rally as data beats, hawkish ECB"], datetime.now(UTC))
    assert bull.direction == Direction.LONG and bull.confidence > 0
    bear = eng.score("EURUSD", ["Euro plunge on dovish ECB, recession fears"],
                     datetime.now(UTC))
    assert bear.direction == Direction.SHORT
    flat = eng.score("EURUSD", ["The central bank met today"], datetime.now(UTC))
    assert flat.direction == Direction.FLAT


class _FakeBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeResp:
    def __init__(self, text, stop_reason="end_turn"):
        self.content = [_FakeBlock(text)]
        self.stop_reason = stop_reason


class _FakeMessages:
    def __init__(self, resp):
        self._resp = resp
        self.calls = 0

    def create(self, **kw):
        self.calls += 1
        return self._resp


class _FakeClient:
    def __init__(self, resp):
        self.messages = _FakeMessages(resp)


def test_claude_sentiment_parses():
    client = _FakeClient(_FakeResp('{"direction":"short","confidence":0.75,'
                                   '"reason":"hot CPI"}'))
    eng = ClaudeSentiment(client)
    s = eng.score("EURUSD", ["US CPI hotter than expected"], datetime.now(UTC))
    assert s.direction == Direction.SHORT and s.confidence == 0.75


def test_claude_sentiment_refusal_is_neutral():
    client = _FakeClient(_FakeResp("", stop_reason="refusal"))
    s = ClaudeSentiment(client).score("EURUSD", ["x"], datetime.now(UTC))
    assert s.direction == Direction.FLAT and "refus" in s.reason


def test_claude_sentiment_bad_json_is_neutral():
    s = ClaudeSentiment(_FakeClient(_FakeResp("not json"))).score(
        "EURUSD", ["x"], datetime.now(UTC))
    assert s.direction == Direction.FLAT


class _CountingEngine(SentimentEngine):
    def __init__(self):
        self.calls = 0

    def score(self, symbol, headlines, at):
        self.calls += 1
        return Sentiment(Direction.LONG, 0.7, "x")


def test_cached_sentiment_hit_miss(tmp_path):
    engine = _CountingEngine()
    cache = CachedSentiment(engine, str(tmp_path / "c.sqlite"), bucket_minutes=15)
    at = datetime(2024, 1, 1, 12, 0, tzinfo=UTC)
    a = cache.score("EURUSD", ["h1"], at)
    b = cache.score("EURUSD", ["h1"], at + timedelta(minutes=1))  # same bucket+hash
    assert a.direction == b.direction == Direction.LONG
    assert engine.calls == 1                                       # second was cached
    cache.score("EURUSD", ["different"], at)                       # new hash -> miss
    assert engine.calls == 2
    cache.close()


# --- backtest integration --------------------------------------------------
class _StubStrategy:
    """Fires one LONG when it first sees >= fire_at_len bars (engine-level test)."""
    def __init__(self, fire_at_len, sl, tp):
        self.fire_at_len, self.sl, self.tp, self.fired = fire_at_len, sl, tp, False

    def generate(self, df, trend_df):
        if not self.fired and len(df) >= self.fire_at_len:
            self.fired = True
            return Signal(Direction.LONG, price=float(df["close"].iloc[-1]),
                          stop_loss=self.sl, take_profit=self.tp, atr=0.001)
        return Signal(Direction.FLAT)


class _BlockingProvider(NullNewsProvider):
    def event_risk(self, currencies, at):
        return EventRisk(blocked=True, impact=Impact.HIGH, titles=["test event"])


def _rising_df():
    closes = list(np.linspace(1.1000, 1.1300, 60))
    return pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=len(closes), freq="15min", tz="UTC"),
        "open": closes, "high": np.array(closes) + 0.0001,
        "low": np.array(closes) - 0.0001, "close": closes,
    })


def test_backtest_news_filter_blocks_entry():
    spec = SymbolSpec()
    cfg = NewsConfig(enabled=True, event_filter_enabled=True, sentiment_mode="off")
    common = dict(risk_cfg=risk.RiskConfig(daily_max_loss_pct=100.0),
                  entry_tf="M15", trend_tf="H1", spec=spec, costs=CostModel(spread=0.0),
                  initial_balance=10_000, risk_pct=0.5, warmup=300, symbol="EURUSD")

    # Without news: the stub's long opens and wins.
    base = run_backtest(_rising_df(), strat=_StubStrategy(20, 1.0950, 1.1250), **common)
    assert base.metrics.closed_trades == 1

    # With a blocking calendar window: the same long is vetoed -> no trades.
    gated = run_backtest(_rising_df(), strat=_StubStrategy(20, 1.0950, 1.1250),
                         news_provider=_BlockingProvider(), news_cfg=cfg, **common)
    assert gated.metrics.closed_trades == 0
