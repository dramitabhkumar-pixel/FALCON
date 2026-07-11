"""
=========================================================
PROJECT FALCON
Trade Manager
Version : 1.0
=========================================================

Manages the lifecycle of all trades.

Responsibilities
----------------
- Register new trades
- Track active trades
- Update active trades
- Move closed trades
- Maintain trade history

This engine performs NO market analysis.
"""

from core.base_engine import BaseEngine

from strategy.exit_engine import ExitEngine

from models.trade_decision import TradeDecision
from models.enums import TradeStatus


class TradeManager(BaseEngine):
    """
    Maintains active and completed trades.
    """

    def __init__(self):

        self.exit_engine = ExitEngine()

        self.active_trades = []

        self.closed_trades = []

    # =====================================================
    # Open Trade
    # =====================================================

    def open_trade(
        self,
        trade: TradeDecision,
    ) -> bool:

        if trade is None:

            return False

        if not trade.valid:

            return False

        trade.status = TradeStatus.PENDING

        self.active_trades.append(trade)

        return True
    # =====================================================
    # Update Active Trades
    # =====================================================

    def update(
        self,
        current_price: float,
    ) -> None:
        """
        Updates all active trades using the Exit Engine.
        """

        remaining_trades = []

        for trade in self.active_trades:

            updated_trade = self.exit_engine.run(
                trade,
                current_price,
            )

            if updated_trade.status == TradeStatus.CLOSED:

                self.closed_trades.append(
                    updated_trade
                )

            else:

                remaining_trades.append(
                    updated_trade
                )

        self.active_trades = remaining_trades
    # =====================================================
    # Get Active Trades
    # =====================================================

    def get_active_trades(self) -> list[TradeDecision]:

        return self.active_trades

    # =====================================================
    # Get Closed Trades
    # =====================================================

    def get_closed_trades(self) -> list[TradeDecision]:

        return self.closed_trades

    # =====================================================
    # Statistics
    # =====================================================

    def active_count(self) -> int:

        return len(self.active_trades)

    def closed_count(self) -> int:

        return len(self.closed_trades)

    def total_trades(self) -> int:

        return (
            self.active_count()
            + self.closed_count()
        )