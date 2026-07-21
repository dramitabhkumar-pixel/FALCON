"""
=========================================================
PROJECT FALCON
Confidence Engine
Version : 4.0
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
from models.enums import ConfidenceGrade, Bias


class ConfidenceEngine:
    """
    Converts a validated ConfluenceResult into a ConfidenceResult.
    """

    # =====================================================
    # Weight Configuration
    # =====================================================

    WEIGHTS = {
        
        "adx_confirmation": 30,
        "golden_zone_confirmation": 15,
        "rsi_confirmation": 20,
        "atr_confirmation": 20,
        "liquidity_confirmation": 10,
        
        "daily_bias_confirmation": 5,
    }

    MINIMUM_CONFIDENCE = 80

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate(confluence: ConfluenceResult) -> None:
        if confluence is None:
            raise ValueError("ConfluenceResult cannot be None.")

        if not confluence.valid:
            raise ValueError("ConfluenceResult is invalid.")

    # =====================================================
    # Grade Calculation
    # =====================================================

    @staticmethod
    def _calculate_grade(score: int) -> ConfidenceGrade:
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

        self._validate(confluence)

        score = 0
        reasons: list[str] = []

        for field_name, weight in self.WEIGHTS.items():
            passed = getattr(confluence, field_name, False)

            if passed:
                score += weight
                reasons.append(f"{field_name}: PASS (+{weight})")
            else:
                reasons.append(f"{field_name}: FAIL (+0)")

        print("\n========== CONFIDENCE ==========")
        
        print("ADX        :", confluence.adx_confirmation)
        print("RSI        :", confluence.rsi_confirmation)
        print("ATR        :", confluence.atr_confirmation)
        print("GoldenZone :", confluence.golden_zone_confirmation)
        print("Liquidity  :", confluence.liquidity_confirmation)
        print("Daily Bias :", confluence.daily_bias_confirmation)
        print("Score      :", score)
        print("================================\n")

        return ConfidenceResult(
            confidence_score=score,
            grade=self._calculate_grade(score),
            minimum_confidence_met=score >= self.MINIMUM_CONFIDENCE,
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
        return self.evaluate(confluence)
