"""
=========================================================
PROJECT FALCON
Exit Engine Tests
=========================================================
"""

from strategy.exit_engine import ExitEngine

from models.trade_decision import TradeDecision

from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
)


def test_long_target_hit():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        direction=Direction.LONG,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )

    result = engine.run(trade, 111.0)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.TARGET
    assert result.exit_price == 111.0
    assert result.pnl == 110.0


def test_long_stoploss_hit():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        direction=Direction.LONG,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )

    result = engine.run(trade, 94.0)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.STOPLOSS
    assert result.exit_price == 94.0
    assert result.pnl == -60.0


def test_short_target_hit():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        direction=Direction.SHORT,
        entry_price=100.0,
        stop_loss=105.0,
        target_price=90.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )

    result = engine.run(trade, 89.0)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.TARGET
    assert result.exit_price == 89.0
    assert result.pnl == 110.0


def test_short_stoploss_hit():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        direction=Direction.SHORT,
        entry_price=100.0,
        stop_loss=105.0,
        target_price=90.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )

    result = engine.run(trade, 106.0)

    assert result.status == TradeStatus.CLOSED
    assert result.exit_reason == ExitReason.STOPLOSS
    assert result.exit_price == 106.0
    assert result.pnl == -60.0


def test_trade_remains_active():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        direction=Direction.LONG,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )

    result = engine.run(trade, 103.0)

    assert result.status == TradeStatus.ACTIVE


def test_invalid_trade():

    engine = ExitEngine()

    trade = TradeDecision()

    result = engine.run(trade, 100.0)

    assert result.valid is False


def test_closed_trade():

    engine = ExitEngine()

    trade = TradeDecision(
        valid=True,
        status=TradeStatus.CLOSED,
    )

    result = engine.run(trade, 100.0)

    assert result.status == TradeStatus.CLOSED