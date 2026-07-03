"""
=========================================================
Project FALCON
Trend Engine
Version : 1.0
=========================================================
"""

import pandas as pd

from core.base_engine import BaseEngine


class TrendEngine(BaseEngine):
    """
    Determines overall market trend from classified swings.
    """

    def __init__(self):

        super().__init__("TrendEngine")

    # -----------------------------------------------------

    def validate(self, swings: pd.DataFrame):

        required = [
            "Classification"
        ]

        for column in required:

            if column not in swings.columns:
                raise ValueError(
                    f"Missing column: {column}"
                )

    # -----------------------------------------------------

    def run(self, swings: pd.DataFrame) -> str:

        self.log("Running Trend Engine")

        self.validate(swings)

        if swings.empty:
            return "UNKNOWN"

        highs = []
        lows = []

        for _, row in swings.iterrows():

            classification = row["Classification"]

            if classification in (
                "Swing High",
                "Higher High",
                "Lower High",
            ):
                highs.append(classification)

            elif classification in (
                "Swing Low",
                "Higher Low",
                "Lower Low",
            ):
                lows.append(classification)

        # -----------------------------
        # Simple Trend Logic (v1)
        # -----------------------------

        if "Higher High" in highs and "Higher Low" in lows:
            return "UPTREND"

        if "Lower High" in highs and "Lower Low" in lows:
            return "DOWNTREND"

        return "RANGE"