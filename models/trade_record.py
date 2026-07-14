"""
=========================================================
PROJECT FALCON
Trade Record
Version : 1.0
=========================================================

Immutable snapshot of a completed trade.

Responsibilities
----------------
• Store completed trade information
• Used by JournalWriter
• Used for reporting and analytics

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.enums import Direction, ExitReason


@dataclass(frozen=True)
class TradeRecord:
    """
    Immutable completed trade record.
    """

    trade_id: str

    symbol: str

    direction: Direction

    entry_time: datetime
    exit_time: datetime

    entry_price: float
    exit_price: float

    stop_loss: float
    target: float

    quantity: int

    pnl: float

    exit_reason: ExitReason

    confidence: float

    winner: bool