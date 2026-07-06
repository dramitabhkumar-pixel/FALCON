import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from strategy.confidence_engine import ConfidenceEngine


class Setup:
    pass


def run_case(name, **kwargs):

    setup = Setup()

    for k, v in kwargs.items():
        setattr(setup, k, v)

    engine = ConfidenceEngine()

    result = engine.calculate(setup)

    print("=" * 60)
    print(name)
    print("=" * 60)
    print("Score      :", result.score)
    print("Passed     :", result.passed)
    print("Grade      :", result.grade)
    print("Confidence :", result.confidence)
    print("Reasons    :", result.reasons)
    print()


run_case(
    "PERFECT SETUP",
    trend="UP",
    structure="BULLISH",
    ema_alignment=True,
    bos=True,
    choch=True,
    golden_zone=True,
    adx_confirmed=True,
    rsi_confirmed=True,
    liquidity_confirmed=True,
)

run_case(
    "AVERAGE SETUP",
    trend="UP",
    structure="BULLISH",
    ema_alignment=True,
    bos=True,
)

run_case(
    "WEAK SETUP",
)