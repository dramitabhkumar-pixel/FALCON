"""
=========================================================
PROJECT FALCON
Confidence Engine
Version : 3.0
=========================================================

Evaluates the confidence of a validated ConfluenceResult.

TradeSetup
    ↓
ConfluenceEngine
    ↓
ConfluenceResult
    ↓
ConfidenceEngine
    ↓
ConfidenceResult
"""

from __future__ import annotations

from models.confluence_result import ConfluenceResult
from models.confidence_result import ConfidenceResult
from models.enums import ConfidenceGrade


class ConfidenceEngine:
    """
    Converts a ConfluenceResult into a ConfidenceResult.
    """

    # =====================================================
    # Weight Configuration
    # =====================================================

    WEIGHTS = {

        "trend_alignment": 15,

        "structure_alignment": 15,

        "ema_alignment": 10,

        "momentum_confirmation": 10,

        "liquidity_confirmation": 10,

        "fibonacci_confirmation": 10,

        "golden_zone_confirmation": 10,

        "bos_confirmation": 5,

        "choch_confirmation": 5,

        "order_block_confirmation": 5,

        "fair_value_gap_confirmation": 5,
    }

    MINIMUM_CONFIDENCE = 80

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate(
        confluence: ConfluenceResult,
    ) -> None:

        if confluence is None:
            raise ValueError(
                "ConfluenceResult cannot be None."
            )

        if not confluence.valid:
            raise ValueError(
                "ConfluenceResult is invalid."
            )

    # =====================================================
    # Grade
    # =====================================================

    @staticmethod
    def _calculate_grade(
        score: int,
    ) -> ConfidenceGrade:

        if score >= 90:
            return ConfidenceGrade.A_PLUS

        if score >= 80:
            return ConfidenceGrade.A

        if score >= 70:
            return ConfidenceGrade.B

        if score >= 60:
            return ConfidenceGrade.C

        return ConfidenceGrade.D
        # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        confluence: ConfluenceResult,
    ) -> ConfidenceResult:

        self._validate(
            confluence,
        )

        score = 0

        reasons: list[str] = []

        for field_name, weight in self.WEIGHTS.items():

            if getattr(
                confluence,
                field_name,
            ):

                score += weight

                reasons.append(
                    f"{field_name}: PASS"
                )

            else:

                reasons.append(
                    f"{field_name}: FAIL"
                )

        return ConfidenceResult(

            confidence_score=score,

            grade=self._calculate_grade(
                score,
            ),

            minimum_confidence_met=(
                score >= self.MINIMUM_CONFIDENCE
            ),

            reasons=reasons,

            valid=True,
        )

    # =====================================================
    # Callable Interface
    # =====================================================

    def __call__(
        self,
        confluence: ConfluenceResult,
    ) -> ConfidenceResult:

        return self.evaluate(
            confluence,
        )