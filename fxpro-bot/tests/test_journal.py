"""Journal + scorecard metrics tests. No MetaTrader5 needed."""
import math

from src.journal import Journal


def _record(j, ticket, profit):
    j.log_open(ticket=ticket, symbol="EURUSD", direction="long", volume=0.1,
               entry_price=1.1, stop_loss=1.09, take_profit=1.12,
               entry_time=f"2024-01-01T00:0{ticket}:00+00:00", reason="t")
    j.log_close(ticket=ticket, exit_price=1.11, profit=profit,
                exit_time=f"2024-01-01T01:0{ticket}:00+00:00")


def test_metrics_empty(tmp_path):
    j = Journal(str(tmp_path / "j.sqlite"), str(tmp_path / "t.csv"))
    m = j.metrics()
    assert m.closed_trades == 0 and m.net_profit == 0.0
    j.close()


def test_metrics_basic(tmp_path):
    j = Journal(str(tmp_path / "j.sqlite"), str(tmp_path / "t.csv"))
    for i, p in enumerate([100.0, -50.0, 75.0, -25.0], start=1):
        _record(j, i, p)

    m = j.metrics()
    assert m.closed_trades == 4
    assert m.wins == 2 and m.losses == 2
    assert m.win_rate == 0.5
    assert m.net_profit == 100.0
    assert m.gross_profit == 175.0
    assert m.gross_loss == -75.0
    assert m.profit_factor == math.isclose(175.0 / 75.0, m.profit_factor) or \
        abs(m.profit_factor - 175.0 / 75.0) < 1e-9
    assert m.expectancy == 25.0
    # cumulative P/L curve: 100 -> 50 -> 125 -> 100.
    # worst peak-to-trough drop is 100 -> 50 = 50.
    assert m.max_drawdown == 50.0
    j.close()


def test_csv_export(tmp_path):
    csv_path = tmp_path / "t.csv"
    j = Journal(str(tmp_path / "j.sqlite"), str(csv_path))
    _record(j, 1, 100.0)
    assert csv_path.exists()
    contents = csv_path.read_text()
    assert "ticket" in contents and "EURUSD" in contents
    j.close()


def test_open_tickets_tracking(tmp_path):
    j = Journal(str(tmp_path / "j.sqlite"), str(tmp_path / "t.csv"))
    j.log_open(ticket=42, symbol="EURUSD", direction="long", volume=0.1,
               entry_price=1.1, stop_loss=1.09, take_profit=1.12,
               entry_time="2024-01-01T00:00:00+00:00")
    assert j.open_tickets() == {42}
    j.log_close(ticket=42, exit_price=1.11, profit=10.0,
                exit_time="2024-01-01T01:00:00+00:00")
    assert j.open_tickets() == set()
    j.close()
