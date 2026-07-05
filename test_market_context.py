from engine.market_context_engine import MarketContextEngine

engine = MarketContextEngine()

result = engine.analyze(
    adx=28,
    ema_fast=221,
    ema_slow=214,
    rsi=66,
    atr=95,
    avg_atr=80,
)

print()

print("Trend      :", result.trend)
print("Bias       :", result.bias)
print("Strength   :", result.strength)
print("Volatility :", result.volatility)
print("Session    :", result.session)