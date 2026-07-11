"""
=========================================================
PROJECT FALCON
Entry Engine
Version : 2.0
=========================================================

The Entry Engine is responsible for converting a
validated market setup into an executable trade.

Inputs
------
TradeSetup
ConfidenceResult

Output
------
TradeDecision

This engine performs NO market analysis.
"""

from core.base_engine import BaseEngine

from config.strategy_config import CONFIG

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision
from models.confidence_result import ConfidenceResult
from models.enums import Direction


class EntryEngine(BaseEngine):
    """
    Converts analysis results into
    a final TradeDecision.
    """

    def run(
        self,
        setup: TradeSetup,
        confidence: ConfidenceResult,
    ) -> TradeDecision:

        decision = TradeDecision()

        # ==============================================
        # Validate Inputs
        # ==============================================

        if setup is None:

            decision.reasons.append(
                "Trade setup is missing."
            )

            return decision

        if confidence is None:

            decision.reasons.append(
                "Confidence result is missing."
            )

            return decision

        if not setup.valid:

            decision.reasons.append(
                "Trade setup is invalid."
            )

            return decision

        if not confidence.valid:

            decision.reasons.append(
                "Confidence result is invalid."
            )

            return decision

        if not confidence.minimum_confidence_met:

            decision.reasons.append(
                "Minimum confidence not satisfied."
            )

            return decision

        if setup.direction not in (
            Direction.LONG,
            Direction.SHORT,
        ):

            decision.reasons.append(
                "Invalid trade direction."
            )

            return decision

        # ==============================================
        # Populate Initial Decision
        # ==============================================

        decision.direction = setup.direction

        decision.confidence_score = (
            confidence.confidence_score
        )

        entry = setup.current_price
        # ==============================================
        # Calculate Stop Loss
        # ==============================================

        if setup.direction == Direction.LONG:

            stop_loss = (
                setup.swing_low
                - (setup.atr * CONFIG.ATR_BUFFER)
            )

        else:

            stop_loss = (
                setup.swing_high
                + (setup.atr * CONFIG.ATR_BUFFER)
            )

        risk = abs(entry - stop_loss)

        if risk <= 0:

            decision.reasons.append(
                "Invalid trade risk."
            )

            return decision

        # ==============================================
        # Calculate Target
        # ==============================================

        if setup.direction == Direction.LONG:

            target = (
                entry
                + (risk * CONFIG.REWARD_RATIO)
            )

        else:

            target = (
                entry
                - (risk * CONFIG.REWARD_RATIO)
            )

        reward = abs(target - entry)

        risk_reward = round(
            reward / risk,
            2,
        )

        if (
            risk_reward
            < CONFIG.MINIMUM_RR
        ):

            decision.reasons.append(
                "Risk reward below minimum."
            )

            return decision

        # ==============================================
        # Populate Decision
        # ==============================================

        decision.entry_price = round(entry, 2)

        decision.stop_loss = round(stop_loss, 2)

        decision.target_price = round(target, 2)

        decision.risk_reward = risk_reward

        decision.quantity = (
            CONFIG.MINIMUM_POSITION_SIZE
        )
        # ==============================================
        # Final Validation
        # ==============================================

        decision.valid = True

        decision.reasons.append(
            "Trade approved."
        )

        return decision