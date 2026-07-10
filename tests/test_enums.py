"""
=========================================================
Project FALCON
Enums Validation Test
=========================================================
"""

from models.enums import (
    Trend,
    Bias,
    Strength,
    Structure,
    StructureEvent,
    SwingType,
    SwingClassification,
    FibonacciDirection,
    LiquidityType,
    Signal,
    Session,
    Volatility,
    Direction,
    ConfidenceGrade,
    TradeStatus,
    ExitReason,
    OrderBlockType,
    FVGType,
)


def main():
    print("========== ENUM VALIDATION ==========")

    print("Trend:", Trend.CONFIRMED_UPTREND)
    print("Bias:", Bias.BULLISH)
    print("Strength:", Strength.STRONG)
    print("Structure:", Structure.BULLISH)
    print("Event:", StructureEvent.BOS_BULLISH)
    print("Swing:", SwingClassification.HH)
    print("Fib:", FibonacciDirection.BULLISH)
    print("Liquidity:", LiquidityType.BUY_SIDE)
    print("Signal:", Signal.BUY)
    print("Session:", Session.MORNING)
    print("Volatility:", Volatility.HIGH)
    print("Direction:", Direction.LONG)
    print("Confidence:", ConfidenceGrade.A_PLUS)
    print("Trade Status:", TradeStatus.ACTIVE)
    print("Exit:", ExitReason.TARGET)
    print("Order Block:", OrderBlockType.BULLISH)
    print("FVG:", FVGType.BULLISH)

    print("\n✅ All enums imported successfully.")
    print("========== PASSED ==========")


if __name__ == "__main__":
    main()