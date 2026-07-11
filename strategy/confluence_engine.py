"""
=========================================================
PROJECT FALCON
Confluence Engine
Version : 3.0 (Frozen)
=========================================================

Validates a TradeSetup and produces a ConfluenceResult.

Responsibilities
----------------
- Validate TradeSetup
- Evaluate confluence confirmations
- Produce ConfluenceResult

This engine performs NO scoring,
NO confidence calculation,
NO execution logic.

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from __future__ import annotations

from models.trade_setup import TradeSetup
from models.confluence_result import ConfluenceResult

from models.enums import (
    Trend,
    Structure,
    Direction,
)

from strategy.strategy_config import CONFIG


class ConfluenceEngine:
    """
    Validates the confluence of a TradeSetup.

    Input
    -----
    TradeSetup

    Output
    ------
    ConfluenceResult
    """

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate(
        setup: TradeSetup,
    ) -> None:
        """
        Validate engine inputs.
        """

        if setup is None:
            raise ValueError(
                "TradeSetup cannot be None."
            )

        if not setup.valid:
            raise ValueError(
                "TradeSetup is invalid."
            )

    # =====================================================
    # Trend Alignment
    # =====================================================

    @staticmethod
    def _trend_alignment(
        setup: TradeSetup,
    ) -> bool:
        """
        Validate trend alignment with trade direction.
        """

        if setup.direction == Direction.LONG:

            return (
                setup.trend
                == Trend.CONFIRMED_UPTREND
            )

        if setup.direction == Direction.SHORT:

            return (
                setup.trend
                == Trend.CONFIRMED_DOWNTREND
            )

        return False
        # =====================================================
    # Structure Alignment
    # =====================================================

    @staticmethod
    def _structure_alignment(
        setup: TradeSetup,
    ) -> bool:
        """
        Validate market structure alignment.
        """

        if setup.direction == Direction.LONG:
            return (
                setup.structure
                == Structure.BULLISH
            )

        if setup.direction == Direction.SHORT:
            return (
                setup.structure
                == Structure.BEARISH
            )

        return False

    # =====================================================
    # Momentum Confirmation
    # =====================================================

    @staticmethod
    def _momentum_confirmation(
        setup: TradeSetup,
    ) -> bool:
        """
        Validate momentum using ADX and RSI.
        """

        if setup.adx < CONFIG.ADX_MINIMUM:
            return False

        if setup.direction == Direction.LONG:
            return (
                setup.rsi >= CONFIG.RSI_LONG
            )

        if setup.direction == Direction.SHORT:
            return (
                setup.rsi <= CONFIG.RSI_SHORT
            )

        return False

    # =====================================================
    # Diagnostics
    # =====================================================

    @staticmethod
    def _collect_reasons(
        result: ConfluenceResult,
    ) -> None:
        """
        Populate diagnostic reasons.
        """

        if result.trend_alignment:
            result.reasons.append(
                "Trend aligned."
            )

        if result.structure_alignment:
            result.reasons.append(
                "Structure aligned."
            )

        if result.ema_alignment:
            result.reasons.append(
                "EMA alignment confirmed."
            )

        if result.momentum_confirmation:
            result.reasons.append(
                "Momentum confirmed."
            )

        if result.liquidity_confirmation:
            result.reasons.append(
                "Liquidity confirmed."
            )

        if result.fibonacci_confirmation:
            result.reasons.append(
                "Fibonacci confirmed."
            )

        if result.golden_zone_confirmation:
            result.reasons.append(
                "Golden Zone confirmed."
            )

        if result.bos_confirmation:
            result.reasons.append(
                "Break of Structure confirmed."
            )

        if result.choch_confirmation:
            result.reasons.append(
                "Change of Character confirmed."
            )

        if result.order_block_confirmation:
            result.reasons.append(
                "Order Block confirmed."
            )

        if result.fair_value_gap_confirmation:
            result.reasons.append(
                "Fair Value Gap confirmed."
            )

    # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        setup: TradeSetup,
    ) -> ConfluenceResult:
                """
        Evaluate the confluence of a validated TradeSetup.

        Parameters
        ----------
        setup : TradeSetup
            Validated market analysis.

        Returns
        -------
        ConfluenceResult
            Result of confluence validation.
        """

        # =====================================================
        # Validation
        # =====================================================

                self._validate(setup)

                result = ConfluenceResult()

        # =====================================================
        # Direction
        # =====================================================

                result.direction = setup.direction

        # =====================================================
        # Confluence Confirmations
        # =====================================================

                result.trend_alignment = self._trend_alignment(
            setup,
        )

                result.structure_alignment = self._structure_alignment(
            setup,
        )

                result.ema_alignment = setup.ema_alignment

                result.momentum_confirmation = (
            self._momentum_confirmation(
                setup,
            )
        )

                result.liquidity_confirmation = setup.liquidity
                result.fibonacci_confirmation = setup.fibonacci
                result.golden_zone_confirmation = setup.golden_zone

                result.bos_confirmation = setup.bos
                result.choch_confirmation = setup.choch

                result.order_block_confirmation = (
            setup.order_block
        )

                result.fair_value_gap_confirmation = (
            setup.fair_value_gap
        )

        # =====================================================
        # Diagnostics
        # =====================================================

                self._collect_reasons(result)

        # =====================================================
        # Validation
        # =====================================================

                result.valid = True

                return result

    # =====================================================
    # Callable Interface
    # =====================================================

    def __call__(
        self,
        setup: TradeSetup,
    ) -> ConfluenceResult:
        """
        Allow the engine to be called directly.
        """

        return self.evaluate(setup)