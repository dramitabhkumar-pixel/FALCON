"""
=========================================================
PROJECT FALCON
Strategy Runner
Version : 4.0
=========================================================

Historical replay adapter for Project FALCON.

Responsibilities
----------------
• Accept rolling historical DataFrame
• Calculate indicators
• Build TradeSetup
• Build current Candle
• Execute StrategyEngine
• Return TradeDecision | None

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from core.candles import Candle

from models.trade_decision import TradeDecision

from engine.indicator_engine import IndicatorEngine
from strategy.setup_builder import SetupBuilder
from strategy.strategy_engine import StrategyEngine
from strategy.strategy_config import CONFIG



class StrategyRunner:
    """
    Thin adapter between the Backtest Engine and the
    frozen Project FALCON strategy pipeline.
    """

    def __init__(self) -> None:

        self.indicator_engine = IndicatorEngine()
        self.setup_builder = SetupBuilder()
        self.strategy_engine = StrategyEngine()
        

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate incoming rolling dataframe.
        """

        if dataframe is None:
            raise ValueError(
                "Rolling dataframe cannot be None."
            )

        if dataframe.empty:
            raise ValueError(
                "Rolling dataframe is empty."
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

                f"Missing required columns: {missing}"

            )

        minimum = max(

            CONFIG.SLOW_EMA,

            CONFIG.ADX_PERIOD,

            CONFIG.ATR_PERIOD,

            CONFIG.RSI_PERIOD,

            50,

        )

        if len(dataframe) < minimum:

            raise ValueError(

                f"Need at least {minimum} candles."

            )

    @staticmethod
    def _normalize(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize dataframe column names.
        """

        df = dataframe.copy()

        df.columns = [

            str(column).lower()

            for column in df.columns

        ]

        return df

    @staticmethod
    def _build_candle(
        dataframe: pd.DataFrame,
    ) -> Candle:
        """
        Convert latest row into Candle model.
        """

        row = dataframe.iloc[-1]

        timestamp = None

        if "timestamp" in dataframe.columns:

            timestamp = row["timestamp"]

        elif "datetime" in dataframe.columns:

            timestamp = row["datetime"]

        elif dataframe.index.dtype.kind == "M":

            timestamp = dataframe.index[-1]

        else:

            raise ValueError(

                "No timestamp/datetime column found."

            )

        volume = 0.0

        if "volume" in dataframe.columns:

            volume = float(row["volume"])

        return Candle(

            timestamp=timestamp,

            open=float(row["open"]),

            high=float(row["high"]),

            low=float(row["low"]),

            close=float(row["close"]),

            volume=volume,

        )

    # =====================================================
    # Public API
    # =====================================================

    def process(
        self,
        dataframe: pd.DataFrame,
        symbol: str = "",
    ) -> Optional[TradeDecision]:
        """
        Execute one historical strategy evaluation.

        Parameters
        ----------
        dataframe
            Rolling OHLCV dataframe ending at the
            current historical candle.

        symbol
            Trading symbol.

        Returns
        -------
        TradeDecision | None
        """

        try:

            # ---------------------------------------------
            # Validation
            # ---------------------------------------------

            self._validate_dataframe(
                dataframe,
            )

            df = self._normalize(
                dataframe,
            )

            # ---------------------------------------------
            # Indicator Analysis
            # ---------------------------------------------

            indicator = self.indicator_engine.analyze(
                df,
            )

            if not indicator.valid:
                return None

            # ---------------------------------------------
            # Current Price
            # ---------------------------------------------

            close = float(
                df.iloc[-1]["close"]
            )

            # ---------------------------------------------
            # Build Trade Setup
            # ---------------------------------------------

            setup = self.setup_builder.build(

               dataframe=df,
               ema_fast=indicator.ema_fast,
               ema_slow=indicator.ema_slow,
               rsi=indicator.rsi,
               adx=indicator.adx,
               atr=indicator.atr,
               avg_atr=indicator.avg_atr,
               volume=indicator.volume,
               close=close,
            )
               

               

               
            
            if setup is None:
                return None

            if not setup.valid:
                return None

            # ---------------------------------------------
            # Current Candle
            # ---------------------------------------------

            candle = self._build_candle(
                df,
            )

            # ---------------------------------------------
            # Execute Strategy
            # ---------------------------------------------

            decision = self.strategy_engine.process(

                setup=setup,

                candle=candle,

                symbol=symbol,

            )

            # ---------------------------------------------
            # Result
            # ---------------------------------------------

            return decision

        except Exception:
            import traceback
            traceback.print_exc()


            

            return None