"""
==========================================================
FALCON INDICATOR ENGINE
Version : 1.0

Calculates

• EMA Fast
• EMA Slow
• RSI
• ATR
• ADX
• Average ATR

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from core.base_engine import BaseEngine
from core.models import IndicatorResult

from config.indicator_config import (
    EMA_FAST,
    EMA_SLOW,
    RSI_PERIOD,
    ATR_PERIOD,
    ADX_PERIOD,
)


class IndicatorEngine(BaseEngine):

    """
    Computes all primary technical indicators
    required by Project FALCON.

    Input
    -----
    OHLC DataFrame

    Output
    ------
    IndicatorResult
    """

    def __init__(self):

        super().__init__()

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_dataframe(
        self,
        df: pd.DataFrame
    ) -> None:

        required = [
            "open",
            "high",
            "low",
            "close",
        ]

        missing = []

        for column in required:

            if column not in df.columns:

                missing.append(column)

        if missing:

            raise ValueError(
                f"Missing OHLC columns : {missing}"
            )

        if len(df) < 50:

            raise ValueError(
                "Minimum 50 candles required."
            )

    # ---------------------------------------------------------
    # EMA
    # ---------------------------------------------------------

    def _ema(
        self,
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

    # ---------------------------------------------------------
    # ATR
    # ---------------------------------------------------------

    def _atr(
        self,
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
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        atr = (
            tr
            .rolling(period)
            .mean()
        )

        return atr

    # ---------------------------------------------------------
    # RSI
    # ---------------------------------------------------------

    def _rsi(
        self,
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
    
    # ---------------------------------------------------------
    # ADX
    # ---------------------------------------------------------

    def _adx(
        self,
        df: pd.DataFrame,
        period: int,
    ) -> pd.Series:

        high = df["high"]
        low = df["low"]

        plus_dm = high.diff()
        minus_dm = -low.diff()

        plus_dm = plus_dm.where(
            (plus_dm > minus_dm) & (plus_dm > 0),
            0.0,
        )

        minus_dm = minus_dm.where(
            (minus_dm > plus_dm) & (minus_dm > 0),
            0.0,
        )

        atr = self._atr(df, period)

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

    # ---------------------------------------------------------
    # Average ATR
    # ---------------------------------------------------------

    def _average_atr(
        self,
        atr: pd.Series,
        period: int = 50,
    ) -> float:

        valid = atr.dropna()

        if len(valid) == 0:
            return 0.0

        return float(
            valid.tail(period).mean()
        )

    # ---------------------------------------------------------
    # Latest Value
    # ---------------------------------------------------------

    def _latest(
        self,
        series: pd.Series,
        default: float = 0.0,
    ) -> float:

        value = series.iloc[-1]

        if pd.isna(value):
            return default

        return float(value)
    
    # ---------------------------------------------------------
    # ANALYZE
    # ---------------------------------------------------------

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> IndicatorResult:

        self.log("Running Indicator Engine")

        self._validate_dataframe(df)

        df = df.copy()
        df.columns = [c.lower() for c in df.columns]

        # -------------------------------------------------
        # EMA
        # -------------------------------------------------

        ema_fast_series = self._ema(
            df["close"],
            EMA_FAST,
        )

        ema_slow_series = self._ema(
            df["close"],
            EMA_SLOW,
        )

        # -------------------------------------------------
        # RSI
        # -------------------------------------------------

        rsi_series = self._rsi(
            df["close"],
            RSI_PERIOD,
        )

        # -------------------------------------------------
        # ATR
        # -------------------------------------------------

        atr_series = self._atr(
            df,
            ATR_PERIOD,
        )

        avg_atr = self._average_atr(
            atr_series
        )

        # -------------------------------------------------
        # ADX
        # -------------------------------------------------

        adx_series = self._adx(
            df,
            ADX_PERIOD,
        )

        # -------------------------------------------------
        # Latest Values
        # -------------------------------------------------

        ema_fast = self._latest(ema_fast_series)

        ema_slow = self._latest(ema_slow_series)

        rsi = self._latest(
            rsi_series,
            default=50.0,
        )

        atr = self._latest(atr_series)

        adx = self._latest(adx_series)

        volume = 0.0

        if "volume" in df.columns:

            try:

                volume = float(
                    df["volume"].iloc[-1]
                )

            except Exception:

                volume = 0.0

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        return IndicatorResult(

            ema_fast=round(
                ema_fast,
                4,
            ),

            ema_slow=round(
                ema_slow,
                4,
            ),

            rsi=round(
                rsi,
                2,
            ),

            adx=round(
                adx,
                2,
            ),

            atr=round(
                atr,
                4,
            ),

            avg_atr=round(
                avg_atr,
                4,
            ),

            volume=volume,
        )