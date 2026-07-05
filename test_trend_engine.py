from engine.market_context_engine import MarketContextEngine
from engine.market_structure_engine import MarketStructureEngine
from engine.trend_engine import TrendEngine


def main():

    context_engine = MarketContextEngine()
    structure_engine = MarketStructureEngine()
    trend_engine = TrendEngine()

    context = context_engine.analyze(
        adx=28,
        ema_fast=220,
        ema_slow=200,
        rsi=65,
        atr=100,
        avg_atr=80,
    )

    swings = [
        {"type": "LOW", "price": 100},
        {"type": "HIGH", "price": 120},
        {"type": "LOW", "price": 110},
        {"type": "HIGH", "price": 130},
    ]

    structure = structure_engine.analyze(swings)

    trend = trend_engine.analyze(
        context=context,
        structure=structure,
    )

    print()
    print("Trend             :", trend.trend)
    print("Strength          :", trend.strength)
    print("Confidence        :", trend.confidence)
    print("Trade Direction   :", trend.trade_direction)
    print("Pullback Allowed  :", trend.pullback_allowed)


if __name__ == "__main__":
    main()