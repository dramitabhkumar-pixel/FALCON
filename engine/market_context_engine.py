"""
=========================================================
PROJECT FALCON
Market Context Engine
Version : 3.1 (Frozen)
=========================================================

Updates the shared MarketContext using IndicatorResult.

Responsibilities
----------------
- Update Indicator State
- Determine Trend
- Determine Strength
- Determine Bias

Produces an updated MarketContext for downstream
analysis engines.

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from __future__ import annotations

from models.indicator_result import IndicatorResult
from models.market_context import MarketContext

from models.enums import (
    Trend,
    Bias,
    Strength,
)

from strategy.strategy_config import CONFIG


class MarketContextEngine:
    """
    Updates the shared MarketContext from the latest
    IndicatorResult.

    This engine performs no indicator calculations.
    """

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate(
        context: MarketContext,
        indicators: IndicatorResult,
    ) -> None:
        """
        Validate engine inputs.
        """

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

    # =====================================================
    # Trend
    # =====================================================

    @staticmethod
    def _determine_trend(
        indicators: IndicatorResult,
    ) -> Trend:
        
        """
        Determine overall market trend from EMA alignment.
        """

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
        """
        Determine trend strength using ADX.
        """

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
        """
        Determine directional market bias.
        """

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
        """
        Copy indicator values into MarketContext.
        """

        state = context.indicators

        state.ema_fast = indicators.ema_fast
        state.ema_slow = indicators.ema_slow
        state.rsi = indicators.rsi
        state.adx = indicators.adx
        state.atr = indicators.atr
        state.volume = indicators.volume

    # =====================================================
    # Trend State
    # =====================================================

    @staticmethod
    def _update_trend_state(
        context: MarketContext,
        indicators: IndicatorResult,
    ) -> None:
        """
        Update trend-related information.
        """

        trend = MarketContextEngine._determine_trend(
            indicators
        )

        strength = MarketContextEngine._determine_strength(
            indicators
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
        
            """
        Update the shared MarketContext using the latest
        IndicatorResult.

        Parameters
        ----------
        context : MarketContext
            Shared market state.

        indicators : IndicatorResult
            Latest validated indicator calculations.

        Returns
        -------
        MarketContext
            Updated market context.
        """

        # =====================================================
        # Validation
        # =====================================================

            self._validate(
            context,
            indicators,
        )

        # =====================================================
        # Indicator State
        # =====================================================

            self._update_indicator_state(
            context,
            indicators,
        )

        # =====================================================
        # Trend State
        # =====================================================

            self._update_trend_state(
            context,
            indicators,
        )

        # =====================================================
        # Return Updated Context
        # =====================================================

            return context