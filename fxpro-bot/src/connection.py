"""MT5 connection + the demo-account safety guard.

THE most important safety property of this whole project lives here: after
logging in we verify the account is a DEMO account and refuse to continue
otherwise. This bot must never place orders on real money.

Imports MetaTrader5, which is Windows-only and requires a running MT5 terminal,
so this module is exercised on the trading PC (not in CI).
"""
from __future__ import annotations

import MetaTrader5 as mt5  # type: ignore

from .config import Credentials


class LiveAccountError(RuntimeError):
    """Raised when the connected account is NOT a demo account."""


class ConnectionError_(RuntimeError):
    """Raised when MT5 cannot initialize or log in."""


def connect(creds: Credentials):
    """Initialize MT5, log in, and assert the account is a demo. Returns the
    MT5 account_info object on success."""
    kwargs = {
        "login": creds.login,
        "password": creds.password,
        "server": creds.server,
    }
    if creds.terminal_path:
        ok = mt5.initialize(creds.terminal_path, **kwargs)
    else:
        ok = mt5.initialize(**kwargs)
    if not ok:
        raise ConnectionError_(f"mt5.initialize failed: {mt5.last_error()}")

    info = mt5.account_info()
    if info is None:
        raise ConnectionError_(f"mt5.account_info returned None: {mt5.last_error()}")

    # Hard safety gate: only ACCOUNT_TRADE_MODE_DEMO is allowed.
    if info.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        mode = {
            mt5.ACCOUNT_TRADE_MODE_REAL: "REAL",
            mt5.ACCOUNT_TRADE_MODE_CONTEST: "CONTEST",
            mt5.ACCOUNT_TRADE_MODE_DEMO: "DEMO",
        }.get(info.trade_mode, str(info.trade_mode))
        shutdown()
        raise LiveAccountError(
            f"Refusing to run: connected account is {mode}, not DEMO. "
            "This bot only trades demo accounts."
        )
    return info


def shutdown() -> None:
    mt5.shutdown()
