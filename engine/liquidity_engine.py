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

    def analyze(
            self, 
            swings,
            atr:float,
    ):        

        print("\n========== LIQUIDITY DEBUG ==========")
        print(type(swings))

        if hasattr(swings, "columns"):
         print(swings.columns)

        print("=====================================\n")

        self.log("Running Liquidity Engine")

        equal_highs = []
        equal_lows = []

        buy_side = []
        sell_side = []

        # ----------------------------------
        # Dynamic Tolerance
        # ----------------------------------

        tolerance = max(
            atr * 0.25,
            5.0,
        )

        print("\n===== LIQUIDITY TOLERANCE =====")
        print("ATR       :", atr)
        print("Tolerance :", round(tolerance, 2))
        print("===============================")

        highs = swings[
            swings["Type"] == "HIGH"
        ]
        

        lows = swings[
            swings["Type"] == "LOW"
        ]

        # ----------------------------------
        # Equal Highs
        # ----------------------------------

        for i in range(len(highs)-1):
            p1 = highs.iloc[i]["Price"]
            p2 = highs.iloc[i + 1]["Price"]
            if abs(p1 - p2) <= tolerance:
                equal_highs.append(p1)
                buy_side.append(p1)
        print(
            p1,
            p2,
            abs(p1-p2)
        )



        # ----------------------------------
        # Equal Lows
        # ----------------------------------

        for i in range(len(lows)-1):
            p1 = lows.iloc[i]["Price"]
            p2 = lows.iloc[i + 1]["Price"]
            if abs(p1 - p2) <= tolerance:
                equal_lows.append(p1)
                sell_side.append(p1)
        print(
            p1,
            p2,
            abs(p1-p2)

        )

            

        return LiquidityResult(

            buy_side_liquidity=buy_side,

            sell_side_liquidity=sell_side,

            equal_highs=equal_highs,

            equal_lows=equal_lows,

            liquidity_sweeps=[]
        )