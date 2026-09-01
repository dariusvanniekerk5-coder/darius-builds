"""NewsProvider interface + shared dataclasses. No network/LLM imports here, so it's
safe to import anywhere (bot, backtester, tests)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum

from ..strategy import Direction


class Impact(IntEnum):
    """Economic-event impact, orderable so thresholds work (`>= Impact.HIGH`)."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def parse(cls, value: str) -> "Impact | None":
        v = str(value).strip().lower()
        return {
            "low": cls.LOW, "medium": cls.MEDIUM, "moderate": cls.MEDIUM,
            "high": cls.HIGH,
        }.get(v)  # "holiday"/"" -> None (not a tradable-risk event)


@dataclass
class EventRisk:
    """Whether `at` falls inside a high-impact event window for the symbol."""
    blocked: bool = False
    impact: Impact | None = None
    titles: list[str] = field(default_factory=list)

    @property
    def reason(self) -> str:
        if not self.blocked:
            return "no high-impact event window"
        head = "; ".join(self.titles[:3]) or "scheduled event"
        return f"high-impact event window ({head})"


@dataclass
class Sentiment:
    """A directional read on fresh news. FLAT == neutral / not enough signal."""
    direction: Direction = Direction.FLAT
    confidence: float = 0.0          # 0..1
    reason: str = ""

    @property
    def is_strong(self) -> bool:
        return self.direction in (Direction.LONG, Direction.SHORT) and self.confidence > 0


def currencies_for(symbol: str) -> set[str]:
    """`EURUSD` -> {'EUR','USD'}. Strips suffixes like `.m`/`pro` by taking the first
    six alphabetic characters."""
    clean = "".join(c for c in symbol if c.isalpha()).upper()
    if len(clean) < 6:
        return set()
    return {clean[:3], clean[3:6]}


class NewsProvider:
    """Source of news-derived signals for a point in time. Live and backtest
    implementations share this interface so the overlay logic runs identically."""

    def event_risk(self, currencies: set[str], at: datetime) -> EventRisk:
        raise NotImplementedError

    def sentiment(self, symbol: str, at: datetime) -> Sentiment:
        raise NotImplementedError


class NullNewsProvider(NewsProvider):
    """Returns no event risk and neutral sentiment — used when news is disabled."""

    def event_risk(self, currencies: set[str], at: datetime) -> EventRisk:
        return EventRisk()

    def sentiment(self, symbol: str, at: datetime) -> Sentiment:
        return Sentiment()
