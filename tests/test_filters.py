from models.trade_setup import TradeSetup
from strategy.filters import TradeFilter

setup = TradeSetup(
    trend="UP",
    structure="BULLISH",
    liquidity=True,
    golden_zone=True,
    ema_alignment=True,
    direction="BUY",
    rsi=65,
    adx=30,
    risk_reward=3.2,
)

engine = TradeFilter()

result = engine.evaluate(setup)

print()

print("Passed :", result.passed)

if result.reasons:

    print()

    print("Reasons")

    for reason in result.reasons:

        print("-", reason)