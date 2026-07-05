from engine.confluence_engine import ConfluenceEngine

engine = ConfluenceEngine()

result = engine.evaluate(
    market_structure="BULLISH",
    market_context="UPTREND",
    swing_direction="HH_HL",
    liquidity="BUY_SIDE",
    ema_bullish=True,
    adx=30,
    rsi=66,
    atr_high=True,
    fib_golden_zone=True,
)

print("\n==============================")
print("FALCON CONFLUENCE REPORT")
print("==============================")

print("Score          :", result.score)
print("Signal         :", result.signal)
print("Confidence     :", result.confidence)
print("Trade Grade    :", result.trade_grade)
print("Bullish Score  :", result.bullish_score)
print("Bearish Score  :", result.bearish_score)

print("\nReasons")

for reason in result.reasons:
    print("✓", reason)