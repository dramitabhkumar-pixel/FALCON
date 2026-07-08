"""
===========================================
Test Swing Fibonacci Engine
===========================================
"""

import pandas as pd

from engine.swing_fibonacci_engine import SwingFibonacciEngine


swings = pd.DataFrame({

    "Index": [10, 20],

    "Datetime": [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-01-02"),
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