"""
=========================================================
PROJECT FALCON
Indicator Engine
Version : 2.0
=========================================================

Calculates all technical indicators required by
Project FALCON.

Input
-----
OHLCV DataFrame

Output
------
IndicatorResult

Architecture
------------
DataFrame
      ↓
Indicator Engine
      ↓
IndicatorResult
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from models.indicator_result import IndicatorResult
from strategy.strategy_config import CONFIG


class IndicatorEngine:
    """
    Calculates all primary indicators used by
    Project FALCON.
    """

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        df: pd.DataFrame,
    ) -> None:

        if df is None:
            raise ValueError("DataFrame cannot be None.")

        if df.empty:
            raise ValueError("DataFrame is empty.")

        required = [
            "open",
            "high",
            "low",
            "close",
        ]

        columns = [c.lower() for c in df.columns]

        missing = [
            column
            for column in required
            if column not in columns
        ]

        if missing:

            raise ValueError(
                f"Missing required columns: {missing}"
            )

        if len(df) < max(
            CONFIG.SLOW_EMA,
            CONFIG.ATR_PERIOD,
            CONFIG.RSI_PERIOD,
            CONFIG.ADX_PERIOD,
            50,
        ):

            raise ValueError(
                "Insufficient candles for indicator calculation."
            )

    # =====================================================
    # EMA
    # =====================================================

    @staticmethod
    def _ema(
        series: pd.Series,
        period: int,
    ) -> pd.Series:

        return (
            series
            .ewm(
                span=period,
                adjust=False,
            )
            .mean()
        )

    # =====================================================
    # RSI
    # =====================================================

    @staticmethod
    def _rsi(
        close: pd.Series,
        period: int,
    ) -> pd.Series:

        delta = close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = (
            gain
            .rolling(period)
            .mean()
        )

        avg_loss = (
            loss
            .rolling(period)
            .mean()
        )

        rs = avg_gain / avg_loss.replace(0, np.nan)

        rsi = 100 - (100 / (1 + rs))

        return rsi.fillna(50)

    # =====================================================
    # ATR
    # =====================================================

    @staticmethod
    def _atr(
        df: pd.DataFrame,
        period: int,
    ) -> pd.Series:

        high = df["high"]

        low = df["low"]

        close = df["close"]

        previous_close = close.shift(1)

        tr1 = high - low

        tr2 = (high - previous_close).abs()

        tr3 = (low - previous_close).abs()

        tr = pd.concat(
            [
                tr1,
                tr2,
                tr3,
            ],
            axis=1,
        ).max(axis=1)

        return (
            tr
            .rolling(period)
            .mean()
        )

    # =====================================================
    # ADX
    # =====================================================

    @staticmethod
    def _adx(
        df: pd.DataFrame,
        period: int,
    ) -> pd.Series:       
    
        high = df["high"]

        low = df["low"]

        plus_dm = high.diff()

        minus_dm = -low.diff()

        plus_dm = plus_dm.where(
            (plus_dm > minus_dm) &
            (plus_dm > 0),
            0.0,
        )

        minus_dm = minus_dm.where(
            (minus_dm > plus_dm) &
            (minus_dm > 0),
            0.0,
        )

        atr = IndicatorEngine._atr(
            df,
            period,
        )

        plus_di = (
            100
            * plus_dm.rolling(period).sum()
            / atr.replace(0, np.nan)
        )

        minus_di = (
            100
            * minus_dm.rolling(period).sum()
            / atr.replace(0, np.nan)
        )

        dx = (
            (
                (plus_di - minus_di).abs()
                /
                (plus_di + minus_di)
            )
            * 100
        )

        adx = (
            dx
            .rolling(period)
            .mean()
        )

        return adx.fillna(0)

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _latest(
        series: pd.Series,
        default: float = 0.0,
    ) -> float:

        value = series.iloc[-1]

        if pd.isna(value):

            return default

        return float(value)

    @staticmethod
    def _average_atr(
        atr: pd.Series,
        period: int = 50,
    ) -> float:

        valid = atr.dropna()

        if valid.empty:

            return 0.0

        return float(
            valid.tail(period).mean()
        )

    # =====================================================
    # Public API
    # =====================================================

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> IndicatorResult:

        self._validate_dataframe(df)

        df = df.copy()

        df.columns = [
            column.lower()
            for column in df.columns
        ]
        self._validate_dataframe(df)

        ema_fast_series = self._ema(
            df["close"],
            CONFIG.FAST_EMA,
        )

        ema_slow_series = self._ema(
            df["close"],
            CONFIG.SLOW_EMA,
        )

        rsi_series = self._rsi(
            df["close"],
            CONFIG.RSI_PERIOD,
        )

        atr_series = self._atr(
            df,
            CONFIG.ATR_PERIOD,
        )

        adx_series = self._adx(
            df,
            CONFIG.ADX_PERIOD,
        )

        avg_atr = self._average_atr(
            atr_series,
        )

        ema_fast = self._latest(
            ema_fast_series,
        )

        ema_slow = self._latest(
            ema_slow_series,
        )

        rsi = self._latest(
            rsi_series,
            50.0,
        )

        atr = self._latest(
            atr_series,
        )

        adx = self._latest(
            adx_series,
        )

        volume = 0.0

        if "volume" in df.columns:

            try:

                volume = float(
                    df["volume"].iloc[-1]
                )

            except Exception:

                volume = 0.0

            ema_alignment = (
            ema_fast > ema_slow
        )

        high_volatility = (
            atr >= avg_atr
        )

        return IndicatorResult(

            # =================================================
            # Moving Averages
            # =================================================

            ema_fast=round(
                ema_fast,
                4,
            ),

            ema_slow=round(
                ema_slow,
                4,
            ),

            ema_alignment=ema_alignment,

            # =================================================
            # Momentum
            # =================================================

            rsi=round(
                rsi,
                2,
            ),

            adx=round(
                adx,
                2,
            ),

            # =================================================
            # Volatility
            # =================================================

            atr=round(
                atr,
                4,
            ),

            avg_atr=round(
                avg_atr,
                4,
            ),

            high_volatility=high_volatility,

            # =================================================
            # Volume
            # =================================================

            volume=volume,

            # =================================================
            # Validation
            # =================================================

            valid=True,

        )   