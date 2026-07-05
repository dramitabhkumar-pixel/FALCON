import argparse

from backtest.backtest_engine import BacktestEngine
from backtest.data_loader import make_synthetic_ohlc


def main():
    parser = argparse.ArgumentParser(description="Run FALCON backtest")
    parser.add_argument("--csv", "-c", help="Path to CSV file for OHLC data", default=None)
    parser.add_argument("--symbol", "-s", help="Symbol name", default="BANKNIFTY")
    parser.add_argument("--warmup", "-w", type=int, help="Warmup bars", default=50)
    parser.add_argument("--initial-capital", "-i", type=float, help="Initial capital", default=500_000)
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.csv:
        engine = BacktestEngine.from_csv(
            args.csv,
            symbol=args.symbol,
            warmup_bars=args.warmup,
            initial_capital=args.initial_capital,
        )
    else:
        engine = BacktestEngine(
            make_synthetic_ohlc(),
            symbol=args.symbol,
            warmup_bars=args.warmup,
            initial_capital=args.initial_capital,
        )

    if args.verbose:
        engine.run_verbose()
    else:
        res = engine.run()
        print(res)


if __name__ == "__main__":
    main()
