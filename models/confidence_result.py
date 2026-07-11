"""
=========================================================
PROJECT FALCON
Confidence Result Model
Version : 2.0
=========================================================

Represents the output of the Confidence Engine.

This model contains ONLY the confidence evaluation.
No business logic belongs here.
"""

from dataclasses import dataclass, field
from typing import List

from models.enums import ConfidenceGrade


@dataclass(slots=True)
class ConfidenceResult:
    """
    Result produced by the Confidence Engine.
    """

    # =====================================================
    # Confidence
    # =====================================================

    confidence_score: int = 0

    grade: ConfidenceGrade = ConfidenceGrade.D

    minimum_confidence_met: bool = False

    # =====================================================
    # Diagnostics
    # =====================================================

    reasons: List[str] = field(default_factory=list)

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False