"""
=========================================================
PROJECT FALCON
Trade Filters V2
=========================================================

Applies rule-based filters before a trade is allowed.
"""

from dataclasses import dataclass, field

from models.trade_setup import TradeSetup
from strategy.strategy_config import StrategyConfig


@dataclass(slots=True)
class FilterResult:
    passed: bool
    reasons: list[str] = field(default_factory=list)


class TradeFilter:
    """
    Applies hard filters to a TradeSetup before it can
    proceed to entry execution.
    """

    def __init__(self, config: StrategyConfig | None = None) -> None:
        self.config = config or StrategyConfig()

    # ---------------------------------------------------------

    def evaluate(self, setup: TradeSetup) -> FilterResult:

        reasons: list[str] = []

        adx = getattr(setup, "adx", 0.0)
        rsi = getattr(setup, "rsi", 50.0)

        # -----------------------------------------------------
        # ADX
        # -----------------------------------------------------

        if adx < self.config.ADX_MIN:
            reasons.append(f"ADX too low ({adx:.2f})")

        # -----------------------------------------------------
        # RSI
        # -----------------------------------------------------

        direction = getattr(setup, "direction", None)

        if direction == "BUY":

            if rsi < self.config.RSI_LONG:
                reasons.append(f"RSI too weak ({rsi:.2f})")

        elif direction == "SELL":

            if rsi > self.config.RSI_SHORT:
                reasons.append(f"RSI too strong ({rsi:.2f})")

        # -----------------------------------------------------
        # Trend
        # -----------------------------------------------------

        if getattr(setup, "trend", None) == "RANGE":
            reasons.append("Market is ranging")

        # -----------------------------------------------------
        # Structure
        # -----------------------------------------------------

        if getattr(setup, "structure", None) == "NEUTRAL":
            reasons.append("No market structure")

        # -----------------------------------------------------
        # Liquidity
        # -----------------------------------------------------

        if not getattr(setup, "liquidity", False):
            reasons.append("Liquidity confirmation missing")

        # -----------------------------------------------------
        # Fibonacci
        # -----------------------------------------------------

        if not getattr(setup, "golden_zone", False):
            reasons.append("Outside Fibonacci Golden Zone")

        # -----------------------------------------------------
        # EMA Alignment
        # -----------------------------------------------------

        if not getattr(setup, "ema_alignment", False):
            reasons.append("EMA alignment missing")

        # -----------------------------------------------------
        # Final Result
        # -----------------------------------------------------

        return FilterResult(
            passed=not reasons,
            reasons=reasons,
        )