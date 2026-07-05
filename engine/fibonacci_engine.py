"""
==========================================================
FALCON FIBONACCI ENGINE
Version : 2.0

Institutional Fibonacci Engine

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from core.base_engine import BaseEngine
from core.models import FibonacciLevels
from core.exceptions import ValidationError
from core.constants import (
    FIB_23_6,
    FIB_38_2,
    FIB_50,
    FIB_61_8,
    FIB_78_6,
)


class FibonacciEngine(BaseEngine):

    def __init__(self):
        super().__init__()

    def calculate(
        self,
        high: float,
        low: float,
        trend: str = "UPTREND"
    ) -> FibonacciLevels:

        self.log("Running Fibonacci Engine")

        if high == low:
            raise ValidationError(
                "High and Low cannot be equal."
            )

        # ==========================================
        # UPTREND
        # ==========================================

        if trend.upper() == "UPTREND":

            if high < low:
                raise ValidationError(
                    "For an uptrend, High must be greater than Low."
                )

            diff = high - low

            fib_0 = high
            fib_23_6 = high - diff * FIB_23_6
            fib_38_2 = high - diff * FIB_38_2
            fib_50 = high - diff * FIB_50
            fib_61_8 = high - diff * FIB_61_8
            fib_78_6 = high - diff * FIB_78_6
            fib_100 = low

        # ==========================================
        # DOWNTREND
        # ==========================================

        elif trend.upper() == "DOWNTREND":

            if low > high:
                raise ValidationError(
                    "For a downtrend, Low must be smaller than High."
                )

            diff = high - low

            fib_0 = low
            fib_23_6 = low + diff * FIB_23_6
            fib_38_2 = low + diff * FIB_38_2
            fib_50 = low + diff * FIB_50
            fib_61_8 = low + diff * FIB_61_8
            fib_78_6 = low + diff * FIB_78_6
            fib_100 = high

        else:

            raise ValidationError(
                "Trend must be UPTREND or DOWNTREND."
            )

        return FibonacciLevels(

            high=high,
            low=low,

            fib_0=fib_0,
            fib_23_6=fib_23_6,
            fib_38_2=fib_38_2,
            fib_50=fib_50,
            fib_61_8=fib_61_8,
            fib_78_6=fib_78_6,
            fib_100=fib_100,

            golden_zone_top=fib_38_2,
            golden_zone_bottom=fib_61_8
        )