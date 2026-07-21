"""
=========================================================
PROJECT FALCON
Confluence Result Model
Version : 2.0
=========================================================

Represents the output of the Confluence Engine.

Contains ONLY confluence evaluation.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List

from models.enums import Direction


@dataclass(slots=True)
class ConfluenceResult:
    """
    Result produced by the Confluence Engine.
    """

    # =====================================================
    # Trade Direction
    # =====================================================

    direction: Direction = Direction.NONE

    # =====================================================
    # Confluence Confirmations
    # =====================================================

    

    adx_confirmation: bool = False

    rsi_confirmation: bool = False

    atr_confirmation: bool = False

    liquidity_confirmation: bool = False

    golden_zone_confirmation: bool = False

    

    daily_bias_confirmation: bool = False
    

    # =====================================================
    # Diagnostics
    # =====================================================

    reasons: List[str] = field(default_factory=list)

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False
