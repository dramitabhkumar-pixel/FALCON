"""
=========================================================
PROJECT FALCON
Trade Decision Model
Version : 3.0
=========================================================

Represents the final trading decision produced
by the Entry Engine and managed by the Trademanager.

This model contains ONLY trade state.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from models.enums import ConfidenceGrade

confidence_grade: ConfidenceGrade = ConfidenceGrade.D
from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
    Trend,
    Structure,
)


@dataclass(slots=True)
class TradeDecision:
    """
    Represents a live trade throughout its lifecycle.

    Created by:
        EntryEngine

    Updated by:
        ExitEngine

    Consumed by:
        StrategyEngine
        StrategyRunner
        BacktestEngine
        Journal
    """

    # =====================================================
    # Identity
    # =====================================================

    trade_id: str = ""
    symbol: str = ""

    # =====================================================
    # Trade
    # =====================================================

    direction: Direction = Direction.NONE
    quantity: int = 0

    # =====================================================
    # Entry
    # =====================================================

    entry_price: float = 0.0
    entry_time: datetime | None = None

    # =====================================================
    # Risk Management
    # =====================================================

    stop_loss: float = 0.0
    target: float = 0.0
    risk_reward: float = 0.0

    # =====================================================
    # Confidence
    # =====================================================

    confidence_score: int = 0
    confidence_grade: str = ""

    # =====================================================
    # Market Snapshot
    # =====================================================

    trend: Trend = Trend.UNKNOWN
    structure: Structure = Structure.UNKNOWN
    confluence: int = 0

    # =====================================================
    # Runtime State
    # =====================================================

    status: TradeStatus = TradeStatus.PENDING

    exit_price: float = 0.0
    exit_time: datetime | None = None
    exit_reason: ExitReason = ExitReason.NONE

    # =====================================================
    # Performance
    # =====================================================

    pnl: float = 0.0
    pnl_points: float = 0.0
    pnl_percent: float = 0.0

    # =====================================================
    # Trade Management
    # =====================================================

    highest_price: float = 0.0
    lowest_price: float = 0.0
    trailing_stop: float = 0.0

    # =====================================================
    # Journal
    # =====================================================

    notes: str = ""
    tags: List[str] = field(default_factory=list)