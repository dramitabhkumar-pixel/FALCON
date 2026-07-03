"""
=========================================================
Project FALCON
Market Context Engine
Version : 2.0
=========================================================
"""

import pandas as pd

from core.base_engine import BaseEngine
from models.market_context import MarketContext


class MarketContextEngine(BaseEngine):

    def __init__(self):

        super().__init__("MarketContext")

    # -------------------------------------------------

    def validate(self, context: MarketContext):

        if context is None:
            raise ValueError("MarketContext cannot be None.")

    # -------------------------------------------------

    def run(self, context: MarketContext) -> MarketContext:

        self.log("Updating Market Context")

        self.validate(context)

        swings = context.swings

        if len(swings) == 0:
            return context

        context.trend.trend = "RANGE"
        context.trend.bias = "NEUTRAL"
        context.trend.strength = "NORMAL"

        higher_high = False
        higher_low = False

        lower_high = False
        lower_low = False

        for _, row in swings.iterrows():

            classification = row["Classification"]

            if classification == "Higher High":
                higher_high = True

            elif classification == "Higher Low":
                higher_low = True

            elif classification == "Lower High":
                lower_high = True

            elif classification == "Lower Low":
                lower_low = True

        if higher_high and higher_low:

            context.trend.trend = "UPTREND"
            context.trend.bias = "BULLISH"

        elif lower_high and lower_low:

            context.trend.trend = "DOWNTREND"
            context.trend.bias = "BEARISH"

        return context