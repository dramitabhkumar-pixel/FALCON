"""
=========================================================
PROJECT FALCON
Trade Manager
Version : 1.0
=========================================================

Coordinates EntryEngine and ExitEngine.

Responsibilities
----------------
• Create new trades
• Manage active trades
• Maintain a single active trade

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations

from core.base_engine import BaseEngine
from core.candles import Candle

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision
from models.confidence_result import ConfidenceResult

from strategy.entry_engine import EntryEngine
from strategy.exit_engine import ExitEngine
from models.enums import TradeStatus

class TradeManager(BaseEngine):
    """
    Coordinates the complete trade lifecycle.
    """

    def __init__(self):

        super().__init__()

        self.entry_engine = EntryEngine()
        self.exit_engine = ExitEngine()

        self.active_trade: TradeDecision | None = None

    # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        setup: TradeSetup,
        confidence: ConfidenceResult,
        candle: Candle,
        symbol: str = "",
    ) -> TradeDecision | None:
        """
        Manage the complete trade lifecycle.

        Returns:
            Active TradeDecision or None.
        """

        # -------------------------------------------------
        # Existing Trade
        # -------------------------------------------------

        if self.active_trade is not None:

            self.active_trade = self.exit_engine.evaluate(
                trade=self.active_trade,
                candle=candle,
            )

            if self.active_trade.status == TradeStatus.CLOSED:
                completed_trade = self.active_trade

                self.active_trade = None

                return completed_trade

            return self.active_trade

        # -------------------------------------------------
        # New Trade
        # -------------------------------------------------

        decision = self.entry_engine.evaluate(
            setup=setup,
            confidence=confidence,
            candle=candle,
            symbol=symbol,
        )
        print("\n========== ENTRY ENGINE ==========")
        print("Decision :", decision)
        if decision is not None:
             print("Status   :", decision.status)
        else:
             print("Status   : None")
        print("=================================\n")

        if decision.status == TradeStatus.ACTIVE:

            self.active_trade = decision

            return decision
        

        return None
    
    # =====================================================
    # Utilities
    # =====================================================

    def has_active_trade(self) -> bool:
        """
        Returns True if there is an active trade.
        """
        return self.active_trade is not None

    def reset(self) -> None:
        """
        Reset the trade manager.
        Useful for backtesting.
        """
        self.active_trade = None