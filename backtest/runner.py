"""
Command-line runner for backtests.

This module is a thin CLI that orchestrates loading data, running the
backtest, building equity, and writing reports. It uses `print` for high-level
CLI output while internals use logging.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from backtest.backtest_engine import BacktestEngine
from backtest.data_loader import load_csv, make_synthetic_ohlc
from backtest.equity_curve import build_equity_curve
from backtest.report_generator import generate_reports

logger = logging.getLogger("backtest.runner")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FALCON backtest runner")
    parser.add_argument("--csv", "-c", help="CSV input path", default=None)
    parser.add_argument("--symbol", "-s", default="BANKNIFTY")
    parser.add_argument("--warmup", "-w", type=int, default=50)
    parser.add_argument("--initial-capital", "-i", type=float, default=500_000)
    parser.add_argument("--out", "-o", default="journal")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )

    if args.csv:
        df = load_csv(args.csv)
    else:
        df = make_synthetic_ohlc()

    engine = BacktestEngine(df, symbol=args.symbol, warmup_bars=args.warmup, initial_capital=args.initial_capital)

    print("Running backtest...")
    metrics, trades = engine.run_full()

    equity = build_equity_curve(trades, initial_capital=args.initial_capital)
    files = generate_reports(metrics, trades, equity, out_dir=Path(args.out))

    print("Backtest complete. Summary:")
    for k, v in metrics.items():
        print(f"{k:18}: {v}")

    print("Reports:")
    for name, path in files.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
