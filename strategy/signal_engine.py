"""
=========================================================
PROJECT FALCON
Signal Engine
=========================================================
"""

from dataclasses import dataclass

from models.trade_setup import TradeSetup


@dataclass
class SignalResult:
    signal: str
    reasons: list[str]


class SignalEngine:

    def generate(self, setup: TradeSetup) -> SignalResult:

        reasons = []

        # BUY
        if (
            setup.trend == "UP"
            and setup.structure == "BULLISH"
            and setup.ema_alignment
            and setup.bos
            and setup.golden_zone
        ):
            reasons.extend([
                "Uptrend",
                "Bullish Structure",
                "EMA Alignment",
                "Break of Structure",
                "Golden Zone"
            ])

            return SignalResult(
                signal="BUY",
                reasons=reasons
            )

        # SELL
        if (
            setup.trend == "DOWN"
            and setup.structure == "BEARISH"
            and setup.ema_alignment
            and setup.choch
            and setup.golden_zone
        ):
            reasons.extend([
                "Downtrend",
                "Bearish Structure",
                "EMA Alignment",
                "CHOCH",
                "Golden Zone"
            ])

            return SignalResult(
                signal="SELL",
                reasons=reasons
            )

        return SignalResult(
            signal="NONE",
            reasons=["No valid setup"]
        )