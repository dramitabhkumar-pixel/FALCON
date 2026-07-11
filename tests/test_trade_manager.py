"""
=========================================================
PROJECT FALCON
Trade Manager Tests
=========================================================
"""

from strategy.trade_manager import TradeManager

from models.trade_decision import TradeDecision

from models.enums import (
    Direction,
    TradeStatus,
)


def create_trade():

    return TradeDecision(
        valid=True,
        direction=Direction.LONG,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        quantity=10,
        status=TradeStatus.PENDING,
    )


def test_open_trade():

    manager = TradeManager()

    trade = create_trade()

    assert manager.open_trade(trade)

    assert manager.active_count() == 1

    assert manager.closed_count() == 0


def test_trade_remains_active():

    manager = TradeManager()

    trade = create_trade()

    manager.open_trade(trade)

    manager.update(103.0)

    assert manager.active_count() == 1

    assert manager.closed_count() == 0


def test_trade_hits_target():

    manager = TradeManager()

    trade = create_trade()

    manager.open_trade(trade)

    manager.update(111.0)

    assert manager.active_count() == 0

    assert manager.closed_count() == 1


def test_trade_hits_stoploss():

    manager = TradeManager()

    trade = create_trade()

    manager.open_trade(trade)

    manager.update(94.0)

    assert manager.active_count() == 0

    assert manager.closed_count() == 1


def test_invalid_trade():

    manager = TradeManager()

    trade = TradeDecision()

    assert manager.open_trade(trade) is False

    assert manager.active_count() == 0