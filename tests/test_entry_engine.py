"""
=========================================================
PROJECT FALCON
Entry Engine Tests
=========================================================
"""

from strategy.entry_engine import EntryEngine

from models.trade_setup import TradeSetup
from models.confidence_result import ConfidenceResult
from models.enums import Direction


def test_buy_trade():

    engine = EntryEngine()

    setup = TradeSetup(
        valid=True,
        direction=Direction.LONG,
        current_price=100.0,
        swing_low=95.0,
        atr=2.0,
    )

    confidence = ConfidenceResult(
        confidence_score=90,
        minimum_confidence_met=True,
        valid=True,
    )

    decision = engine.run(setup, confidence)

    assert decision.valid is True

    assert decision.direction == Direction.LONG

    assert decision.entry_price == 100.0

    assert decision.STOPLOSS == 93.0

    assert decision.target_price == 117.5

    assert decision.risk_reward == 2.5


def test_sell_trade():

    engine = EntryEngine()

    setup = TradeSetup(
        valid=True,
        direction=Direction.SHORT,
        current_price=100.0,
        swing_high=105.0,
        atr=2.0,
    )

    confidence = ConfidenceResult(
        confidence_score=95,
        minimum_confidence_met=True,
        valid=True,
    )

    decision = engine.run(setup, confidence)

    assert decision.valid is True

    assert decision.direction == Direction.SHORT

    assert decision.entry_price == 100.0

    assert decision.STOPLOSS == 107.0

    assert decision.target_price == 82.5

    assert decision.risk_reward == 2.5


def test_reject_low_confidence():

    engine = EntryEngine()

    setup = TradeSetup(
        valid=True,
        direction=Direction.LONG,
        current_price=100.0,
        swing_low=95.0,
        atr=2.0,
    )

    confidence = ConfidenceResult(
        confidence_score=70,
        minimum_confidence_met=False,
        valid=True,
    )

    decision = engine.run(setup, confidence)

    assert decision.valid is False


def test_invalid_setup():

    engine = EntryEngine()

    setup = TradeSetup()

    confidence = ConfidenceResult()

    decision = engine.run(setup, confidence)

    assert decision.valid is False