"""
==========================================================
FALCON TREND ENGINE
Version : 1.0

Combines Market Context + Market Structure
to produce the final trend assessment.

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from core.base_engine import BaseEngine
from core.models import (
    MarketContext,
    MarketStructure,
    TrendResult,
)


class TrendEngine(BaseEngine):

    def __init__(self):
        super().__init__()

    def analyze(
        self,
        context: MarketContext,
        structure: MarketStructure,
    ) -> TrendResult:

        self.log("Running Trend Engine")

        confidence = 50.0

        # -------------------------------------------------
        # Trend Agreement
        # -------------------------------------------------

        if context.trend == structure.trend:

            trend = context.trend

            confidence += 30

        else:

            trend = "RANGE"

            confidence -= 20

        # -------------------------------------------------
        # Strength
        # -------------------------------------------------

        strength = context.strength

        if structure.bos:
            confidence += 10

        if structure.choch:
            confidence -= 15

        confidence = max(0, min(confidence, 100))

        # -------------------------------------------------
        # Trade Direction
        # -------------------------------------------------

        if trend == "UPTREND":
            trade_direction = "LONG"

        elif trend == "DOWNTREND":
            trade_direction = "SHORT"

        else:
            trade_direction = "NONE"

        # -------------------------------------------------
        # Pullback Permission
        # -------------------------------------------------

        pullback_allowed = (
            trade_direction != "NONE"
            and confidence >= 70
        )

        return TrendResult(
            trend=trend,
            strength=strength,
            confidence=confidence,
            trade_direction=trade_direction,
            pullback_allowed=pullback_allowed,
        )