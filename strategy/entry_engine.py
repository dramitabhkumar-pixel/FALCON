"""
=========================================================
PROJECT FALCON
Entry Engine
Version : 4.0
=========================================================

Converts a validated TradeSetup and ConfidenceResult
into a TradeDecision.

Responsibilities
----------------
• Validate inputs
• Calculate stop loss
• Calculate target
• Calculate risk/reward
• Build TradeDecision

This engine performs NO market analysis,
NO trade management and NO exit logic.
=========================================================
"""

from __future__ import annotations


from uuid import uuid4

from config.strategy_config import CONFIG

from core.candles import Candle
from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision
from models.confidence_result import ConfidenceResult

from models.enums import (
    Direction,
    TradeStatus,
)


class EntryEngine:
    """
    Produces a TradeDecision from a validated
    TradeSetup and ConfidenceResult.
    """

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate(
        setup: TradeSetup,
        confidence: ConfidenceResult,
    ) -> None:
        """
        Validate engine inputs.
        """

        if setup is None:
            raise ValueError(
                "TradeSetup cannot be None."
            )

        if confidence is None:
            raise ValueError(
                "ConfidenceResult cannot be None."
            )

    # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        setup: TradeSetup,
        confidence: ConfidenceResult,
        candle: Candle,
        symbol: str = "",
    ) -> TradeDecision:
        """
        Create a TradeDecision from validated
        analysis results.
        """

        self._validate(
            setup,
            confidence,
        )

        decision = TradeDecision()

        # -------------------------------------------------
        # Business Validation
        # -------------------------------------------------

        if not setup.valid:
            return decision

        if not confidence.valid:
            return decision

        if not confidence.minimum_confidence_met:
            return decision

        if setup.direction not in (
            Direction.LONG,
            Direction.SHORT,
        ):
            return decision

        # -------------------------------------------------
        # Calculate Levels
        # -------------------------------------------------

        entry_price = setup.current_price

        stop_loss = self._calculate_stop_loss(
            setup,
        )

        risk = abs(
            entry_price - stop_loss
        )

        if risk <= 0:
            return decision

        target = self._calculate_target(
            direction=setup.direction,
            entry_price=entry_price,
            risk=risk,
        )

        reward = abs(
            target - entry_price
        )

        risk_reward = round(
            reward / risk,
            2,
        )

        if (
            risk_reward
            < CONFIG.MINIMUM_RR
        ):
            return decision

        # -------------------------------------------------
        # Populate Decision
        # -------------------------------------------------

        decision.trade_id = str(
            uuid4()
        )

        decision.symbol = symbol

        decision.direction = (
            setup.direction
        )

        decision.quantity = (
            CONFIG.MINIMUM_POSITION_SIZE
        )

        decision.entry_price = round(
            entry_price,
            2,
        )

        decision.entry_time = candle.timestamp

        decision.stop_loss = round(
            stop_loss,
            2,
        )      

        decision.target = round(
            target,
            2,
        )

        decision.risk_reward = risk_reward

        decision.confidence_score = (
            confidence.confidence_score
        )

        decision.confidence_grade = (
            confidence.grade
        )

        decision.trend = setup.trend

        decision.structure = (
            setup.structure
        )

        decision.confluence = (
            confidence.confidence_score
        )

        decision.status = (
            TradeStatus.ACTIVE
        )

        return decision

    # =====================================================
    # Stop Loss
    # =====================================================

    def _calculate_stop_loss(
        self,
        setup: TradeSetup,
    ) -> float:
        """
        Calculate initial stop loss.
        """

        if setup.direction == Direction.LONG:

            return (
                setup.swing_low
                - (
                    setup.atr
                    * CONFIG.ATR_MULTIPLIER
                )
            )

        return (
            setup.swing_high
            + (
                setup.atr
                * CONFIG.ATR_MULTIPLIER
            )
        )
    # =====================================================
    # Target
    # =====================================================

    def _calculate_target(
        self,
        direction: Direction,
        entry_price: float,
        risk: float,
    ) -> float:
        """
        Calculate profit target from the configured
        risk-reward ratio.
        """

        if direction == Direction.LONG:

            return (
                entry_price
                + (
                    risk
                    * CONFIG.REWARD_RATIO
                )
            )

        return (
            entry_price
            - (
                risk
                * CONFIG.REWARD_RATIO
            )
        )

    # =====================================================
    # Callable Interface
    # =====================================================

    def __call__(
        self,
        setup: TradeSetup,
        confidence: ConfidenceResult,
        candle: Candle,
        symbol: str = "",
    ) -> TradeDecision:
        """
        Callable interface.
        """

        return self.evaluate(
           setup=setup,
           confidence=confidence,
           candle=candle,
           symbol=symbol,
    )