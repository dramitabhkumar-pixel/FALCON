"""
=========================================================
PROJECT FALCON
Market Context Engine
Version : 3.0
=========================================================

Updates the shared MarketContext using the latest
IndicatorResult.

Input
-----
MarketContext
IndicatorResult

Output
------
Updated MarketContext
"""

from __future__ import annotations

from models.indicator_result import IndicatorResult
from models.market_context import MarketContext
from models.enums import (
    Bias,
    Strength,
    Trend,
)
from strategy.strategy_config import CONFIG


class MarketContextEngine:
    """
    Updates the shared MarketContext using the latest
    calculated IndicatorResult.
    """

    # =====================================================
    # Trend
    # =====================================================

    @staticmethod
    def _determine_trend(
        indicators: IndicatorResult,
    ) -> Trend:

        if indicators.ema_fast > indicators.ema_slow:
            return Trend.CONFIRMED_UPTREND

        if indicators.ema_fast < indicators.ema_slow:
            return Trend.CONFIRMED_DOWNTREND

        return Trend.RANGE

    # =====================================================
    # Strength
    # =====================================================

    @staticmethod
    def _determine_strength(
        indicators: IndicatorResult,
    ) -> Strength:

        if indicators.adx >= CONFIG.ADX_MINIMUM:
            return Strength.STRONG

        return Strength.NORMAL

    # =====================================================
    # Bias
    # =====================================================

    @staticmethod
    def _determine_bias(
        trend: Trend,
        indicators: IndicatorResult,
    ) -> Bias:

        if (
            trend == Trend.CONFIRMED_UPTREND
            and indicators.rsi >= CONFIG.RSI_LONG
        ):
            return Bias.BULLISH

        if (
            trend == Trend.CONFIRMED_DOWNTREND
            and indicators.rsi <= CONFIG.RSI_SHORT
        ):
            return Bias.BEARISH

        return Bias.NEUTRAL

    # =====================================================
    # Indicator State
    # =====================================================

    @staticmethod
    def _update_indicator_state(
        context: MarketContext,
        indicators: IndicatorResult,
    ) -> None:

        context.indicators.ema_fast = indicators.ema_fast
        context.indicators.ema_slow = indicators.ema_slow
        context.indicators.rsi = indicators.rsi
        context.indicators.adx = indicators.adx
        context.indicators.atr = indicators.atr
        context.indicators.volume = indicators.volume

    # =====================================================
    # Trend State
    # =====================================================

    @staticmethod
    def _update_trend_state(
        context: MarketContext,
        indicators: IndicatorResult,
    ) -> None:

        trend = MarketContextEngine._determine_trend(
            indicators,
        )

        strength = MarketContextEngine._determine_strength(
            indicators,
        )

        bias = MarketContextEngine._determine_bias(
            trend,
            indicators,
        )

        context.trend.trend = trend
        context.trend.strength = strength
        context.trend.bias = bias

    # =====================================================
    # Public API
    # =====================================================

    def analyze(
        self,
        context: MarketContext,
        indicators: IndicatorResult,
    ) -> MarketContext:
                if context is None:
                 raise ValueError(
                "MarketContext cannot be None."
            )

                if indicators is None:
                 raise ValueError(
                "IndicatorResult cannot be None."
            )

                if not indicators.valid:
                 raise ValueError(
                "IndicatorResult is invalid."
            )

        # =================================================
        # Update Indicator State
        # =================================================

                self._update_indicator_state(
            context,
            indicators,
        )

        # =================================================
        # Update Trend State
        # =================================================

                self._update_trend_state(
            context,
            indicators,
        )

                return context