"""
=========================================================
PROJECT FALCON
Indicator Engine
Version : 2.1
=========================================================

Calculates all technical indicators required by
Project FALCON.

Changes from V2.0
-----------------
- Added ATR Moving Average support
- Added atr_expanding output
- Removed average ATR helper
- Removed duplicate dataframe validation
- Compatible with updated IndicatorResult
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from models.indicator_result import IndicatorResult
from strategy.strategy_config import CONFIG


class IndicatorEngine:

    @staticmethod
    def _validate_dataframe(df: pd.DataFrame) -> None:
        if df is None:
            raise ValueError("DataFrame cannot be None.")
        if df.empty:
            raise ValueError("DataFrame is empty.")

        df.columns = [c.lower() for c in df.columns]

        required = ["open", "high", "low", "close"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        minimum = max(
            CONFIG.SLOW_EMA,
            CONFIG.RSI_PERIOD,
            CONFIG.ADX_PERIOD,
            CONFIG.ATR_PERIOD,
            CONFIG.ATR_MA_PERIOD,
            50,
        )

        if len(df) < minimum:
            raise ValueError("Insufficient candles for indicator calculation.")

    @staticmethod
    def _ema(series: pd.Series, period: int) -> pd.Series:
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def _rsi(close: pd.Series, period: int) -> pd.Series:
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        return (100 - (100 / (1 + rs))).fillna(50)

    @staticmethod
    def _atr(df: pd.DataFrame, period: int) -> pd.Series:
        high = df["high"]
        low = df["low"]
        close = df["close"]
        prev = close.shift(1)
        tr = pd.concat(
            [(high-low), (high-prev).abs(), (low-prev).abs()],
            axis=1
        ).max(axis=1)
        return tr.rolling(period).mean()

    @staticmethod
    def _atr_ma(atr: pd.Series, period: int) -> pd.Series:
        return atr.rolling(period).mean()

    @staticmethod
    def _adx(df: pd.DataFrame, period: int) -> pd.Series:
        high = df["high"]
        low = df["low"]

        plus_dm = high.diff()
        minus_dm = -low.diff()

        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

        atr = IndicatorEngine._atr(df, period)

        plus_di = 100 * plus_dm.rolling(period).sum() / atr.replace(0, np.nan)
        minus_di = 100 * minus_dm.rolling(period).sum() / atr.replace(0, np.nan)

        dx = ((plus_di - minus_di).abs() / (plus_di + minus_di)) * 100
        return dx.rolling(period).mean().fillna(0)

    @staticmethod
    def _latest(series: pd.Series, default: float = 0.0) -> float:
        value = series.iloc[-1]
        if pd.isna(value):
            return default
        return float(value)

    def analyze(self, df: pd.DataFrame) -> IndicatorResult:
        df = df.copy()
        self._validate_dataframe(df)

        ema_fast_series = self._ema(df["close"], CONFIG.FAST_EMA)
        ema_slow_series = self._ema(df["close"], CONFIG.SLOW_EMA)
        rsi_series = self._rsi(df["close"], CONFIG.RSI_PERIOD)
        atr_series = self._atr(df, CONFIG.ATR_PERIOD)
        atr_ma_series = self._atr_ma(atr_series, CONFIG.ATR_MA_PERIOD)
        adx_series = self._adx(df, CONFIG.ADX_PERIOD)

        ema_fast = self._latest(ema_fast_series)
        ema_slow = self._latest(ema_slow_series)
        rsi = self._latest(rsi_series, 50.0)
        atr = self._latest(atr_series)
        atr_ma = self._latest(atr_ma_series)
        adx = self._latest(adx_series)

        return IndicatorResult(
            ema_fast=round(ema_fast, 4),
            ema_slow=round(ema_slow, 4),
            ema_alignment=ema_fast > ema_slow,
            rsi=round(rsi, 2),
            adx=round(adx, 2),
            atr=round(atr, 4),
            atr_ma=round(atr_ma, 4),
            atr_expanding=atr > atr_ma,
            valid=True,
        )
