"""
=========================================================
PROJECT FALCON
Trade Decision Model
Version : 3.0
=========================================================

Represents the final trading decision produced
by the Entry Engine and managed by the Exit Engine.

This model contains ONLY trade state.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List

from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
)


@dataclass(slots=True)
class TradeDecision:
    """
    Final trade decision produced by the
    Strategy Layer.
    """

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False

    # =====================================================
    # Trade Direction
    # =====================================================

    direction: Direction = Direction.NONE

    # =====================================================
    # Trade Parameters
    # =====================================================

    entry_price: float = 0.0

    stop_loss: float = 0.0

    target_price: float = 0.0

    risk_reward: float = 0.0

    quantity: int = 0

    confidence_score: int = 0

    # =====================================================
    # Trade Lifecycle
    # =====================================================

    status: TradeStatus = TradeStatus.PENDING

    exit_reason: ExitReason = ExitReason.NONE

    exit_price: float = 0.0

    pnl: float = 0.0

    # =====================================================
    # Diagnostics
    # =====================================================

    reasons: List[str] = field(default_factory=list)