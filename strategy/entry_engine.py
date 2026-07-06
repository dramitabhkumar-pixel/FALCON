"""
=========================================================
PROJECT FALCON
Entry Engine
=========================================================
"""

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision


class EntryEngine:

    MIN_RISK_REWARD = 2.5

    def evaluate(self, setup: TradeSetup) -> TradeDecision:

        decision = TradeDecision()

        # Direction
        if setup.direction not in ("BUY", "SELL"):
            decision.reasons.append("No valid trading direction")
            return decision

        decision.signal = setup.direction
        decision.entry_price = setup.entry_price
        decision.stop_loss = setup.stop_loss
        decision.target_price = setup.target_price
        decision.confidence = setup.confidence

        risk = abs(decision.entry_price - decision.stop_loss)
        reward = abs(decision.target_price - decision.entry_price)

        if risk <= 0:
            decision.reasons.append("Invalid Stop Loss")
            return decision

        decision.risk_reward = reward / risk

        if decision.risk_reward < self.MIN_RISK_REWARD:
            decision.reasons.append(
                f"Risk Reward below {self.MIN_RISK_REWARD}"
            )
            return decision

        decision.valid = True
        decision.reasons.append("Entry conditions satisfied")

        return decision