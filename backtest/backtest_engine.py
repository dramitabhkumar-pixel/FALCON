"""
Main backtest engine for Project FALCON.
Supports StrategyConfig for parameter optimization.
"""

from __future__ import annotations

import pandas as pd

from backtest.candle_feed import BacktestCandleFeed
from backtest.data_loader import (
    load_csv,
    make_synthetic_ohlc,
    normalize_columns,
)
from backtest.performance import compute_metrics
from backtest.strategy_runner import StrategyRunner
from backtest.trade_engine import BacktestTradeEngine

from config.strategy_config import StrategyConfig


class BacktestEngine:
    """
    Walk-forward Backtest Engine.

    Every run uses one StrategyConfig object.
    This makes parameter optimization possible.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        config: StrategyConfig | None = None,
        symbol: str = "BANKNIFTY",
        warmup_bars: int = 50,
        initial_capital: float = 500_000,
    ):

        self.df = normalize_columns(df)

        self.symbol = symbol
        self.warmup_bars = warmup_bars
        self.initial_capital = initial_capital

        # ------------------------------------------------
        # Strategy Configuration
        # ------------------------------------------------
        self.config = config or StrategyConfig()

        # ------------------------------------------------
        # Strategy Runner
        # ------------------------------------------------
        self.strategy = StrategyRunner(
            config=self.config
        )

        # ------------------------------------------------
        # Trade Engine
        # ------------------------------------------------
        self.trade_engine = BacktestTradeEngine(
            symbol=symbol
        )

    @classmethod
    def from_csv(
        cls,
        path: str,
        config: StrategyConfig | None = None,
        symbol: str = "BANKNIFTY",
        warmup_bars: int = 50,
        initial_capital: float = 500_000,
    ):

        return cls(
            load_csv(path),
            config=config,
            symbol=symbol,
            warmup_bars=warmup_bars,
            initial_capital=initial_capital,
        )

    def run(self) -> dict:

        feed = BacktestCandleFeed(
            self.df,
            warmup_bars=self.warmup_bars,
        )

        signals = 0
        entries = 0

        for window, bar in feed:

            self.trade_engine.on_bar(bar)

            setup = self.strategy.evaluate(window)

            if setup is None:
                continue

            signals += 1

            order = self.trade_engine.try_entry(
    side=setup.side,
    entry=setup.entry,
    stop_loss=setup.stop_loss,
    target=setup.target,
    entry_time=bar.name,
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

        # Strategy Parameters
        metrics["ema_fast"] = self.config.ema_fast
        metrics["ema_slow"] = self.config.ema_slow
        metrics["adx_threshold"] = self.config.adx_threshold
        metrics["rsi_buy"] = self.config.rsi_buy
        metrics["reward_ratio"] = self.config.reward_ratio

        return metrics

    def run_verbose(self) -> dict:

        result = self.run()

        print("=" * 60)
        print("PROJECT FALCON BACKTEST")
        print("=" * 60)

        for key, value in result.items():
            print(f"{key:20}: {value}")

        print("=" * 60)

        return result

    def run_full(self) -> tuple[dict, pd.DataFrame]:
        """
        Returns:

            metrics,
            trade_history_dataframe
        """

        result = self.run()

        history_df = self.trade_engine.history.to_dataframe()

        return result, history_df


def run_backtest(
    df: pd.DataFrame | None = None,
    csv_path: str | None = None,
    config: StrategyConfig | None = None,
    symbol: str = "BANKNIFTY",
    warmup_bars: int = 50,
):

    if csv_path is not None:

        engine = BacktestEngine.from_csv(
            csv_path,
            config=config,
            symbol=symbol,
            warmup_bars=warmup_bars,
        )

    elif df is not None:

        engine = BacktestEngine(
            df,
            config=config,
            symbol=symbol,
            warmup_bars=warmup_bars,
        )

    else:

        engine = BacktestEngine(
            make_synthetic_ohlc(),
            config=config,
            symbol=symbol,
            warmup_bars=warmup_bars,
        )

    return engine.run()


if __name__ == "__main__":

    config = StrategyConfig()

    BacktestEngine(
        make_synthetic_ohlc(),
        config=config,
    ).run_verbose()