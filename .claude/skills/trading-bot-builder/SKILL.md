---
name: trading-bot-builder
description: Build and run a paper-trading stock bot with a two-file memory system (ledger + learnings) using a moving-average crossover strategy on Alpaca's paper trading API. Use when the user wants to build, set up, or run an AI/automated trading bot, or asks about giving a trading bot memory so it learns from past losses. This skill only ever places PAPER trades — it has no live-trading code path.
---

# Trading Bot Builder

Builds and runs the paper-trading bot in `scripts/trading_bot/bot.py`, based
on the 3-step method (venue → strategy → memory) from this reference video:
https://youtu.be/PBBSMSyU674

## Scope — read before using

This is **paper trading only**. `scripts/trading_bot/bot.py` hardcodes
`paper=True` when constructing Alpaca's `TradingClient` — there is no flag,
env var, or code path in this script that places a live order. Do not add
one without the user explicitly asking for live trading in a separate,
deliberate step, and even then treat it as a distinct, higher-risk change
(real money, real API permissions) rather than flipping a flag.

## Prerequisites

1. A free Alpaca **paper trading** account: https://app.alpaca.markets/paper/dashboard/overview
2. Generate a paper API key/secret from that dashboard (not the live-trading
   keys — the dashboard clearly separates the two).
3. Set `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` in the environment or a local
   `.env` file in the repo root (git-ignored).
4. `pip install -r scripts/trading_bot/requirements.txt`

## The two-file memory system

- `scripts/trading_bot/data/ledger.log` — CSV log of every order the bot
  places or skips (timestamp, symbol, action, qty, price, reason).
- `scripts/trading_bot/data/learnings.md` — plain-English lessons, one per
  line, tagged `[SYMBOL/strategy-tag]`. Before firing a new buy signal, the
  bot checks this file for a prior loss on the same symbol+strategy and
  skips the trade if one exists.

Both files are runtime data, git-ignored, and created on first use.

This script does not automatically detect when a position closes at a loss
(that requires polling Alpaca's closed orders/positions, which isn't
implemented yet). Record a lesson yourself after reviewing a closed trade:

```bash
python3 scripts/trading_bot/bot.py learn --symbol AAPL --lesson "lost on low-volume chop, wait for volume confirmation"
```

## Usage

```bash
# One-off check: paper-trades if the SMA crossover fires right now
python3 scripts/trading_bot/bot.py run --symbol AAPL --fast 10 --slow 30 --qty 1

# Repeat on an interval
python3 scripts/trading_bot/bot.py loop --symbol AAPL --interval 60

# Review the memory files
python3 scripts/trading_bot/bot.py status
```

## What this does NOT do (yet)

- No live trading (see Scope above).
- No crypto or non-Alpaca exchanges — the video also covers Binance/Bybit/
  Pionex MCP connections for crypto, none of which are wired up here.
- No automatic backtesting via TradingView MCP, as shown in the video.
- No automatic loss detection/learning — lessons are recorded manually via
  the `learn` subcommand.
- Only a single strategy (SMA crossover). The video's broader point — that
  the memory system matters more than the specific strategy — still holds;
  swap in a different signal in `check_signal()` if needed.

If asked to extend this (add live trading, another exchange, automatic PnL
tracking), treat each as a distinct, real-world-risk change and confirm
scope with the user first, same as building this skill required.
