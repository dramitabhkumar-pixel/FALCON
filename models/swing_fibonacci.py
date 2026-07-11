"""
=========================================================
PROJECT FALCON
Swing Fibonacci Model
Version : 2.0
=========================================================

Represents the Fibonacci retracement of the latest
validated market impulse.
"""

from dataclasses import dataclass

from models.enums import FibonacciDirection


@dataclass(slots=True)
class SwingFibonacci:
    """
    Represents the Fibonacci retracement of the latest
    completed market impulse.
    """

    # =====================================================
    # Direction
    # =====================================================

    direction: FibonacciDirection = FibonacciDirection.NONE

    # =====================================================
    # Swing
    # =====================================================

    swing_high: float = 0.0

    swing_low: float = 0.0

    range_points: float = 0.0

    # =====================================================
    # Fibonacci Levels
    # =====================================================

    fib_236: float = 0.0

    fib_382: float = 0.0

    fib_500: float = 0.0

    fib_618: float = 0.0

    fib_786: float = 0.0

    # =====================================================
    # Golden Zone
    # =====================================================

    golden_upper: float = 0.0

    golden_lower: float = 0.0

    # =====================================================
    # Pullback Validation
    # =====================================================

    pullback_valid: bool = False