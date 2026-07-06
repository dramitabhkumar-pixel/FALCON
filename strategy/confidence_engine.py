"""
=========================================================
PROJECT FALCON
Confidence Engine V1.0
=========================================================

Calculates confidence score (0-100) for every setup.
"""

from dataclasses import dataclass, field


@dataclass
class ConfidenceResult:
    score: float
    passed: bool
    grade: str
    confidence: str
    reasons: list[str] = field(default_factory=list)


class ConfidenceEngine:

    def __init__(self):

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

        self.minimum_score = 80

    # -----------------------------------------------------

    def _grade(self, score):

        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        if score >= 60:
            return "C"

        return "D"

    # -----------------------------------------------------

    def _confidence(self, score):

        if score >= 90:
            return "VERY HIGH"

        if score >= 80:
            return "HIGH"

        if score >= 60:
            return "MEDIUM"

        return "LOW"

    # -----------------------------------------------------

    def calculate(self, setup):

        score = 0
        reasons = []

        checks = [

            ("trend",
             getattr(setup, "trend", None) in ("UP", "DOWN"),
             "Trend Confirmed"),

            ("structure",
             getattr(setup, "structure", None) in ("BULLISH", "BEARISH"),
             "Market Structure"),

            ("ema_alignment",
             getattr(setup, "ema_alignment", False),
             "EMA Alignment"),

            ("bos",
             getattr(setup, "bos", False),
             "Break of Structure"),

            ("choch",
             getattr(setup, "choch", False),
             "CHOCH"),

            ("golden_zone",
             getattr(setup, "golden_zone", False),
             "Golden Zone"),

            ("adx",
             getattr(setup, "adx_confirmed", False),
             "ADX Strength"),

            ("rsi",
             getattr(setup, "rsi_confirmed", False),
             "RSI Confirmation"),

            ("liquidity",
             getattr(setup, "liquidity_confirmed", False),
             "Liquidity"),
        ]

        for key, condition, label in checks:

            if condition:
                score += self.weights[key]
                reasons.append(label)

        score = round(min(score, 100), 2)

        return ConfidenceResult(
            score=score,
            passed=score >= self.minimum_score,
            grade=self._grade(score),
            confidence=self._confidence(score),
            reasons=reasons,
        )