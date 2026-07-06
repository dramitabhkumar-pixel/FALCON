"""
=========================================================
PROJECT FALCON
Trade State
=========================================================
"""

from enum import Enum


class TradeState(Enum):
    WAITING = "WAITING"
    READY = "READY"
    OPEN = "OPEN"
    BREAKEVEN = "BREAKEVEN"
    TRAILING = "TRAILING"
    PARTIAL_EXIT = "PARTIAL_EXIT"
    TARGET_HIT = "TARGET_HIT"
    STOP_LOSS = "STOP_LOSS"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"