"""
=========================================================
PROJECT FALCON
Strategy Runner

Backtest Integration Layer

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
RunnerDecision
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


# ==========================================================
# Runner Decision
# ==========================================================

@dataclass
class RunnerDecision:
    """
    Returned to BacktestEngine.
    """

    side: OrderSide

    entry: float

    stop_loss: float

    target: float

    confidence: float = 0.0


# ==========================================================
# Strategy Runner
# ==========================================================

class StrategyRunner:

    """
    Integrates every strategy component.

    Historical Window
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
    RunnerDecision
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

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _prepare_dataframe(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        IndicatorEngine expects lowercase OHLC columns.
        """

        working = df.copy()

        working.columns = [
            str(c).lower()
            for c in working.columns
        ]

        return working

    @staticmethod
    def _convert_swings(
        swings_df: pd.DataFrame,
    ) -> list[dict]:

        """
        Convert Swing dataframe into
        LiquidityEngine input.
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

    # =====================================================
    # Main Evaluation
    # =====================================================

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
            # Indicator Engine
            # ------------------------------------------

            indicators = self.indicators.analyze(
                working
            )

            # ------------------------------------------
            # Swing Engine
            # (Used only for Liquidity Engine)
            # ------------------------------------------

            swings_df = self.swing_engine.run(
                window
            )

            swing_list = self._convert_swings(
                swings_df
            )

            # ------------------------------------------
            # Liquidity Engine
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

            # ------------------------------------------
            # Setup Builder
            # ------------------------------------------

            setup = self.builder.build(

                dataframe=window,

                ema_fast=indicators.ema_fast,

                ema_slow=indicators.ema_slow,

                rsi=indicators.rsi,

                adx=indicators.adx,

                atr=indicators.atr,

                avg_atr=indicators.avg_atr,

                volume=indicators.volume,

                close=float(
                    latest["Close"]
                ),

                liquidity=liquidity,
            )

            if not setup.valid:
                return None

            # ------------------------------------------
            # Strategy Engine
            # ------------------------------------------

            decision = self.strategy.process(
                setup
            )

            if decision is None:
                return None

            if not decision.valid:
                return None

            # ------------------------------------------
            # Convert Signal
            # ------------------------------------------

            signal = str(
                decision.signal
            ).upper()

            if signal == "BUY":

                side = OrderSide.BUY

            elif signal == "SELL":

                side = OrderSide.SELL

            else:

                return None

            # ------------------------------------------
            # Return to Backtest Engine
            # ------------------------------------------

            return RunnerDecision(

                side=side,

                entry=float(
                    decision.entry_price
                ),

                stop_loss=float(
                    decision.stop_loss
                ),

                target=float(
                    decision.target_price
                ),

                confidence=float(
                    decision.confidence
                ),
            )

        except Exception as exc:

            print(
                f"[StrategyRunner] Error: {exc}"
            )

            return None