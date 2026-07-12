"""
Command-line runner for backtests.
"""

from __future__ import annotations

import argparse
import logging

from backtest.backtest_engine import BacktestEngine
from backtest.data_loader import load_csv, make_synthetic_ohlc

logger = logging.getLogger("backtest.runner")


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Run FALCON backtest runner"
    )

    parser.add_argument("--csv", "-c", default=None)
    parser.add_argument("--days", "-d", type=int, default=None)
    parser.add_argument("--symbol", "-s", default="BANKNIFTY")
    parser.add_argument("--warmup", "-w", type=int, default=50)
    parser.add_argument("--initial-capital", "-i", type=float, default=500000)
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )

    if args.csv:

        df = load_csv(
            args.csv,
            last_days=args.days,
        )

    else:

        if args.days is not None:

            raise ValueError(
                "--days may only be used with --csv"
            )

        df = make_synthetic_ohlc()

    print("Running backtest...")

    engine = BacktestEngine()

    trades = engine.run(
        dataframe=df,
        symbol=args.symbol,
    )

    print(f"Trades generated: {len(trades)}")


if __name__ == "__main__":
    main()