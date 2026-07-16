"""
=========================================================
PROJECT FALCON
Confidence Result Model
Version : 2.1 (Frozen)
=========================================================

Represents the output of the Confidence Engine.

Contains ONLY confidence evaluation.
No business logic.
No trading logic.

FROZEN ARCHITECTURE
"""

from dataclasses import dataclass, field
from typing import Dict, List

from models.enums import ConfidenceGrade


@dataclass(slots=True)
class ConfidenceResult:
    """
    Result produced by the Confidence Engine.
    """

    # =====================================================
    # CONFIDENCE
    # =====================================================

    confidence_score: int = 0
    grade: ConfidenceGrade = ConfidenceGrade.D
    minimum_confidence_met: bool = False

    # =====================================================
    # DIAGNOSTICS
    # =====================================================

    # Human-readable explanation of confidence calculation.
    reasons: List[str] = field(default_factory=list)

    # Per-factor contribution to the final confidence score.
    # Example:
    # {
    #     "trend": 20,
    #     "structure": 20,
    #     "ema": 10,
    #     "adx": 10,
    #     "liquidity": 5,
    #     "daily_bias": 5,
    #     "cpr": 5,
    # }
    factor_scores: Dict[str, int] = field(default_factory=dict)

    # =====================================================
    # VALIDATION
    # =====================================================

    valid: bool = False