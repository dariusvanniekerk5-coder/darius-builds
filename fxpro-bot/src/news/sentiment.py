"""Sentiment engines: turn fresh headlines into a directional read.

  * RuleBasedSentiment — free keyword/lexicon scoring (no key, blunt).
  * ClaudeSentiment    — uses an injected Anthropic client (so tests pass a stub; no
                         key/network needed). Uses raw JSON-schema structured output,
                         so this module needs no `anthropic`/`pydantic` import.
  * CachedSentiment    — wraps any engine, persisting scores so we don't re-pay per bar
                         and backtests replay deterministically.

`direction` is from the perspective of the BASE currency / the pair going up
(LONG = base strengthens), matching the technical strategy's Signal.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime

from ..strategy import Direction
from .provider import Sentiment

# --- rule-based -------------------------------------------------------------
_BULLISH = {"sur(ge)?", "rally", "jump", "gains", "strong", "beats", "hawkish",
            "rate hike", "robust", "upbeat", "tightening", "risk-on", "soars"}
_BEARISH = {"plunge", "slump", "falls", "weak", "misses", "dovish", "rate cut",
            "recession", "downbeat", "easing", "risk-off", "tumbles", "crisis"}


class SentimentEngine:
    def score(self, symbol: str, headlines: list[str], at: datetime) -> Sentiment:
        raise NotImplementedError


class RuleBasedSentiment(SentimentEngine):
    """Counts bullish vs bearish keywords across the base currency's headlines."""

    def score(self, symbol: str, headlines: list[str], at: datetime) -> Sentiment:
        text = " ".join(headlines).lower()
        bull = sum(text.count(w) for w in _BULLISH if " " in w) + \
            sum(1 for w in _BULLISH if " " not in w and w in text)
        bear = sum(text.count(w) for w in _BEARISH if " " in w) + \
            sum(1 for w in _BEARISH if " " not in w and w in text)
        total = bull + bear
        if total == 0:
            return Sentiment(reason="no sentiment keywords")
        if bull == bear:
            return Sentiment(reason="mixed sentiment")
        direction = Direction.LONG if bull > bear else Direction.SHORT
        confidence = abs(bull - bear) / total
        return Sentiment(direction=direction, confidence=round(confidence, 3),
                         reason=f"keyword score bull={bull} bear={bear}")


# --- Claude -----------------------------------------------------------------
_SYS_PROMPT = (
    "You are a forex news analyst. Given recent headlines, judge the likely SHORT-TERM "
    "directional pressure on the given currency pair. Respond ONLY via the schema. "
    "'long' = the base currency (first of the pair) likely strengthens vs the quote; "
    "'short' = likely weakens; 'flat' = no clear, fresh, tradable signal. Be "
    "conservative: most headlines are already priced in — prefer 'flat' with low "
    "confidence unless the news is clearly market-moving and fresh."
)

_SCHEMA = {
    "type": "object",
    "properties": {
        "direction": {"type": "string", "enum": ["long", "short", "flat"]},
        "confidence": {"type": "number"},
        "reason": {"type": "string"},
    },
    "required": ["direction", "confidence", "reason"],
    "additionalProperties": False,
}


class ClaudeSentiment(SentimentEngine):
    """Scores headlines with Claude via an injected client (`client.messages.create`).

    The client is injected so this is fully unit-testable with a stub. Use
    `default_claude_client()` to build a real one at runtime.
    """

    def __init__(self, client, model: str = "claude-opus-4-8", max_tokens: int = 512):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def score(self, symbol: str, headlines: list[str], at: datetime) -> Sentiment:
        if not headlines:
            return Sentiment(reason="no headlines")
        prompt = (f"Pair: {symbol}\nTime: {at.isoformat()}\nRecent headlines:\n"
                  + "\n".join(f"- {h}" for h in headlines[:30]))
        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=[{"type": "text", "text": _SYS_PROMPT,
                         "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": prompt}],
                output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
            )
        except Exception as exc:  # API/network failure -> neutral, never blocks
            return Sentiment(reason=f"sentiment error: {exc}")

        if getattr(resp, "stop_reason", None) == "refusal":
            return Sentiment(reason="model refused")
        text = next((b.text for b in resp.content if getattr(b, "type", None) == "text"),
                    None)
        if not text:
            return Sentiment(reason="empty response")
        try:
            data = json.loads(text)
            direction = {"long": Direction.LONG, "short": Direction.SHORT,
                         "flat": Direction.FLAT}[data["direction"]]
            confidence = max(0.0, min(1.0, float(data["confidence"])))
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
            return Sentiment(reason=f"parse error: {exc}")
        return Sentiment(direction=direction, confidence=confidence,
                         reason=str(data.get("reason", "")))


def default_claude_client():
    """Build a real Anthropic client (lazy import; needs `anthropic` + a key)."""
    import anthropic
    return anthropic.Anthropic()


# --- caching ----------------------------------------------------------------
class CachedSentiment(SentimentEngine):
    """Persists scores keyed by (symbol, bucketed time, headline hash) so repeated bars
    and backtests don't re-call the underlying engine."""

    def __init__(self, engine: SentimentEngine, db_path: str = "sentiment_cache.sqlite",
                 bucket_minutes: int = 15):
        self.engine = engine
        self.bucket_minutes = bucket_minutes
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS sentiment ("
            "key TEXT PRIMARY KEY, direction TEXT, confidence REAL, reason TEXT)")
        self.conn.commit()

    def _key(self, symbol: str, headlines: list[str], at: datetime) -> str:
        bucket = int(at.timestamp() // (self.bucket_minutes * 60))
        digest = hashlib.sha256("\n".join(headlines).encode()).hexdigest()[:16]
        return f"{symbol}:{bucket}:{digest}"

    def score(self, symbol: str, headlines: list[str], at: datetime) -> Sentiment:
        key = self._key(symbol, headlines, at)
        row = self.conn.execute(
            "SELECT direction, confidence, reason FROM sentiment WHERE key=?",
            (key,)).fetchone()
        if row:
            return Sentiment(direction=Direction(row[0]), confidence=row[1],
                             reason=row[2])
        result = self.engine.score(symbol, headlines, at)
        self.conn.execute(
            "INSERT OR REPLACE INTO sentiment VALUES (?, ?, ?, ?)",
            (key, result.direction.value, result.confidence, result.reason))
        self.conn.commit()
        return result

    def close(self) -> None:
        self.conn.close()
