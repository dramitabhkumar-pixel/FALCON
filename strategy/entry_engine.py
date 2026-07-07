"""
=========================================================
PROJECT FALCON
Entry Engine
=========================================================

Converts a validated TradeSetup into a TradeDecision.
"""

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision


class EntryEngine:

    MIN_RISK_REWARD = 2.5

    def evaluate(self, setup: TradeSetup) -> TradeDecision:

        decision = TradeDecision()

        if setup is None:
            decision.reasons.append("Trade setup is missing")
            return decision

        # -----------------------------------------------------
        # Direction
        # -----------------------------------------------------

        direction = getattr(setup, "direction", None)

        if direction not in ("BUY", "SELL"):
            decision.reasons.append("No valid trading direction")
            return decision

        # -----------------------------------------------------
        # Prices
        # -----------------------------------------------------

        decision.signal = direction
        decision.entry_price = float(getattr(setup, "entry_price", 0.0))
        decision.stop_loss = float(getattr(setup, "stop_loss", 0.0))
        decision.target_price = float(getattr(setup, "target_price", 0.0))
        decision.confidence = float(getattr(setup, "confidence", 0.0))

        # -----------------------------------------------------
        # Basic Validation
        # -----------------------------------------------------

        if decision.entry_price <= 0:
            decision.reasons.append("Invalid entry price")
            return decision

        if decision.stop_loss <= 0:
            decision.reasons.append("Invalid stop loss")
            return decision

        if decision.target_price <= 0:
            decision.reasons.append("Invalid target price")
            return decision

        # -----------------------------------------------------
        # Risk / Reward
        # -----------------------------------------------------

        risk = abs(decision.entry_price - decision.stop_loss)
        reward = abs(decision.target_price - decision.entry_price)

        if risk <= 0:
            decision.reasons.append("Invalid Stop Loss")
            return decision

        decision.risk_reward = round(reward / risk, 2)

        if decision.risk_reward < self.MIN_RISK_REWARD:
            decision.reasons.append(
                f"Risk Reward below {self.MIN_RISK_REWARD:.1f}"
            )
            return decision

        # -----------------------------------------------------
        # Passed
        # -----------------------------------------------------

        decision.valid = True
        decision.reasons.append("Entry conditions satisfied")

        return decision