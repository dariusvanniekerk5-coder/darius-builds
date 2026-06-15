# FXPro MT5 Demo Trading Bot

An automated trading bot for an **FXPro MetaTrader 5 _demo_ account**. It trades a
transparent EMA-crossover strategy with strict risk controls and journals every
trade so you can judge results honestly.

## Read this first — honest expectations

**This is not a money machine, and no AI "cracks" forex — not Claude, not ChatGPT.**

Retail forex is close to a zero-sum game played against banks and high-frequency
firms, and spreads, swaps and slippage tilt it further against retail traders. The
large majority of retail accounts lose money over time. A strategy that "wins most
of the time but sometimes blows up" is usually just coin-flipping with extra steps —
it looks great until variance catches up.

So the point of this project is **not** to promise profit. It's to be an *honest
measurement harness*:

- a simple, explainable baseline strategy (so we know exactly why it traded),
- hard risk controls (so one bad run can't wipe the account),
- a complete trade journal + scorecard (so we can tell a real edge from luck).

We judge it over **many** trades, not a lucky afternoon. And it runs on **demo
money** — zero financial risk. The impressive thing to show someone isn't a
guaranteed win; it's a rigorous, self-policing system that tells the truth about its
own performance.

### Safety guarantee
The bot reads the account's trade mode after login and **refuses to run unless the
account is a DEMO account** (`src/connection.py`). It will not place orders on real
money.

## Requirements

- **Windows** (the official `MetaTrader5` Python package is Windows-only in
  practice; on macOS/Linux you'd need a Windows VM or Wine).
- **Python 3.10+**.
- **MetaTrader 5 terminal** installed and logged into your FXPro **demo** account,
  left running while the bot runs.

> The bot connects to the MT5 *terminal* on the same machine. It cannot run in the
> cloud by itself — it runs on your PC, and you start/stop it.

## Setup

```bash
cd fxpro-bot
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt

copy .env.example .env                # then edit .env with your DEMO login
copy config.example.yaml config.yaml  # then tune if you like
```

Fill `.env` with your FXPro **demo** `MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER`
(server name is shown in the MT5 login dialog, e.g. `FxPro-MT5`).

## Run

```bash
# 1) Dry run — computes signals and prints what it WOULD do, sends no orders.
python -m src.bot --dry-run

# 2) Live demo trading — places orders on the demo account.
python -m src.bot
```

Press **Ctrl-C** to stop; it prints a scorecard and writes `trades.csv`.

## What it does each cycle

1. Wait for a new **closed** bar on the trading timeframe (default EURUSD M15).
2. Compute the signal: EMA(fast)/EMA(slow) crossover, filtered by a higher-timeframe
   trend (default H1 EMA50), with ATR-based stop-loss and take-profit.
3. Apply risk checks: daily max-loss kill switch, max open positions,
   one-position-per-symbol.
4. Size the position so the stop-loss costs a fixed % of equity (default 0.5%).
5. Place the order (or just log it in `--dry-run`) and journal everything.

## Backtesting (validate before you trust it)

Before letting a strategy trade even the demo account, replay it over historical
data. The backtester runs the **same** strategy, risk, and scorecard code as the
live bot:

```bash
# Quick smoke test on reproducible random-walk data (no data file needed):
python -m src.backtest --synthetic 5000

# On your own historical CSV (columns: time,open,high,low,close):
python -m src.backtest --csv path/to/EURUSD_M15.csv

# Pull history straight from a running MT5 terminal (Windows):
python -m src.backtest --from-mt5 --bars 20000
```

It writes `backtest_trades.csv` and `backtest_equity.csv` and prints the scorecard
plus total return.

**It is built to *not* lie to you:** no lookahead on signals or fills (entries fill
at the next bar's open), pessimistic intrabar exits (if a bar touches both stop and
target, the stop is assumed first), and modeled spread + commission costs. Even so —
**a good backtest is necessary, not sufficient.** The `--synthetic` mode proves the
point: a random walk has no edge, yet a given seed can still show a "profit" purely
by luck. Past performance does not predict the future.

## The scorecard

Every trade lands in `journal.sqlite` and `trades.csv`. Metrics computed:
win rate, profit factor, expectancy, net profit, and max drawdown. This is the
artifact worth showing — it's the honest record of what actually happened.

## Tests

The strategy, risk, and journal logic are pure Python and tested without MT5:

```bash
pip install pytest pandas numpy
pytest -q
```

## Tuning & next steps

- Edit `config.yaml` to change the symbol, timeframe, EMA/ATR params, and — most
  importantly — the risk limits.
- **Workflow:** tune params → **backtest** (`python -m src.backtest`) → if it holds
  up, run `--dry-run` live → then demo-trade. Re-backtest whenever you change the
  strategy.
- Watch out for over-fitting: if you tweak parameters until the backtest looks
  great, you've probably just memorised the past. Prefer params that work across
  many periods/instruments over ones that are perfect on one.

## Layout

```
src/
  config.py       load config.yaml + .env credentials
  connection.py   MT5 init/login + DEMO-only safety gate
  data.py         pull OHLC bars from MT5
  indicators.py   EMA / ATR / crossover helpers
  strategy.py     EMA-crossover strategy (Strategy interface)
  risk.py         position sizing + daily-loss kill switch + exposure limits
  execution.py    order_send wrappers (open/close, P/L reconciliation)
  journal.py      SQLite + CSV trade log and metrics (compute_metrics shared)
  timeframes.py   pure timeframe metadata (resample freq + bar duration)
  backtest.py     historical replay using the same strategy/risk/scorecard code
  bot.py          main loop
tests/            unit tests for strategy, risk, journal, backtest
```
