"""
=========================================================
Project FALCON
Test : Swing Fibonacci Engine
=========================================================
"""

import pandas as pd

from engine.swing_fibonacci_engine import SwingFibonacciEngine


def run_test(title, swings, current_price):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    engine = SwingFibonacciEngine()

    result = engine.run(
        swings=swings,
        current_price=current_price,
    )

    for key, value in result.items():
        print(f"{key} : {value}")


# =========================================================
# TEST 1 : BULLISH
# =========================================================

bullish_swings = pd.DataFrame({

    "Index": [10, 20],

    "Datetime": [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-01-02"),
    ],

    "Price": [
        50000,
        51000,
    ],

    "Classification": [
        "Higher Low",
        "Higher High",
    ],

})

run_test(
    "TEST 1 : BULLISH IMPULSE",
    bullish_swings,
    current_price=50600,
)


# =========================================================
# TEST 2 : BEARISH
# =========================================================

bearish_swings = pd.DataFrame({

    "Index": [30, 40],

    "Datetime": [
        pd.Timestamp("2026-02-01"),
        pd.Timestamp("2026-02-02"),
    ],

    "Price": [
        52000,
        51000,
    ],

    "Classification": [
        "Lower High",
        "Lower Low",
    ],

})

run_test(
    "TEST 2 : BEARISH IMPULSE",
    bearish_swings,
    current_price=51400,
)


# =========================================================
# TEST 3 : NO VALID IMPULSE
# =========================================================

invalid_swings = pd.DataFrame({

    "Index": [50, 60],

    "Datetime": [
        pd.Timestamp("2026-03-01"),
        pd.Timestamp("2026-03-02"),
    ],

    "Price": [
        50000,
        50100,
    ],

    "Classification": [
        "Higher Low",
        "Higher Low",
    ],

})

run_test(
    "TEST 3 : INVALID STRUCTURE",
    invalid_swings,
    current_price=50050,
)