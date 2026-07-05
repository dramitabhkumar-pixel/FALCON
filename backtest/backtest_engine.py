"""
Main backtest engine for Project FALCON.
"""

from __future__ import annotations

import pandas as pd

from backtest.candle_feed import BacktestCandleFeed
from backtest.data_loader import load_csv, make_synthetic_ohlc, normalize_columns
from backtest.performance import compute_metrics
from backtest.strategy_runner import StrategyRunner
from backtest.trade_engine import BacktestTradeEngine


class BacktestEngine:
    """Walk-forward backtest over historical OHLC data."""

    def __init__(
        self,
        df: pd.DataFrame,
        symbol: str = "BANKNIFTY",
        warmup_bars: int = 50,
        initial_capital: float = 500_000,
    ):
        self.df = normalize_columns(df)
        self.symbol = symbol
        self.warmup_bars = warmup_bars
        self.initial_capital = initial_capital

        self.strategy = StrategyRunner()
        self.trade_engine = BacktestTradeEngine(symbol=symbol)

    @classmethod
    def from_csv(
        cls,
        path: str,
        symbol: str = "BANKNIFTY",
        warmup_bars: int = 50,
        initial_capital: float = 500_000,
    ):
        return cls(
            load_csv(path),
            symbol=symbol,
            warmup_bars=warmup_bars,
            initial_capital=initial_capital,
        )

    def run(self) -> dict:
        feed = BacktestCandleFeed(self.df, warmup_bars=self.warmup_bars)
        signals = 0
        entries = 0

        for window, bar in feed:
            self.trade_engine.on_bar(bar, entry_time=bar.name)

            setup = self.strategy.evaluate(window)
            if setup is None:
                continue

            signals += 1

            order = self.trade_engine.try_entry(
                side=setup.side,
                entry=setup.entry,
                stop_loss=setup.stop_loss,
                target=setup.target,
            )

            if order is not None:
                entries += 1

        metrics = compute_metrics(
            self.trade_engine.history.to_dataframe(),
            initial_capital=self.initial_capital,
        )
        metrics["signals"] = signals
        metrics["entries"] = entries
        metrics["symbol"] = self.symbol
        metrics["bars_processed"] = len(self.df) - self.warmup_bars

        return metrics

    def run_verbose(self) -> dict:
        result = self.run()
        print("=" * 50)
        print("FALCON BACKTEST RESULTS")
        print("=" * 50)
        for key, value in result.items():
            print(f"{key:18}: {value}")
        print("=" * 50)
        return result


def run_backtest(
    df: pd.DataFrame | None = None,
    csv_path: str | None = None,
    symbol: str = "BANKNIFTY",
    warmup_bars: int = 50,
) -> dict:
    """Convenience helper to run a backtest from CSV or dataframe."""

    if csv_path is not None:
        engine = BacktestEngine.from_csv(
            csv_path,
            symbol=symbol,
            warmup_bars=warmup_bars,
        )
    elif df is not None:
        engine = BacktestEngine(
            df,
            symbol=symbol,
            warmup_bars=warmup_bars,
        )
    else:
        engine = BacktestEngine(
            make_synthetic_ohlc(),
            symbol=symbol,
            warmup_bars=warmup_bars,
        )

    return engine.run()


if __name__ == "__main__":
    BacktestEngine(make_synthetic_ohlc()).run_verbose()
