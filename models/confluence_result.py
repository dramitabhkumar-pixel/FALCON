"""
=========================================================
PROJECT FALCON
Confluence Result Model
Version : 1.0
=========================================================

Represents the output of the Confluence Engine.

This model contains ONLY the confluence evaluation.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List

from models.enums import Direction


@dataclass(slots=True)
class ConfluenceResult:
    """
    Result produced by the Confluence Engine.

    This model represents whether the various
    confluence conditions required by the strategy
    have been satisfied.

    It does NOT calculate confidence, grades,
    or trading decisions.
    """

    # =====================================================
    # Trade Direction
    # =====================================================

    direction: Direction = Direction.NONE

    # =====================================================
    # Confluence Confirmations
    # =====================================================

    trend_alignment: bool = False

    structure_alignment: bool = False

    ema_alignment: bool = False

    momentum_confirmation: bool = False

    liquidity_confirmation: bool = False

    fibonacci_confirmation: bool = False

    golden_zone_confirmation: bool = False

    bos_confirmation: bool = False

    choch_confirmation: bool = False

    order_block_confirmation: bool = False

    fair_value_gap_confirmation: bool = False

    # =====================================================
    # Diagnostics
    # =====================================================

    reasons: List[str] = field(default_factory=list)

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False