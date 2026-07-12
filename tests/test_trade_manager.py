"""
=========================================================
PROJECT FALCON
Trade Manager Tests
Version : 1.0
=========================================================
"""

from datetime import datetime

from strategy.trade_manager import TradeManager

from core.candles import Candle

from models.trade_setup import TradeSetup
from models.trade_decision import TradeDecision
from models.confidence_result import ConfidenceResult

from models.enums import (
    Direction,
    TradeStatus,
    Trend,
    Structure,
    ConfidenceGrade,
)


# =====================================================
# Helpers
# =====================================================

def make_candle():

    return Candle(
        timestamp=datetime.now(),
        open=100,
        high=102,
        low=98,
        close=101,
        volume=1000,
    )


def make_setup():

    setup = TradeSetup()

    setup.valid = True
    setup.direction = Direction.LONG
    setup.current_price = 100
    setup.swing_low = 95
    setup.swing_high = 105
    setup.atr = 2

    setup.trend = Trend.CONFIRMED_UPTREND
    setup.structure = Structure.BULLISH

    return setup


def make_confidence():

    confidence = ConfidenceResult()

    confidence.valid = True
    confidence.minimum_confidence_met = True
    confidence.confidence_score = 95
    confidence.grade = ConfidenceGrade.A_PLUS

    return confidence


# =====================================================
# Tests
# =====================================================

def test_create_new_trade():

    manager = TradeManager()

    trade = manager.evaluate(
        setup=make_setup(),
        confidence=make_confidence(),
        candle=make_candle(),
        symbol="BANKNIFTY",
    )

    assert trade is not None
    assert trade.status == TradeStatus.ACTIVE


def test_has_active_trade():

    manager = TradeManager()

    manager.evaluate(
        setup=make_setup(),
        confidence=make_confidence(),
        candle=make_candle(),
        symbol="BANKNIFTY",
    )

    assert manager.has_active_trade()


def test_reset():

    manager = TradeManager()

    manager.evaluate(
        setup=make_setup(),
        confidence=make_confidence(),
        candle=make_candle(),
        symbol="BANKNIFTY",
    )

    manager.reset()

    assert manager.has_active_trade() is False


def test_invalid_setup_returns_none():

    manager = TradeManager()

    setup = make_setup()
    setup.valid = False

    trade = manager.evaluate(
        setup=setup,
        confidence=make_confidence(),
        candle=make_candle(),
        symbol="BANKNIFTY",
    )

    assert trade is None


def test_close_trade():

    manager = TradeManager()

    trade = manager.evaluate(
        setup=make_setup(),
        confidence=make_confidence(),
        candle=make_candle(),
        symbol="BANKNIFTY",
    )

    assert trade is not None

    exit_candle = Candle(
        timestamp=datetime.now(),
        open=100,
        high=125,
        low=99,
        close=122,
        volume=1000,
    )

    result = manager.evaluate(
        setup=make_setup(),
        confidence=make_confidence(),
        candle=exit_candle,
        symbol="BANKNIFTY",
    )

    assert result.status == TradeStatus.CLOSED
    assert manager.has_active_trade() is False