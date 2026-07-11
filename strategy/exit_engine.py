"""
=========================================================
PROJECT FALCON
Exit Engine
Version : 1.0
=========================================================

The Exit Engine monitors an active trade and
determines whether the trade should remain active
or be closed.

Inputs
------
TradeDecision
Current Market Price

Output
------
Updated TradeDecision

This engine performs NO market analysis.
"""

from core.base_engine import BaseEngine

from models.trade_decision import TradeDecision

from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
)


class ExitEngine(BaseEngine):
    """
    Handles trade exits.
    """

    def run(
        self,
        trade: TradeDecision,
        current_price: float,
    ) -> TradeDecision:

        # ==================================================
        # Validation
        # ==================================================

        if trade is None:

            return TradeDecision()

        if not trade.valid:

            return trade

        if trade.status == TradeStatus.CLOSED:

            return trade

        if current_price <= 0:

            trade.reasons.append(
                "Invalid market price."
            )

            return trade

        # ==================================================
        # Trade becomes Active
        # ==================================================

        if trade.status == TradeStatus.PENDING:

            trade.status = TradeStatus.ACTIVE

                # ==================================================
        # LONG Position
        # ==================================================

        if trade.direction == Direction.LONG:

            if current_price <= trade.stop_loss:

                trade.status = TradeStatus.CLOSED

                trade.exit_reason = ExitReason.STOPLOSS

                trade.exit_price = current_price

                trade.pnl = (
                    (current_price - trade.entry_price)
                    * trade.quantity
                )

                trade.reasons.append(
                    "Stop Loss hit."
                )

                return trade

            if current_price >= trade.target_price:

                trade.status = TradeStatus.CLOSED

                trade.exit_reason = ExitReason.TARGET

                trade.exit_price = current_price

                trade.pnl = (
                    (current_price - trade.entry_price)
                    * trade.quantity
                )

                trade.reasons.append(
                    "Target achieved."
                )

                return trade

        # ==================================================
        # SHORT Position
        # ==================================================

        elif trade.direction == Direction.SHORT:

            if current_price >= trade.stop_loss:

                trade.status = TradeStatus.CLOSED

                trade.exit_reason = ExitReason.STOPLOSS

                trade.exit_price = current_price

                trade.pnl = (
                    (trade.entry_price - current_price)
                    * trade.quantity
                )

                trade.reasons.append(
                    "Stop Loss hit."
                )

                return trade

            if current_price <= trade.target_price:

                trade.status = TradeStatus.CLOSED

                trade.exit_reason = ExitReason.TARGET

                trade.exit_price = current_price

                trade.pnl = (
                    (trade.entry_price - current_price)
                    * trade.quantity
                )

                trade.reasons.append(
                    "Target achieved."
                )

                return trade
        # ==================================================
        # Trade Continues
        # ==================================================

        trade.reasons.append(
            "Trade remains active."
        )

        return trade