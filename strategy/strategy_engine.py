"""
=========================================================
PROJECT FALCON
Strategy Engine
=========================================================

Master Strategy Pipeline
"""

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision

from strategy.signal_engine import SignalEngine
from strategy.filters import TradeFilter
from strategy.confidence_engine import ConfidenceEngine
from strategy.entry_engine import EntryEngine


class StrategyEngine:

    def __init__(self):

        self.signal_engine = SignalEngine()
        self.filter_engine = TradeFilter()
        self.confidence_engine = ConfidenceEngine()
        self.entry_engine = EntryEngine()

    # =====================================================

    def process(self, setup: TradeSetup) -> TradeDecision | None:

        print("\n==============================")
        print("PROJECT FALCON STRATEGY ENGINE")
        print("==============================")

        if setup is None:
            print("❌ Trade setup missing.")
            return None

        # -------------------------------------------------
        # SIGNAL ENGINE
        # -------------------------------------------------

        signal = self.signal_engine.generate(setup)
        print("\n===== SIGNAL DEBUG =====")
        print("Trend        :", setup.trend)
        print("Structure    :", setup.structure)
        print("EMA Align    :", setup.ema_alignment)
        print("BOS          :", setup.bos)
        print("CHOCH        :", setup.choch)
        print("Golden Zone  :", setup.golden_zone)
        print("========================")

        setup.direction = signal.signal

        print(f"\nSignal     : {signal.signal}")

        if signal.reasons:
            print("Reasons:")
            for reason in signal.reasons:
                print(f"  ✓ {reason}")

        if signal.signal == "NONE":
            print("\n❌ No valid trading signal.")
            return None

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        filters = self.filter_engine.evaluate(setup)

        print("\nFilter Check")

        if not filters.passed:

            print("FAILED")

            for reason in filters.reasons:
                print(f"  ✗ {reason}")

            return None

        print("PASSED")

        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = self.confidence_engine.calculate(setup)

        setup.confidence = confidence.score

        print("\nConfidence")
        print(f"Score       : {confidence.score:.2f}")
        print(f"Grade       : {confidence.grade}")
        print(f"Confidence  : {confidence.confidence}")
        print(f"Qualified   : {'YES' if confidence.passed else 'NO'}")

        if confidence.reasons:
            print("\nConfidence Reasons")
            for reason in confidence.reasons:
                print(f"  ✓ {reason}")

        # -------------------------------------------------
        # ENTRY ENGINE
        # -------------------------------------------------

        decision = self.entry_engine.evaluate(setup)

        print("\nEntry Engine")

        if decision.valid:
            print("Trade Accepted")
        else:
            print("Trade Rejected")

        if decision.reasons:
            print("\nReasons")
            for reason in decision.reasons:
                print(f"  • {reason}")

        return decision