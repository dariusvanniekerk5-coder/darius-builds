"""Load config.yaml and .env credentials. No MetaTrader5 import."""
from __future__ import annotations

import os
from dataclasses import dataclass

import yaml
from dotenv import load_dotenv


@dataclass
class Credentials:
    login: int
    password: str
    server: str
    terminal_path: str | None = None


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_credentials() -> Credentials:
    """Read MT5 demo credentials from environment / .env file."""
    load_dotenv()
    login = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    if not (login and password and server):
        raise RuntimeError(
            "Missing MT5 credentials. Copy .env.example to .env and fill in "
            "MT5_LOGIN, MT5_PASSWORD and MT5_SERVER (use your FxPro DEMO account)."
        )
    return Credentials(
        login=int(login),
        password=password,
        server=server,
        terminal_path=os.getenv("MT5_TERMINAL_PATH") or None,
    )
