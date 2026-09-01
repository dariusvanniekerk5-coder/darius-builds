"""Main loop: poll for a new closed bar -> generate signal -> apply risk ->
execute on the demo account -> journal.

Run:
    python -m src.bot --dry-run     # signals only, NO orders sent
    python -m src.bot               # trade the DEMO account

Ctrl-C exits cleanly and prints the scorecard.
"""
from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone

from . import connection, data, execution, journal, risk, strategy
from .config import load_config, load_credentials
from .news import overlay as news_overlay
from .strategy import Direction


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def reconcile_closed(j: journal.Journal) -> None:
    """Find positions we logged as open that are no longer open, and journal
    their realized result (covers SL/TP exits the bot didn't trigger itself)."""
    live = {p.ticket for p in execution.open_positions()}
    for ticket in j.open_tickets() - live:
        info = execution.realized_pnl(ticket)
        if info is None:
            continue
        profit, exit_price, exit_time = info
        j.log_close(ticket=ticket, exit_price=exit_price, profit=profit,
                    exit_time=exit_time)
        j.log_event(_now_iso(), "INFO",
                    f"position {ticket} closed, realized P/L {profit:.2f}")


def run(config_path: str, dry_run: bool) -> None:
    cfg = load_config(config_path)
    creds = load_credentials()

    strat = strategy.from_config(cfg)
    risk_cfg = risk.from_config(cfg)
    risk_mgr = risk.RiskManager(risk_cfg)

    news_cfg = news_overlay.news_config_from(cfg)
    news_provider = news_overlay.build_provider(news_cfg)

    jcfg = cfg.get("journal", {})
    j = journal.Journal(jcfg.get("db_path", "journal.sqlite"),
                        jcfg.get("csv_path", "trades.csv"))

    symbol = cfg.get("symbol", "EURUSD")
    tf = cfg.get("timeframe", "M15")
    trend_tf = cfg.get("trend_timeframe", "H1")
    warmup = int(cfg.get("warmup_bars", 300))
    poll = int(cfg.get("poll_seconds", 15))

    # Safety gate: connects and REFUSES anything that isn't a demo account.
    info = connection.connect(creds)
    mode = "DRY-RUN (no orders)" if dry_run else "LIVE DEMO TRADING"
    news_state = "news ON" if news_cfg.enabled else "news off"
    print(f"[{_now_iso()}] connected demo acct {info.login} | equity={info.equity:.2f} "
          f"| {symbol} {tf} | {mode} | {news_state}")
    j.log_event(_now_iso(), "INFO", f"started {mode} on {symbol} {tf} ({news_state})")

    sym = execution.ensure_symbol(symbol)
    last_bar_time = None

    try:
        while True:
            try:
                bar_time = data.last_closed_bar_time(symbol, tf)
                if bar_time != last_bar_time:
                    last_bar_time = bar_time
                    _on_new_bar(cfg, strat, risk_mgr, j, symbol, tf, trend_tf,
                                warmup, sym, dry_run, news_cfg, news_provider)
            except Exception as exc:  # keep the loop alive; log and continue
                print(f"[{_now_iso()}] loop error: {exc}")
                j.log_event(_now_iso(), "ERROR", str(exc))
            time.sleep(poll)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        print("Scorecard:", j.metrics().summary())
        j.export_csv()
        j.close()
        connection.shutdown()


def _on_new_bar(cfg, strat, risk_mgr, j, symbol, tf, trend_tf, warmup, sym, dry_run,
                news_cfg, news_provider):
    # Keep the journal in sync with reality before deciding anything new.
    reconcile_closed(j)

    df = data.get_bars(symbol, tf, warmup)
    trend_df = data.get_bars(symbol, trend_tf, warmup)
    sig = strat.generate(df, trend_df)

    equity = execution.account_equity()
    risk_mgr.mark_day(datetime.now(timezone.utc), equity)

    print(f"[{_now_iso()}] bar={df['time'].iloc[-1]} close={sig.price:.5f} "
          f"signal={sig.direction.value} ({sig.reason})")

    if not sig.is_actionable:
        return

    # News/sentiment overlay: can only veto a technical signal, never create one.
    if news_cfg.enabled:
        now = datetime.now(timezone.utc)
        currencies = news_overlay.currencies_for(symbol)
        event_risk = news_provider.event_risk(currencies, now)
        sentiment = news_provider.sentiment(symbol, now)
        print(f"[{_now_iso()}] news: event={event_risk.reason} | "
              f"sentiment={sentiment.direction.value} "
              f"({sentiment.confidence:.2f}) {sentiment.reason}")
        sig, news_reason = news_overlay.apply_news(sig, event_risk, sentiment, news_cfg)
        if not sig.is_actionable:
            print(f"[{_now_iso()}] news veto: {news_reason}")
            j.log_event(_now_iso(), "INFO", f"news veto: {news_reason}")
            return

    total = len(execution.open_positions())
    in_symbol = len(execution.open_positions(symbol))
    allowed, reason = risk_mgr.can_open_new(
        equity=equity, open_positions_total=total, open_positions_symbol=in_symbol)
    if not allowed:
        print(f"[{_now_iso()}] skip {sig.direction.value}: {reason}")
        j.log_event(_now_iso(), "INFO", f"skip {sig.direction.value}: {reason}")
        return

    volume = risk.position_size(
        equity=equity,
        risk_pct=cfg.get("risk", {}).get("risk_per_trade_pct", 0.5),
        entry=sig.price,
        stop_loss=sig.stop_loss,
        tick_size=sym.tick_size,
        tick_value=sym.tick_value,
        volume_step=sym.volume_step,
        volume_min=sym.volume_min,
        volume_max=min(sym.volume_max, cfg.get("risk", {}).get("max_lot", 1.0)),
    )
    if volume <= 0:
        msg = "trade skipped: size below minimum within risk budget"
        print(f"[{_now_iso()}] {msg}")
        j.log_event(_now_iso(), "INFO", msg)
        return

    if dry_run:
        msg = (f"WOULD {sig.direction.value} {volume} {symbol} @~{sig.price:.5f} "
               f"sl={sig.stop_loss:.5f} tp={sig.take_profit:.5f}")
        print(f"[{_now_iso()}] [DRY-RUN] {msg}")
        j.log_event(_now_iso(), "DRYRUN", msg)
        return

    result = execution.open_market(
        symbol=symbol, direction=sig.direction, volume=volume,
        stop_loss=sig.stop_loss, take_profit=sig.take_profit)
    _handle_open_result(j, result, sig, symbol, volume)


def _handle_open_result(j, result, sig, symbol, volume):
    import MetaTrader5 as mt5  # local import; only reached when actually trading
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        rc = getattr(result, "retcode", "None")
        comment = getattr(result, "comment", "")
        msg = f"order FAILED retcode={rc} {comment}"
        print(f"[{_now_iso()}] {msg}")
        j.log_event(_now_iso(), "ERROR", msg)
        return

    ticket = result.order
    # The opened position's ticket equals the deal's position id; use order id as
    # our journal key and rely on reconcile to fill the close.
    pos = execution.open_positions(symbol)
    ticket = pos[-1].ticket if pos else ticket
    j.log_open(
        ticket=ticket, symbol=symbol, direction=sig.direction.value, volume=volume,
        entry_price=result.price, stop_loss=sig.stop_loss, take_profit=sig.take_profit,
        entry_time=_now_iso(), reason=sig.reason)
    msg = (f"OPENED {sig.direction.value} {volume} {symbol} @ {result.price:.5f} "
           f"ticket={ticket}")
    print(f"[{_now_iso()}] {msg}")
    j.log_event(_now_iso(), "INFO", msg)


def main() -> None:
    ap = argparse.ArgumentParser(description="FXPro MT5 demo trading bot")
    ap.add_argument("--config", default="config.yaml", help="path to config.yaml")
    ap.add_argument("--dry-run", action="store_true",
                    help="compute signals but send NO orders")
    args = ap.parse_args()
    run(args.config, args.dry_run)


if __name__ == "__main__":
    main()
