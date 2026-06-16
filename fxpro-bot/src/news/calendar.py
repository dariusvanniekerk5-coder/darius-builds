"""Economic calendar: detect high-impact event windows for a symbol's currencies.

Two implementations share the same window logic:
  * CsvCalendar  — reads events from a CSV (used by the backtester, fully offline).
  * LiveCalendar — fetches the free ForexFactory weekly JSON (used by the live bot).

`requests` is imported lazily inside LiveCalendar so this module imports with no
third-party deps (CsvCalendar + the window logic are pure stdlib and testable here).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .provider import EventRisk, Impact, NewsProvider, Sentiment

# Free weekly economic calendar (ForexFactory data via FairEconomy). No key required.
FF_THIS_WEEK = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"


@dataclass
class CalendarEvent:
    time: datetime          # tz-aware (UTC)
    currency: str           # e.g. "USD"
    impact: Impact
    title: str


def _parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def event_risk_from(
    events: list[CalendarEvent],
    currencies: set[str],
    at: datetime,
    *,
    pre_minutes: int,
    post_minutes: int,
    threshold: Impact,
) -> EventRisk:
    """Block if `at` is within [event - pre, event + post] of any event at/above
    `threshold` for one of `currencies`. Shared by both calendars and unit-tested."""
    pre = timedelta(minutes=pre_minutes)
    post = timedelta(minutes=post_minutes)
    hits = [
        e for e in events
        if e.currency in currencies and e.impact >= threshold
        and (e.time - pre) <= at <= (e.time + post)
    ]
    if not hits:
        return EventRisk()
    return EventRisk(
        blocked=True,
        impact=max(e.impact for e in hits),
        titles=[f"{e.currency} {e.title}" for e in hits],
    )


class _BaseCalendar(NewsProvider):
    def __init__(self, *, pre_minutes: int = 30, post_minutes: int = 30,
                 threshold: Impact = Impact.HIGH):
        self.pre_minutes = pre_minutes
        self.post_minutes = post_minutes
        self.threshold = threshold

    def _events(self, at: datetime) -> list[CalendarEvent]:
        raise NotImplementedError

    def event_risk(self, currencies: set[str], at: datetime) -> EventRisk:
        try:
            events = self._events(at)
        except Exception:
            return EventRisk()  # fail safe: a dead feed never blocks trading
        return event_risk_from(
            events, currencies, at,
            pre_minutes=self.pre_minutes, post_minutes=self.post_minutes,
            threshold=self.threshold)

    def sentiment(self, symbol: str, at: datetime) -> Sentiment:
        return Sentiment()  # calendar carries no sentiment


def load_calendar_csv(path: str) -> list[CalendarEvent]:
    """CSV columns: time, currency, impact, title (case-insensitive headers)."""
    events: list[CalendarEvent] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [c.strip().lower() for c in (reader.fieldnames or [])]
        for row in reader:
            row = {k.strip().lower(): v for k, v in row.items()}
            impact = Impact.parse(row.get("impact", ""))
            if impact is None:
                continue
            events.append(CalendarEvent(
                time=_parse_time(row["time"]),
                currency=str(row["currency"]).strip().upper(),
                impact=impact,
                title=str(row.get("title", "")).strip(),
            ))
    return events


class CsvCalendar(_BaseCalendar):
    def __init__(self, path: str, **kw):
        super().__init__(**kw)
        self._cache = load_calendar_csv(path)

    def _events(self, at: datetime) -> list[CalendarEvent]:
        return self._cache


class LiveCalendar(_BaseCalendar):
    """Fetches the free weekly ForexFactory JSON and caches it for an hour."""

    def __init__(self, url: str = FF_THIS_WEEK, **kw):
        super().__init__(**kw)
        self.url = url
        self._cache: list[CalendarEvent] = []
        self._fetched_at: datetime | None = None

    def _events(self, at: datetime) -> list[CalendarEvent]:
        now = datetime.now(timezone.utc)
        if self._fetched_at and (now - self._fetched_at) < timedelta(hours=1):
            return self._cache
        import requests  # lazy: live-only dependency
        data = requests.get(self.url, timeout=15).json()
        events: list[CalendarEvent] = []
        for item in data:
            impact = Impact.parse(item.get("impact", ""))
            if impact is None:
                continue
            events.append(CalendarEvent(
                time=_parse_time(item["date"]),
                currency=str(item.get("country", "")).strip().upper(),
                impact=impact,
                title=str(item.get("title", "")).strip(),
            ))
        self._cache = events
        self._fetched_at = now
        return events
