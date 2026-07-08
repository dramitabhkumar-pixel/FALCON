"""
=========================================================
PROJECT FALCON
Swing Fibonacci Engine Test
=========================================================

Validation Suite
"""

from __future__ import annotations

import traceback

import pandas as pd

from engine.swing_fibonacci_engine import SwingFibonacciEngine


# =========================================================
# TEST DATA
# =========================================================

def bullish_price_data() -> pd.DataFrame:

    close = [
        100,101,102,103,104,
        105,106,107,108,109,
        110,111,112,113,114,
        115,116,117,118,119,
        114
    ]

    return pd.DataFrame(
        {
            "Open": close,
            "High": [x + 1 for x in close],
            "Low": [x - 1 for x in close],
            "Close": close,
        }
    )


def bearish_price_data() -> pd.DataFrame:

    close = [
        120,119,118,117,116,
        115,114,113,112,111,
        110,109,108,107,106,
        105,104,103,102,101,
        106
    ]

    return pd.DataFrame(
        {
            "Open": close,
            "High": [x + 1 for x in close],
            "Low": [x - 1 for x in close],
            "Close": close,
        }
    )


def bullish_swings() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "Index": [0, 20],
            "Datetime": [
                "2026-01-01 09:15",
                "2026-01-01 14:15",
            ],
            "Price": [100, 120],
            "Type": [
                "LOW",
                "HIGH",
            ],
            "Classification": [
                "HL",
                "HH",
            ],
            "Strength": [
                "STRONG",
                "STRONG",
            ],
        }
    )


def bearish_swings() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "Index": [0, 20],
            "Datetime": [
                "2026-01-01 09:15",
                "2026-01-01 14:15",
            ],
            "Price": [120, 100],
            "Type": [
                "HIGH",
                "LOW",
            ],
            "Classification": [
                "LH",
                "LL",
            ],
            "Strength": [
                "STRONG",
                "STRONG",
            ],
        }
    )


def weak_swings() -> pd.DataFrame:

    df = bullish_swings()

    df.loc[1, "Strength"] = "WEAK"

    return df


def short_impulse_swings() -> pd.DataFrame:

    df = bullish_swings()

    df.loc[1, "Index"] = 8

    return df


# =========================================================
# TESTS
# =========================================================

def test_bullish():

    print("\n[BULLISH TEST]")

    engine = SwingFibonacciEngine()

    result = engine.calculate(
        bullish_price_data(),
        bullish_swings(),
    )

    assert result is not None

    print("Direction :", result.direction)
    print("High      :", result.swing_high)
    print("Low       :", result.swing_low)
    print("Fib 38.2  :", round(result.fib_382, 2))
    print("Fib 61.8  :", round(result.fib_618, 2))
    print("Golden    :", round(result.golden_lower, 2),
          "-", round(result.golden_upper, 2))
    print("Pullback  :", result.pullback_valid)


def test_bearish():

    print("\n[BEARISH TEST]")

    engine = SwingFibonacciEngine()

    result = engine.calculate(
        bearish_price_data(),
        bearish_swings(),
    )

    assert result is not None

    print("Direction :", result.direction)
    print("High      :", result.swing_high)
    print("Low       :", result.swing_low)
    print("Fib 38.2  :", round(result.fib_382, 2))
    print("Fib 61.8  :", round(result.fib_618, 2))

def test_weak_swings():

    print("\n[WEAK SWING TEST]")

    engine = SwingFibonacciEngine()

    result = engine.calculate(
        bullish_price_data(),
        weak_swings(),
    )

    assert result is None

    print("PASS : Weak swing rejected.")


def test_short_impulse():

    print("\n[SHORT IMPULSE TEST]")

    engine = SwingFibonacciEngine()

    result = engine.calculate(
        bullish_price_data(),
        short_impulse_swings(),
    )

    assert result is None

    print("PASS : Short impulse rejected.")


def test_missing_columns():

    print("\n[MISSING COLUMN TEST]")

    engine = SwingFibonacciEngine()

    df = bullish_price_data().drop(
        columns=["Close"]
    )

    try:

        engine.calculate(
            df,
            bullish_swings(),
        )

        raise AssertionError(
            "Expected ValueError."
        )

    except ValueError as e:

        print("PASS :", e)


def test_empty_dataframe():

    print("\n[EMPTY DATAFRAME TEST]")

    engine = SwingFibonacciEngine()

    result = engine.calculate(
        pd.DataFrame(),
        bullish_swings(),
    )

    assert result is None

    print("PASS : Empty dataframe handled.")


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 70)
    print("SWING FIBONACCI ENGINE VALIDATION")
    print("=" * 70)

    tests = [

        test_bullish,

        test_bearish,

        test_weak_swings,

        test_short_impulse,

        test_missing_columns,

        test_empty_dataframe,

    ]

    passed = 0

    failed = 0

    for test in tests:

        try:

            test()

            passed += 1

        except Exception:

            failed += 1

            print()

            traceback.print_exc()

    print()
    print("=" * 70)

    print(f"Passed : {passed}")

    print(f"Failed : {failed}")

    print("=" * 70)

    if failed == 0:

        print("SWING FIBONACCI ENGINE VALIDATED")

    else:

        print("VALIDATION FAILED")


if __name__ == "__main__":

    main()