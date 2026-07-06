"""
=========================================================
PROJECT FALCON
Trade Filters V2
=========================================================
"""

from dataclasses import dataclass

from models.trade_setup import TradeSetup
from strategy.strategy_config import (
    ADX_MIN,
    RSI_LONG,
    RSI_SHORT,
)


@dataclass
class FilterResult:
    passed: bool
    reasons: list[str]


class TradeFilter:

    def evaluate(self, setup: TradeSetup) -> FilterResult:

        reasons = []

        # ----------------------------------------
        # ADX
        # ----------------------------------------
        if setup.adx < ADX_MIN:
            reasons.append(f"ADX too low ({setup.adx})")

        # ----------------------------------------
        # RSI
        # ----------------------------------------
        if setup.direction == "BUY":

            if setup.rsi < RSI_LONG:
                reasons.append(f"RSI too weak ({setup.rsi})")

        elif setup.direction == "SELL":

            if setup.rsi > RSI_SHORT:
                reasons.append(f"RSI too strong ({setup.rsi})")

        # ----------------------------------------
        # Trend
        # ----------------------------------------
        if setup.trend == "RANGE":
            reasons.append("Market is ranging")

        # ----------------------------------------
        # Structure
        # ----------------------------------------
        if setup.structure == "NEUTRAL":
            reasons.append("No market structure")

        # ----------------------------------------
        # Liquidity
        # ----------------------------------------
        if not setup.liquidity:
            reasons.append("Liquidity confirmation missing")

        # ----------------------------------------
        # Fibonacci
        # ----------------------------------------
        if not setup.golden_zone:
            reasons.append("Outside Fibonacci Golden Zone")

        # ----------------------------------------
        # EMA Alignment
        # ----------------------------------------
        if not setup.ema_alignment:
            reasons.append("EMA alignment missing")

        # ----------------------------------------
        # Final Result
        # ----------------------------------------
        return FilterResult(
            passed=len(reasons) == 0,
            reasons=reasons,
        )