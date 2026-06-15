"""Trade journal + honest scorecard.

Logs every opened/closed trade to SQLite, mirrors closed trades to CSV, and
computes the metrics that actually matter for judging an edge: win rate, profit
factor, expectancy, and max drawdown. No MetaTrader5 import — pure stdlib — so
it is fully testable and usable for analysis after a run.
"""
from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass

SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    ticket      INTEGER PRIMARY KEY,
    symbol      TEXT NOT NULL,
    direction   TEXT NOT NULL,
    volume      REAL NOT NULL,
    entry_price REAL NOT NULL,
    stop_loss   REAL,
    take_profit REAL,
    entry_time  TEXT NOT NULL,
    exit_price  REAL,
    exit_time   TEXT,
    profit      REAL,
    status      TEXT NOT NULL DEFAULT 'open',
    reason      TEXT
);
CREATE TABLE IF NOT EXISTS events (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    time  TEXT NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL
);
"""


@dataclass
class Metrics:
    closed_trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0          # fraction 0..1
    gross_profit: float = 0.0      # sum of winning P/L
    gross_loss: float = 0.0        # sum of losing P/L (negative)
    profit_factor: float = 0.0     # gross_profit / |gross_loss|
    net_profit: float = 0.0
    expectancy: float = 0.0        # net_profit / closed_trades
    max_drawdown: float = 0.0      # largest peak-to-trough drop on realized P/L curve

    def summary(self) -> str:
        return (
            f"trades={self.closed_trades} win_rate={self.win_rate*100:.1f}% "
            f"profit_factor={self.profit_factor:.2f} net={self.net_profit:.2f} "
            f"expectancy={self.expectancy:.2f} max_dd={self.max_drawdown:.2f}"
        )


class Journal:
    def __init__(self, db_path: str = "journal.sqlite", csv_path: str = "trades.csv"):
        self.db_path = db_path
        self.csv_path = csv_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # --- writes -------------------------------------------------------------
    def log_open(
        self,
        *,
        ticket: int,
        symbol: str,
        direction: str,
        volume: float,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        entry_time: str,
        reason: str = "",
    ) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO trades
               (ticket, symbol, direction, volume, entry_price, stop_loss,
                take_profit, entry_time, status, reason)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?)""",
            (ticket, symbol, direction, volume, entry_price, stop_loss,
             take_profit, entry_time, reason),
        )
        self.conn.commit()

    def log_close(self, *, ticket: int, exit_price: float, profit: float,
                  exit_time: str) -> None:
        self.conn.execute(
            """UPDATE trades
               SET exit_price=?, profit=?, exit_time=?, status='closed'
               WHERE ticket=?""",
            (exit_price, profit, exit_time, ticket),
        )
        self.conn.commit()
        self.export_csv()

    def log_event(self, time: str, level: str, message: str) -> None:
        self.conn.execute(
            "INSERT INTO events (time, level, message) VALUES (?, ?, ?)",
            (time, level, message),
        )
        self.conn.commit()

    def open_tickets(self) -> set[int]:
        rows = self.conn.execute(
            "SELECT ticket FROM trades WHERE status='open'"
        ).fetchall()
        return {r["ticket"] for r in rows}

    # --- reads / analysis ---------------------------------------------------
    def closed_profits(self) -> list[float]:
        rows = self.conn.execute(
            "SELECT profit FROM trades WHERE status='closed' AND profit IS NOT NULL "
            "ORDER BY exit_time"
        ).fetchall()
        return [float(r["profit"]) for r in rows]

    def metrics(self) -> Metrics:
        profits = self.closed_profits()
        m = Metrics(closed_trades=len(profits))
        if not profits:
            return m

        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p < 0]
        m.wins = len(wins)
        m.losses = len(losses)
        m.win_rate = m.wins / m.closed_trades
        m.gross_profit = sum(wins)
        m.gross_loss = sum(losses)
        m.net_profit = sum(profits)
        m.expectancy = m.net_profit / m.closed_trades
        m.profit_factor = (
            m.gross_profit / abs(m.gross_loss) if m.gross_loss != 0
            else float("inf") if m.gross_profit > 0 else 0.0
        )
        m.max_drawdown = _max_drawdown(profits)
        return m

    def export_csv(self) -> None:
        rows = self.conn.execute(
            "SELECT * FROM trades ORDER BY entry_time"
        ).fetchall()
        if not rows:
            return
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            for r in rows:
                writer.writerow([r[k] for k in r.keys()])


def _max_drawdown(profits: list[float]) -> float:
    """Largest peak-to-trough drop on the cumulative realized-P/L curve.
    Returned as a positive number (0 if never underwater)."""
    cum = 0.0
    peak = 0.0
    max_dd = 0.0
    for p in profits:
        cum += p
        peak = max(peak, cum)
        max_dd = max(max_dd, peak - cum)
    return max_dd
