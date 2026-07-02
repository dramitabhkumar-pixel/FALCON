"""
=========================================================
Project FALCON
Swing Detection Engine
Version : 1.2
Author  : Amitabh Kumar
=========================================================
"""

import pandas as pd

from models.swing import SwingPoint


class SwingEngine:
    """
    Detects Swing Highs and Swing Lows.
    """

    def __init__(self, left_bars: int = 3, right_bars: int = 3):
        self.left_bars = left_bars
        self.right_bars = right_bars

    # -----------------------------------------------------

    def validate_dataframe(self, df: pd.DataFrame) -> None:
        """
        Validate OHLC dataframe.
        """

        required = ["Open", "High", "Low", "Close"]

        for column in required:
            if column not in df.columns:
                raise ValueError(f"Missing column: {column}")

        if df.empty:
            raise ValueError("Input dataframe is empty.")

        minimum = self.left_bars + self.right_bars + 1

        if len(df) < minimum:
            raise ValueError(
                f"Need at least {minimum} candles."
            )

    # -----------------------------------------------------

    def detect_swings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect Swing Highs and Swing Lows.
        """

        self.validate_dataframe(df)

        swings = []

        start = self.left_bars
        end = len(df) - self.right_bars

        for i in range(start, end):

            current_high = df.iloc[i]["High"]
            current_low = df.iloc[i]["Low"]

            left_highs = df.iloc[
                i - self.left_bars:i
            ]["High"]

            right_highs = df.iloc[
                i + 1:i + self.right_bars + 1
            ]["High"]

            left_lows = df.iloc[
                i - self.left_bars:i
            ]["Low"]

            right_lows = df.iloc[
                i + 1:i + self.right_bars + 1
            ]["Low"]

            # ----------------------------
            # Swing High
            # ----------------------------

            if (
                current_high > left_highs.max()
                and current_high > right_highs.max()
            ):

                swings.append(
                    {
                        "Index": i,
                        "Datetime": df.index[i],
                        "Price": current_high,
                        "Type": "Swing High",
                    }
                )

            # ----------------------------
            # Swing Low
            # ----------------------------

            if (
                current_low < left_lows.min()
                and current_low < right_lows.min()
            ):

                swings.append(
                    {
                        "Index": i,
                        "Datetime": df.index[i],
                        "Price": current_low,
                        "Type": "Swing Low",
                    }
                )

        result = pd.DataFrame(swings)

        if result.empty:
            return result

        return self.classify_swings(result)

    # -----------------------------------------------------

    def classify_swings(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Classify swings into HH / HL / LH / LL.
        """

        last_high = None
        last_low = None

        classification = []

        for _, row in swings.iterrows():

            if row["Type"] == "Swing High":

                if last_high is None:
                    classification.append("Swing High")

                elif row["Price"] > last_high:
                    classification.append("Higher High")

                else:
                    classification.append("Lower High")

                last_high = row["Price"]

            else:

                if last_low is None:
                    classification.append("Swing Low")

                elif row["Price"] > last_low:
                    classification.append("Higher Low")

                else:
                    classification.append("Lower Low")

                last_low = row["Price"]

        swings = swings.copy()

        swings["Classification"] = classification

        return swings