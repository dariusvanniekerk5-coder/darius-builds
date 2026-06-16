"""Combine the news layer with the technical signal, and wire up a live provider.

`apply_news` is pure and unit-tested: it takes the technical Signal plus the
news inputs and returns a (possibly vetoed) Signal + a human reason. The default
keeps news in a *risk* role — it vetoes technical trades that fight strong fresh
sentiment, rather than inventing trades of its own.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..strategy import Direction, Signal
from . import calendar as calendar_mod
from . import headlines as headlines_mod
from . import sentiment as sentiment_mod
from .provider import (EventRisk, Impact, NewsProvider, NullNewsProvider,
                       Sentiment, currencies_for)


@dataclass
class NewsConfig:
    enabled: bool = False
    # Calendar risk filter
    event_filter_enabled: bool = True
    pre_minutes: int = 30
    post_minutes: int = 30
    impact_threshold: Impact = Impact.HIGH
    # Sentiment overlay
    sentiment_mode: str = "gate"        # "off" | "gate" | "confirm"
    min_confidence: float = 0.6
    sentiment_engine: str = "claude"    # "claude" | "rule"
    model: str = "claude-opus-4-8"
    freshness_minutes: int = 180
    feeds: list[str] = field(default_factory=list)
    cache_db: str = "sentiment_cache.sqlite"


def news_config_from(cfg: dict) -> NewsConfig:
    n = cfg.get("news", {})
    threshold = Impact.parse(n.get("impact_threshold", "high")) or Impact.HIGH
    return NewsConfig(
        enabled=n.get("enabled", False),
        event_filter_enabled=n.get("event_filter_enabled", True),
        pre_minutes=n.get("pre_minutes", 30),
        post_minutes=n.get("post_minutes", 30),
        impact_threshold=threshold,
        sentiment_mode=n.get("sentiment_mode", "gate"),
        min_confidence=n.get("min_confidence", 0.6),
        sentiment_engine=n.get("sentiment_engine", "claude"),
        model=n.get("model", "claude-opus-4-8"),
        freshness_minutes=n.get("freshness_minutes", 180),
        feeds=n.get("feeds", []) or [],
        cache_db=n.get("cache_db", "sentiment_cache.sqlite"),
    )


def apply_news(signal: Signal, event_risk: EventRisk, sentiment: Sentiment,
               cfg: NewsConfig) -> tuple[Signal, str]:
    """Return (possibly-vetoed signal, reason). Only ever turns an actionable signal
    FLAT — it never flips or creates a trade."""
    if not signal.is_actionable:
        return signal, ""

    # 1) Calendar risk filter — hard veto inside a high-impact window.
    if cfg.event_filter_enabled and event_risk.blocked:
        return _flatten(signal), f"blocked: {event_risk.reason}"

    # 2) Sentiment overlay.
    if cfg.sentiment_mode == "off":
        return signal, ""
    strong = sentiment.is_strong and sentiment.confidence >= cfg.min_confidence

    if cfg.sentiment_mode == "gate":
        if strong and sentiment.direction != signal.direction:
            return _flatten(signal), (
                f"vetoed: sentiment {sentiment.direction.value} "
                f"({sentiment.confidence:.2f}) opposes {signal.direction.value}")
        return signal, ""

    if cfg.sentiment_mode == "confirm":
        if strong and sentiment.direction == signal.direction:
            return signal, (f"confirmed by sentiment ({sentiment.confidence:.2f})")
        return _flatten(signal), "no sentiment confirmation"

    return signal, ""


def _flatten(signal: Signal) -> Signal:
    return Signal(Direction.FLAT, price=signal.price, atr=signal.atr,
                  reason=signal.reason)


class LiveNewsProvider(NewsProvider):
    """Composes a live calendar + RSS headlines + a (cached) sentiment engine."""

    def __init__(self, cfg: NewsConfig, *, sentiment_engine=None, calendar=None):
        self.cfg = cfg
        self.calendar = calendar or calendar_mod.LiveCalendar(
            pre_minutes=cfg.pre_minutes, post_minutes=cfg.post_minutes,
            threshold=cfg.impact_threshold)
        engine = sentiment_engine or self._build_engine(cfg)
        self.sentiment_engine = sentiment_mod.CachedSentiment(engine, cfg.cache_db)

    @staticmethod
    def _build_engine(cfg: NewsConfig):
        if cfg.sentiment_engine == "rule":
            return sentiment_mod.RuleBasedSentiment()
        return sentiment_mod.ClaudeSentiment(
            sentiment_mod.default_claude_client(), model=cfg.model)

    def event_risk(self, currencies: set[str], at: datetime) -> EventRisk:
        return self.calendar.event_risk(currencies, at)

    def sentiment(self, symbol: str, at: datetime) -> Sentiment:
        if self.cfg.sentiment_mode == "off":
            return Sentiment()
        heads = headlines_mod.fetch_headlines(
            self.cfg.feeds or None, freshness_minutes=self.cfg.freshness_minutes)
        return self.sentiment_engine.score(symbol, heads, at)


def build_provider(cfg: NewsConfig) -> NewsProvider:
    """Live provider when news is enabled, else a no-op provider."""
    if not cfg.enabled:
        return NullNewsProvider()
    return LiveNewsProvider(cfg)


__all__ = ["NewsConfig", "news_config_from", "apply_news", "LiveNewsProvider",
           "build_provider", "currencies_for"]
