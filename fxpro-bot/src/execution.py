"""Order execution wrappers around MT5's order_send.

Imports MetaTrader5 (Windows + running terminal). Keeps the request-building and
broker quirks (filling modes, bid/ask sides) in one place so bot.py stays
readable.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import MetaTrader5 as mt5  # type: ignore

from .strategy import Direction

MAGIC = 770077  # identifies this bot's orders


@dataclass
class SymbolParams:
    tick_size: float
    tick_value: float
    volume_step: float
    volume_min: float
    volume_max: float
    digits: int


def ensure_symbol(symbol: str) -> SymbolParams:
    """Make the symbol visible in Market Watch and return its trade params."""
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Could not select symbol {symbol}: {mt5.last_error()}")
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"No symbol_info for {symbol}: {mt5.last_error()}")
    return SymbolParams(
        tick_size=info.trade_tick_size,
        tick_value=info.trade_tick_value,
        volume_step=info.volume_step,
        volume_min=info.volume_min,
        volume_max=info.volume_max,
        digits=info.digits,
    )


def account_equity() -> float:
    info = mt5.account_info()
    if info is None:
        raise RuntimeError(f"account_info failed: {mt5.last_error()}")
    return float(info.equity)


def open_positions(symbol: str | None = None):
    positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    return list(positions) if positions else []


def realized_pnl(ticket: int):
    """Total realized P/L (profit + swap + commission), exit price and exit time
    for a closed position, read from deal history.

    Returns (profit, exit_price, exit_time_iso) or None if no closing deals are
    found yet. Used to journal positions that closed on SL/TP without us.
    """
    # Select a generous history window so the deals are loaded.
    mt5.history_select(datetime.now(timezone.utc) - timedelta(days=30),
                       datetime.now(timezone.utc) + timedelta(days=1))
    deals = mt5.history_deals_get(position=ticket)
    if not deals:
        return None
    # Exclude the entry deal (entry==DEAL_ENTRY_IN) when summing realized P/L is
    # unnecessary — profit/swap/commission are attributed to closing deals — but
    # summing all deals for the position gives the correct net regardless.
    profit = sum(d.profit + d.swap + d.commission for d in deals)
    last = deals[-1]
    exit_time = datetime.fromtimestamp(last.time, tz=timezone.utc).isoformat()
    return profit, float(last.price), exit_time


def open_market(
    *,
    symbol: str,
    direction: Direction,
    volume: float,
    stop_loss: float,
    take_profit: float,
    deviation: int = 20,
    comment: str = "ema-bot",
):
    """Send a market order with SL/TP. Tries IOC then FOK filling for broker
    compatibility. Returns the MT5 order result (check .retcode == TRADE_RETCODE_DONE)."""
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"No tick for {symbol}: {mt5.last_error()}")

    if direction == Direction.LONG:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif direction == Direction.SHORT:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        raise ValueError("open_market requires LONG or SHORT")

    base = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "price": price,
        "sl": float(stop_loss),
        "tp": float(take_profit),
        "deviation": deviation,
        "magic": MAGIC,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
    }

    result = None
    for filling in (mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK):
        request = {**base, "type_filling": filling}
        result = mt5.order_send(request)
        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            return result
    return result  # caller logs the failure retcode


def close_position(position):
    """Close an open position by sending the opposite market order."""
    symbol = position.symbol
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"No tick for {symbol}: {mt5.last_error()}")

    if position.type == mt5.POSITION_TYPE_BUY:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask

    base = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": order_type,
        "position": position.ticket,
        "price": price,
        "deviation": 20,
        "magic": MAGIC,
        "comment": "ema-bot-close",
        "type_time": mt5.ORDER_TIME_GTC,
    }
    result = None
    for filling in (mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK):
        result = mt5.order_send({**base, "type_filling": filling})
        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            return result
    return result
