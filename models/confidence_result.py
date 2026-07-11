"""
=========================================================
PROJECT FALCON
Confidence Result Model
Version : 1.0
=========================================================

Represents the output of the Confidence Engine.

This model contains ONLY the confidence evaluation.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class ConfidenceResult:
    """
    Result produced by the Confidence Engine.

    This model represents the overall confidence
    score derived from the ConfluenceResult.

    It does NOT make trading decisions.
    """

    # =====================================================
    # Confidence
    # =====================================================

    confidence_score: int = 0

    grade: str = "D"

    minimum_confidence_met: bool = False

    # =====================================================
    # Diagnostics
    # =====================================================

    reasons: List[str] = field(default_factory=list)

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False