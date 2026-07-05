"""
==========================================================
FALCON LIQUIDITY ENGINE
Version : 1.0

Detects:

• Equal Highs
• Equal Lows
• Buy Side Liquidity
• Sell Side Liquidity

==========================================================
"""

from core.base_engine import BaseEngine
from core.models import LiquidityResult


class LiquidityEngine(BaseEngine):

    def __init__(self):

        super().__init__()

    def analyze(self, swings):

        self.log("Running Liquidity Engine")

        equal_highs = []
        equal_lows = []

        buy_side = []
        sell_side = []

        tolerance = 0.20

        highs = [
            s for s in swings
            if s["type"] == "HIGH"
        ]

        lows = [
            s for s in swings
            if s["type"] == "LOW"
        ]

        # ----------------------------------
        # Equal Highs
        # ----------------------------------

        for i in range(len(highs)-1):

            if abs(
                highs[i]["price"] -
                highs[i+1]["price"]
            ) <= tolerance:

                equal_highs.append(
                    highs[i]["price"]
                )

                buy_side.append(
                    highs[i]["price"]
                )

        # ----------------------------------
        # Equal Lows
        # ----------------------------------

        for i in range(len(lows)-1):

            if abs(
                lows[i]["price"] -
                lows[i+1]["price"]
            ) <= tolerance:

                equal_lows.append(
                    lows[i]["price"]
                )

                sell_side.append(
                    lows[i]["price"]
                )

        return LiquidityResult(

            buy_side_liquidity=buy_side,

            sell_side_liquidity=sell_side,

            equal_highs=equal_highs,

            equal_lows=equal_lows,

            liquidity_sweeps=[]
        )