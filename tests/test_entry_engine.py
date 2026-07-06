import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from types import SimpleNamespace

from strategy.confidence_engine import ConfidenceEngine


setup = SimpleNamespace(
    trend="UP",
    structure="BULLISH",
    ema_alignment=True,
    bos=True,
    choch=False,
    golden_zone=True,
    adx_confirmed=True,
    rsi_confirmed=True,
    liquidity_confirmed=False,
)

engine = ConfidenceEngine()

result = engine.calculate(setup)

engine.print_report(result)

print("\nEngine:")
print(engine)

print("\nTradeable :", engine.is_tradeable(result))
print("High Confidence :", engine.is_high_confidence(result))