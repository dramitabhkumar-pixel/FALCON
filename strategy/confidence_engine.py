"""
=========================================================
PROJECT FALCON
Confidence Engine V1.0
=========================================================

Calculates confidence score (0-100) for every setup.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConfidenceResult:
    score: float
    passed: bool
    grade: str
    confidence: str
    reasons: list[str] = field(default_factory=list)


class ConfidenceEngine:
    """
    Computes confidence score for a TradeSetup.

    The engine is intentionally deterministic so that
    historical backtests and live trading produce identical
    confidence values.
    """

    MINIMUM_SCORE = 80.0

    def __init__(self) -> None:

        self.weights = {
            "trend": 20,
            "structure": 20,
            "ema_alignment": 10,
            "bos": 10,
            "choch": 10,
            "golden_zone": 10,
            "adx": 10,
            "rsi": 5,
            "liquidity": 5,
        }

    # ---------------------------------------------------------

    @staticmethod
    def _grade(score: float) -> str:

        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        if score >= 60:
            return "C"

        return "D"

    # ---------------------------------------------------------

    @staticmethod
    def _confidence(score: float) -> str:

        if score >= 90:
            return "VERY HIGH"

        if score >= 80:
            return "HIGH"

        if score >= 60:
            return "MEDIUM"

        return "LOW"

    # ---------------------------------------------------------

    def calculate(self, setup: Any) -> ConfidenceResult:
        """
        Calculate confidence score for the supplied TradeSetup.
        """

        if setup is None:
            return ConfidenceResult(
                score=0.0,
                passed=False,
                grade="D",
                confidence="LOW",
                reasons=[],
            )

        score = 0
        reasons: list[str] = []

        checks = [

            (
                "trend",
                getattr(setup, "trend", None) in ("UP", "DOWN"),
                "Trend Confirmed",
            ),

            (
                "structure",
                getattr(setup, "structure", None) in ("BULLISH", "BEARISH"),
                "Market Structure",
            ),

            (
                "ema_alignment",
                getattr(setup, "ema_alignment", False),
                "EMA Alignment",
            ),

            (
                "bos",
                getattr(setup, "bos", False),
                "Break of Structure",
            ),

            (
                "choch",
                getattr(setup, "choch", False),
                "CHOCH",
            ),

            (
                "golden_zone",
                getattr(setup, "golden_zone", False),
                "Golden Zone",
            ),

            (
                "adx",
                getattr(setup, "adx_confirmed", False),
                "ADX Strength",
            ),

            (
                "rsi",
                getattr(setup, "rsi_confirmed", False),
                "RSI Confirmation",
            ),

            (
                "liquidity",
                getattr(setup, "liquidity_confirmed", False),
                "Liquidity",
            ),
        ]

        for key, condition, description in checks:

            if condition:
                score += self.weights[key]
                reasons.append(description)

        score = round(min(score, 100), 2)

        return ConfidenceResult(
            score=score,
            passed=score >= self.MINIMUM_SCORE,
            grade=self._grade(score),
            confidence=self._confidence(score),
            reasons=reasons,
        )