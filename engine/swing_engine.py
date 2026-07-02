"""
=========================================================
Project FALCON
Swing Detection Engine
Version : 2.0
=========================================================
"""

import pandas as pd

from core.base_engine import BaseEngine


class SwingEngine(BaseEngine):
    """
    Detects Swing Highs and Swing Lows.
    """

    def __init__(
        self,
        left_bars: int = 3,
        right_bars: int = 3,
    ):

        super().__init__("SwingEngine")

        self.left_bars = left_bars
        self.right_bars = right_bars

    # -----------------------------------------------------

    def validate(self, df: pd.DataFrame):

        required = [
            "Open",
            "High",
            "Low",
            "Close",
        ]

        for column in required:

            if column not in df.columns:
                raise ValueError(
                    f"Missing column: {column}"
                )

        minimum = (
            self.left_bars
            + self.right_bars
            + 1
        )

        if len(df) < minimum:
            raise ValueError(
                "Not enough candles."
            )

    # -----------------------------------------------------

    def classify_swings(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        last_high = None
        last_low = None

        labels = []

        for _, row in swings.iterrows():

            if row["Type"] == "Swing High":

                if last_high is None:
                    labels.append("Swing High")

                elif row["Price"] > last_high:
                    labels.append("Higher High")

                else:
                    labels.append("Lower High")

                last_high = row["Price"]

            else:

                if last_low is None:
                    labels.append("Swing Low")

                elif row["Price"] > last_low:
                    labels.append("Higher Low")

                else:
                    labels.append("Lower Low")

                last_low = row["Price"]

        swings = swings.copy()

        swings["Classification"] = labels

        return swings

    # -----------------------------------------------------

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        self.log("Running Swing Engine")

        self.validate(df)

        swings = []

        start = self.left_bars
        end = len(df) - self.right_bars

        for i in range(start, end):

            current_high = df.iloc[i]["High"]
            current_low = df.iloc[i]["Low"]

            left_highs = df.iloc[
                i-self.left_bars:i
            ]["High"]

            right_highs = df.iloc[
                i+1:i+self.right_bars+1
            ]["High"]

            left_lows = df.iloc[
                i-self.left_bars:i
            ]["Low"]

            right_lows = df.iloc[
                i+1:i+self.right_bars+1
            ]["Low"]

            if (
                current_high > left_highs.max()
                and current_high > right_highs.max()
            ):

                swings.append({

                    "Index": i,
                    "Datetime": df.index[i],
                    "Price": current_high,
                    "Type": "Swing High",

                })

            if (
                current_low < left_lows.min()
                and current_low < right_lows.min()
            ):

                swings.append({

                    "Index": i,
                    "Datetime": df.index[i],
                    "Price": current_low,
                    "Type": "Swing Low",

                })

        result = pd.DataFrame(swings)

        if result.empty:
            return result

        return self.classify_swings(result)