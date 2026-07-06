"""
=========================================================
PROJECT FALCON
Exit Engine
=========================================================
"""

from models.trade_decision import TradeDecision


class ExitEngine:

    def should_exit(
        self,
        trade: TradeDecision,
        current_price: float
    ):

        if trade.signal == "BUY":

            if current_price >= trade.target_price:
                return True, "TARGET"

            if current_price <= trade.stop_loss:
                return True, "STOP_LOSS"

        elif trade.signal == "SELL":

            if current_price <= trade.target_price:
                return True, "TARGET"

            if current_price >= trade.stop_loss:
                return True, "STOP_LOSS"

        return False, "HOLD"