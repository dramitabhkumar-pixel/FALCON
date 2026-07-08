"""
=========================================================
PROJECT FALCON
Swing Fibonacci Model
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SwingFibonacci:
    """
    Represents the Fibonacci retracement of the latest
    completed market impulse.
    """

    direction: str

    swing_high: float
    swing_low: float

    range_points: float

    fib_236: float
    fib_382: float
    fib_500: float
    fib_618: float
    fib_786: float

    golden_upper: float
    golden_lower: float

    pullback_valid: bool