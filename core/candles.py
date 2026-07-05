"""
==========================================================
FALCON CANDLE MODEL
Version : 2.0
==========================================================
"""

from dataclasses import dataclass


@dataclass
class Candle:

    timestamp: str

    open: float
    high: float
    low: float
    close: float

    volume: float

    # ---------------------------------------
    # Direction
    # ---------------------------------------

    @property
    def bullish(self):

        return self.close > self.open

    @property
    def bearish(self):

        return self.close < self.open

    @property
    def direction(self):

        if self.bullish:
            return "BULLISH"

        if self.bearish:
            return "BEARISH"

        return "DOJI"

    # ---------------------------------------
    # Body
    # ---------------------------------------

    @property
    def body(self):

        return abs(self.close - self.open)

    # ---------------------------------------
    # Wicks
    # ---------------------------------------

    @property
    def upper_wick(self):

        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self):

        return min(self.open, self.close) - self.low

    # ---------------------------------------
    # Range
    # ---------------------------------------

    @property
    def range(self):

        return self.high - self.low

    # ---------------------------------------
    # Midpoint
    # ---------------------------------------

    @property
    def midpoint(self):

        return (self.high + self.low) / 2

    # ---------------------------------------
    # Candle Types
    # ---------------------------------------

    @property
    def is_doji(self):

        if self.range == 0:
            return False

        return self.body <= self.range * 0.10

    @property
    def is_marubozu(self):

        if self.range == 0:
            return False

        return (

            self.upper_wick <= self.range * 0.05

            and

            self.lower_wick <= self.range * 0.05

        )

    @property
    def body_percent(self):

        if self.range == 0:
            return 0

        return (self.body / self.range) * 100