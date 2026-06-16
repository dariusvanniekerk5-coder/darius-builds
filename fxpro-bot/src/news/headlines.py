"""Fetch recent FX/macro headlines via RSS (live-only).

`feedparser` is imported lazily so importing this module has no third-party deps.
Returns recent headline strings; relevance to the specific pair is left to the
sentiment engine (Claude judges it; the rule-based engine just keyword-scores).
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

# Free, no-key RSS feeds covering FX / macro news.
DEFAULT_FEEDS = [
    "https://www.fxstreet.com/rss/news",
    "https://www.forexlive.com/feed/news",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
]


def fetch_headlines(feeds: list[str] | None = None, *, freshness_minutes: int = 180,
                    limit: int = 30) -> list[str]:
    """Return recent headline titles across `feeds`, newest first. Returns [] on any
    failure (fail-safe — missing news must never block trading)."""
    feeds = feeds or DEFAULT_FEEDS
    cutoff = datetime.now(timezone.utc).timestamp() - freshness_minutes * 60
    items: list[tuple[float, str]] = []
    try:
        import feedparser  # lazy: live-only dependency
    except Exception:
        return []
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
        except Exception:
            continue
        for entry in parsed.entries:
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            ts = time.mktime(published) if published else cutoff + 1
            if ts >= cutoff and entry.get("title"):
                items.append((ts, entry["title"].strip()))
    items.sort(reverse=True)
    return [title for _, title in items[:limit]]
