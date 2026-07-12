"""
=========================================================
PROJECT FALCON
Order Model
Version : 2.0
=========================================================

Represents an executable order managed by the
Execution Layer.

This model is used ONLY by the execution/backtest
subsystem.
"""

from dataclasses import dataclass, field
from datetime import datetime

from models.enums import (
    Direction,
    TradeStatus,
)


@dataclass(slots=True)
class Order:
    """
    Execution order used by the
    OrderBook and Backtest Engine.
    """

    order_id: int

    symbol: str

    side: Direction

    quantity: int

    entry_price: float

    STOPLOSS: float

    target: float

    status: TradeStatus = TradeStatus.PENDING

    filled_price: float | None = None

    exit_price: float | None = None

    pnl: float = 0.0

    remarks: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    closed_at: datetime | None = None

    entry_time: datetime | None = None