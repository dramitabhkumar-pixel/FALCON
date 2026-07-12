"""
=========================================================
PROJECT FALCON
Exit Engine Tests
=========================================================
"""

from datetime import datetime

from strategy.exit_engine import ExitEngine
from models.trade_decision import TradeDecision
from core.models import Candle
from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
)


def make_candle(
    open_price: float,
    high: float,
    low: float,
    close: float,
) -> Candle:

    return Candle(
        timestamp=datetime.now(),
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=1000,
    )


def test_LONG_STOPLOSS():

    engine = ExitEngine()

    trade = TradeDecision(
        direction=Direction.LONG,
        quantity=100,
        entry_price=100,
        STOPLOSS=95,
        target=110,
        status=TradeStatus.ACTIVE,
    )

    candle = make_candle(
        open_price=100,
        high=102,
        low=94,
        close=96,
    )

    result = engine.evaluate(trade, candle)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.STOPLOSS
    assert result.exit_price == 95


def test_LONG_target():

    engine = ExitEngine()

    trade = TradeDecision(
        direction=Direction.LONG,
        quantity=100,
        entry_price=100,
        STOPLOSS=95,
        target=110,
        status=TradeStatus.ACTIVE,
    )

    candle = make_candle(
        open_price=100,
        high=111,
        low=99,
        close=110,
    )

    result = engine.evaluate(trade, candle)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.TARGET
    assert result.exit_price == 110


def test_SHORT_STOPLOSS():

    engine = ExitEngine()

    trade = TradeDecision(
        direction=Direction.SHORT,
        quantity=100,
        entry_price=100,
        STOPLOSS=105,
        target=90,
        status=TradeStatus.ACTIVE,
    )

    candle = make_candle(
        open_price=100,
        high=106,
        low=98,
        close=105,
    )

    result = engine.evaluate(trade, candle)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.STOPLOSS
    assert result.exit_price == 105


def test_SHORT_target():

    engine = ExitEngine()

    trade = TradeDecision(
        direction=Direction.SHORT,
        quantity=100,
        entry_price=100,
        STOPLOSS=105,
        target=90,
        status=TradeStatus.ACTIVE,
    )

    candle = make_candle(
        open_price=100,
        high=101,
        low=89,
        close=90,
    )

    result = engine.evaluate(trade, candle)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.TARGET
    assert result.exit_price == 90


def test_trade_remains_open():

    engine = ExitEngine()

    trade = TradeDecision(
        direction=Direction.LONG,
        quantity=100,
        entry_price=100,
        STOPLOSS=95,
        target=110,
        status=TradeStatus.ACTIVE,
    )

    candle = make_candle(
        open_price=100,
        high=104,
        low=98,
        close=103,
    )

    result = engine.evaluate(trade, candle)

    assert result.status == TradeStatus.ACTIVE
    assert result.exit_reason == ExitReason.NONE