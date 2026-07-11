"""
=========================================================
PROJECT FALCON
Strategy Engine
Version : 1.0
=========================================================

Coordinates the complete strategy workflow.

TradeSetup
    ↓
Confluence Engine
    ↓
Confidence Engine
    ↓
Entry Engine
    ↓
Trade Manager
    ↓
Trade Decision

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from engine.confluence_engine import ConfluenceEngine
from strategy.confidence_engine import ConfidenceEngine
from strategy.entry_engine import EntryEngine
from strategy.trade_manager import TradeManager


class StrategyEngine:
    """
    Main strategy orchestrator.

    This engine contains NO trading logic.
    It only coordinates the individual strategy engines.
    """

    def __init__(self):

        self.confluence_engine = ConfluenceEngine()
        self.confidence_engine = ConfidenceEngine()
        self.entry_engine = EntryEngine()
        self.trade_manager = TradeManager()

    def process(self, setup):
        """
        Execute the complete strategy pipeline.

        Parameters
        ----------
        setup : TradeSetup

        Returns
        -------
        TradeDecision
        """

        # ---------------------------------------------
        # Confluence
        # ---------------------------------------------
        confluence = self.confluence_engine.evaluate(setup)

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------
        confidence = self.confidence_engine.calculate(setup)

        # ---------------------------------------------
        # Entry
        # ---------------------------------------------
        decision = self.entry_engine.run(
            setup,
            confidence
        )
        return decision