#!/usr/bin/env python3
"""Paper-trading bot with a two-file memory system (ledger + learnings).

PAPER TRADING ONLY. This script talks exclusively to Alpaca's paper
trading endpoint (via `paper=True`, hardcoded, not a flag) — there is no
live-trading code path here. See ../../.claude/skills/trading-bot-builder/
for the full writeup and how to add live trading later, deliberately.

Strategy: a simple fast/slow SMA crossover on one symbol. Before firing a
buy on a crossover, the bot checks learnings.md for a recorded loss on the
same symbol+strategy and skips if one exists. Every order is appended to
ledger.log. Losses are recorded into learnings.md via the `learn`
subcommand after you review a closed trade (this script does not track
open-position PnL automatically).

Usage:
    python3 scripts/trading_bot/bot.py run --symbol AAPL
    python3 scripts/trading_bot/bot.py loop --symbol AAPL --interval 60
    python3 scripts/trading_bot/bot.py learn --symbol AAPL --lesson "..."
    python3 scripts/trading_bot/bot.py status

Requires ALPACA_API_KEY and ALPACA_SECRET_KEY (paper trading keys) in the
environment or a local .env file. Get free paper trading keys at:
https://app.alpaca.markets/paper/dashboard/overview
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
LEDGER_PATH = DATA_DIR / "ledger.log"
LEARNINGS_PATH = DATA_DIR / "learnings.md"


def ensure_data_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    LEDGER_PATH.touch(exist_ok=True)
    LEARNINGS_PATH.touch(exist_ok=True)


def strategy_tag(fast: int, slow: int) -> str:
    return f"sma{fast}-{slow}"


def read_learnings() -> list[str]:
    ensure_data_files()
    return LEARNINGS_PATH.read_text().splitlines()


def has_prior_loss_lesson(symbol: str, tag: str) -> bool:
    marker = f"[{symbol}/{tag}]"
    return any(marker in line for line in read_learnings())


def write_learning(symbol: str, tag: str, lesson: str) -> None:
    ensure_data_files()
    with LEARNINGS_PATH.open("a") as f:
        f.write(f"[{symbol}/{tag}] {datetime.now(timezone.utc).isoformat()} - {lesson}\n")


def log_trade(symbol: str, action: str, qty, price, reason: str) -> None:
    ensure_data_files()
    is_new = LEDGER_PATH.stat().st_size == 0
    with LEDGER_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp_utc", "symbol", "action", "qty", "price", "reason"])
        writer.writerow(
            [datetime.now(timezone.utc).isoformat(), symbol, action, qty, price or "", reason]
        )


def get_clients():
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print(
            "Error: set ALPACA_API_KEY and ALPACA_SECRET_KEY (paper trading keys).\n"
            "Get free ones at https://app.alpaca.markets/paper/dashboard/overview",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from alpaca.trading.client import TradingClient
        from alpaca.data.historical import StockHistoricalDataClient
    except ImportError:
        print(
            "Error: alpaca-py is not installed.\n"
            "Install it with: pip install -r scripts/trading_bot/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    # paper=True is intentionally hardcoded — this script has no live-trading path.
    trading = TradingClient(api_key, secret_key, paper=True)
    data = StockHistoricalDataClient(api_key, secret_key)
    return trading, data


def sma(values: list[float], period: int) -> float:
    return sum(values[-period:]) / period


def check_signal(data_client, symbol: str, fast: int, slow: int):
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute, limit=slow + 1)
    bars = data_client.get_stock_bars(request).df
    if bars.empty:
        return None
    closes = bars["close"].tolist()
    if len(closes) < slow + 1:
        return None

    fast_prev, fast_now = sma(closes[:-1], fast), sma(closes, fast)
    slow_prev, slow_now = sma(closes[:-1], slow), sma(closes, slow)

    if fast_prev <= slow_prev and fast_now > slow_now:
        return "buy"
    if fast_prev >= slow_prev and fast_now < slow_now:
        return "sell"
    return None


def cmd_run(args) -> int:
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.trading.requests import MarketOrderRequest

    trading, data = get_clients()
    tag = strategy_tag(args.fast, args.slow)
    signal = check_signal(data, args.symbol, args.fast, args.slow)

    if signal is None:
        print(f"No crossover signal for {args.symbol} right now.")
        return 0

    if signal == "buy" and has_prior_loss_lesson(args.symbol, tag):
        print(f"Signal fired ({signal}) but skipping: prior recorded loss for {args.symbol}/{tag}.")
        log_trade(args.symbol, "skip", args.qty, None, f"learnings.md lesson for {tag}")
        return 0

    order = MarketOrderRequest(
        symbol=args.symbol,
        qty=args.qty,
        side=OrderSide.BUY if signal == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    result = trading.submit_order(order)
    log_trade(args.symbol, signal, args.qty, None, f"{tag} crossover")
    print(f"[PAPER] {signal} {args.qty} {args.symbol} submitted (order id {result.id})")
    return 0


def cmd_loop(args) -> int:
    print(f"Polling {args.symbol} every {args.interval}s (Ctrl+C to stop)...")
    try:
        while True:
            cmd_run(args)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


def cmd_learn(args) -> int:
    tag = strategy_tag(args.fast, args.slow)
    write_learning(args.symbol, tag, args.lesson)
    print(f"Recorded lesson for {args.symbol}/{tag}: {args.lesson}")
    return 0


def cmd_status(_args) -> int:
    ensure_data_files()
    print(f"--- {LEDGER_PATH} ---")
    print(LEDGER_PATH.read_text() or "(empty)")
    print(f"\n--- {LEARNINGS_PATH} ---")
    print(LEARNINGS_PATH.read_text() or "(empty)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_strategy_args(p):
        p.add_argument("--symbol", required=True, help="Ticker symbol, e.g. AAPL")
        p.add_argument("--fast", type=int, default=10, help="Fast SMA period (default: 10)")
        p.add_argument("--slow", type=int, default=30, help="Slow SMA period (default: 30)")
        p.add_argument("--qty", type=float, default=1, help="Order quantity (default: 1)")

    run_p = sub.add_parser("run", help="Check the signal once and paper-trade if it fires")
    add_strategy_args(run_p)
    run_p.set_defaults(func=cmd_run)

    loop_p = sub.add_parser("loop", help="Repeat `run` on an interval")
    add_strategy_args(loop_p)
    loop_p.add_argument("--interval", type=int, default=60, help="Seconds between checks (default: 60)")
    loop_p.set_defaults(func=cmd_loop)

    learn_p = sub.add_parser("learn", help="Manually record a lesson after reviewing a closed trade")
    learn_p.add_argument("--symbol", required=True)
    learn_p.add_argument("--fast", type=int, default=10)
    learn_p.add_argument("--slow", type=int, default=30)
    learn_p.add_argument("--lesson", required=True, help="Plain-English lesson, e.g. 'lost on low-volume chop'")
    learn_p.set_defaults(func=cmd_learn)

    status_p = sub.add_parser("status", help="Print the ledger and learnings files")
    status_p.set_defaults(func=cmd_status)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
