"""
=========================================================
PROJECT FALCON
Confidence Engine
Version : 1.0
=========================================================

Calculates confidence score from the
Confluence Engine output.

TradeSetup
    ↓
ConfluenceResult
    ↓
Confidence Engine
    ↓
ConfidenceResult
"""

from core.base_engine import BaseEngine

from models.confluence_result import ConfluenceResult
from models.confidence_result import ConfidenceResult


class ConfidenceEngine(BaseEngine):
    """
    Converts a ConfluenceResult into
    a ConfidenceResult.
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
    # Engine
    # =====================================================

    def run(
        self,
        confluence: ConfluenceResult,
    ) -> ConfidenceResult:

        score = 0

        reasons = []

        for field_name, weight in self.WEIGHTS.items():

            if getattr(confluence, field_name):

                score += weight

                reasons.append(f"{field_name}: PASS")

            else:

                reasons.append(f"{field_name}: FAIL")

        grade = self._calculate_grade(score)

        return ConfidenceResult(

            confidence_score=score,

            grade=grade,

            minimum_confidence_met=(
                score >= self.MINIMUM_CONFIDENCE
            ),

            reasons=reasons,

            valid=confluence.valid,
        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _calculate_grade(score: int) -> str:

        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        if score >= 60:
            return "C"

        return "D"