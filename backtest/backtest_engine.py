"""
=========================================================
PROJECT FALCON
Backtest Engine
Version : 4.0
=========================================================

Historical replay engine for Project FALCON.

Responsibilities
----------------
• Replay historical candles
• Feed rolling DataFrame to StrategyRunner
• Collect TradeDecision objects
• Compute performance metrics

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations


from typing import List

import pandas as pd

from models.trade_decision import TradeDecision

from backtest.strategy_runner import StrategyRunner
from strategy.strategy_config import CONFIG


class BacktestEngine:
    """
    Historical replay engine.

    Replays candles sequentially through the
    frozen Project FALCON strategy pipeline.
    """

    def __init__(self) -> None:

        self.runner = StrategyRunner()

        self.trade_log: List[TradeDecision] = []

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate historical dataframe.
        """

        if dataframe is None:
            raise ValueError(
                "Historical dataframe cannot be None."
            )

        if dataframe.empty:
            raise ValueError(
                "Historical dataframe is empty."
            )

        dataframe.columns = [
            str(column).lower()
            for column in dataframe.columns
        ]

        required = [
            "open",
            "high",
            "low",
            "close",
        ]

        missing = [

            column

            for column in required

            if column not in dataframe.columns

        ]

        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )

    @staticmethod
    def _normalize(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize dataframe columns.
        """

        df = dataframe.copy()

        df.columns = [

            str(column).lower()

            for column in df.columns

        ]

        return df

    @staticmethod
    def _minimum_bars() -> int:
        """
        Minimum candles before strategy evaluation.
        """

        return max(

            CONFIG.SLOW_EMA,

            CONFIG.ADX_PERIOD,

            CONFIG.ATR_PERIOD,

            CONFIG.RSI_PERIOD,

            50,

        )

    # =====================================================
    # Public API
    # =====================================================

    def run(
      self,
      dataframe: pd.DataFrame,
      symbol: str = "",
) -> List[TradeDecision]:
    
        """
        Execute a historical backtest.

        Parameters
        ----------
        dataframe
            Historical OHLCV dataframe.

        symbol
            Trading symbol.

        Returns
        -------
        list[TradeDecision]
        """

        self._validate_dataframe(
            dataframe,
        )

        df = self._normalize(
            dataframe,
        )

        self.trade_log.clear()

        minimum = self._minimum_bars()

        # -------------------------------------------------
        # Historical Replay
        # -------------------------------------------------

        for index in range(

            minimum,

            len(df),

        ):

            history = df.iloc[
                : index + 1
            ].copy()

            decision = self.runner.process(

                dataframe=history,

                symbol=symbol,

            )

            if decision is None:

                continue

            self.trade_log.append(

                decision

            )

        return self.trade_log