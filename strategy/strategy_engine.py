"""
=========================================================
PROJECT FALCON
Strategy Engine
Version : 2.0
=========================================================

Coordinates the complete strategy workflow.

TradeSetup
    ↓
Confluence Engine
    ↓
Confidence Engine
    ↓
Trade Manager
    ↓
Trade Decision

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations

from core.candles import Candle

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision

from strategy.confluence_engine import ConfluenceEngine
from strategy.confidence_engine import ConfidenceEngine
from strategy.trade_manager import TradeManager


class StrategyEngine:
    """
    Main strategy orchestrator.

    Coordinates the strategy engines without
    implementing trading logic.
    """

    def __init__(self):

        self.confluence_engine = ConfluenceEngine()
        self.confidence_engine = ConfidenceEngine()
        self.trade_manager = TradeManager()

    # =====================================================
    # Public API
    # =====================================================

    def process(
        self,
        setup: TradeSetup,
        candle: Candle,
        symbol: str = "",
    ) -> TradeDecision | None:
        """
        Execute the complete strategy pipeline.
        """

        # -------------------------------------------------
        # Confluence
        # -------------------------------------------------

        confluence = self.confluence_engine.evaluate(
            setup,
        )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence = self.confidence_engine.evaluate(
            confluence,
        )

        # -------------------------------------------------
        # Trade Management
        # -------------------------------------------------

        decision = self.trade_manager.evaluate(
            setup=setup,
            confidence=confidence,
            candle=candle,
            symbol=symbol,
        )

        return decision