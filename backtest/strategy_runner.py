"""
=========================================================
PROJECT FALCON
Strategy Runner

Backtest Integration Layer

Bridges

Historical Replay
        ↓
Indicator Engine
        ↓
Swing Engine
        ↓
Liquidity Engine
        ↓
Setup Builder
        ↓
Strategy Engine
        ↓
Trade Decision
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from enums import OrderSide

from config.strategy_config import StrategyConfig

from engine.indicator_engine import IndicatorEngine
from engine.swing_engine import SwingEngine
from engine.liquidity_engine import LiquidityEngine

from strategy.setup_builder import SetupBuilder
from strategy.strategy_engine import StrategyEngine


@dataclass
class RunnerDecision:
    """
    Adapter returned to BacktestEngine.
    """

    side: OrderSide

    entry: float

    stop_loss: float

    target: float

    confidence: float = 0.0


class StrategyRunner:

    """
    Integrates all strategy components.

    evaluate(window)

        ↓

    RunnerDecision | None
    """

    def __init__(
        self,
        config: StrategyConfig | None = None,
    ):

        self.config = config or StrategyConfig()

        self.indicators = IndicatorEngine()

        self.swing_engine = SwingEngine()

        self.liquidity_engine = LiquidityEngine()

        self.builder = SetupBuilder()

        self.strategy = StrategyEngine()

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _prepare_dataframe(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        IndicatorEngine expects lowercase columns.
        """

        working = df.copy()

        working.columns = [
            c.lower()
            for c in working.columns
        ]

        return working

    @staticmethod
    def _convert_swings(
        swings_df: pd.DataFrame,
    ) -> list[dict]:

        """
        Convert SwingEngine dataframe
        into LiquidityEngine format.
        """

        if swings_df is None:

            return []

        if swings_df.empty:

            return []

        swings = []

        for _, row in swings_df.iterrows():

            swings.append(

                {
                    "type": str(
                        row["Type"]
                    ).upper(),

                    "price": float(
                        row["Price"]
                    ),
                }

            )

        return swings
    # ======================================================
    # Main Evaluation
    # ======================================================

    def evaluate(
        self,
        window: pd.DataFrame,
    ) -> RunnerDecision | None:

        if window is None or window.empty:
            return None

        try:

            # ------------------------------------------
            # Prepare dataframe
            # ------------------------------------------

            working = self._prepare_dataframe(window)

            # ------------------------------------------
            # Indicators
            # ------------------------------------------

            indicators = self.indicators.analyze(
                working
            )

            # ------------------------------------------
            # Swing Detection
            # ------------------------------------------

            swings_df = self.swing_engine.run(
                window
            )

            swing_list = self._convert_swings(
                swings_df
            )

            # ------------------------------------------
            # Liquidity
            # ------------------------------------------

            liquidity_result = self.liquidity_engine.analyze(
                swing_list
            )

            if liquidity_result.buy_side_liquidity:
                liquidity = "BUY_SIDE"

            elif liquidity_result.sell_side_liquidity:
                liquidity = "SELL_SIDE"

            else:
                liquidity = "NONE"

            # ------------------------------------------
            # Latest Candle
            # ------------------------------------------

            latest = window.iloc[-1]

            setup = self.builder.build(

                ema_fast=indicators.ema_fast,

                ema_slow=indicators.ema_slow,

                rsi=indicators.rsi,

                adx=indicators.adx,

                atr=indicators.atr,

                avg_atr=indicators.avg_atr,

                volume=indicators.volume,

                high=float(latest["High"]),

                low=float(latest["Low"]),

                close=float(latest["Close"]),

                swings=swings_df,

                liquidity=liquidity,
            )

            if not setup.valid:
                return None

            decision = self.strategy.process(
                setup
            )

            if decision is None:
                return None

            if not decision.valid:
                return None

            if decision.signal == "BUY":
                side = OrderSide.BUY

            elif decision.signal == "SELL":
                side = OrderSide.SELL

            else:

                        return RunnerDecision(
                side=side,
                entry=float(decision.entry_price),
                stop_loss=float(decision.stop_loss),
                target=float(decision.target_price),
                confidence=float(decision.confidence),
            )

        except Exception as exc:

            print(
                f"[StrategyRunner] Error : {exc}"
            )

            return None
                