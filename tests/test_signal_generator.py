from models.trade_setup import TradeSetup
from strategy.signal_generator import SignalGenerator

setup = TradeSetup(
    trend="UP",
    structure="BULLISH",
    ema_alignment=True,
    bos=True,
    choch=False,
    golden_zone=True,
)

engine = SignalGenerator()

result = engine.generate(setup)

print("\n===== Signal Generator =====")
print("Signal   :", result.signal)
print("Strength :", result.strength)

print("\nReasons:")
for reason in result.reasons:
    print("-", reason)