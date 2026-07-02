"""
=========================================================
Project FALCON
Structure Engine
Version : 2.0
=========================================================
"""

import pandas as pd

from core.base_engine import BaseEngine


class StructureEngine(BaseEngine):
    """
    Detects market structure from classified swings.
    """

    def __init__(self):

        super().__init__("StructureEngine")

    # -----------------------------------------------------

    def validate(
        self,
        swings: pd.DataFrame,
    ):

        required = [
            "Price",
            "Type",
            "Classification",
        ]

        for column in required:

            if column not in swings.columns:
                raise ValueError(
                    f"Missing column: {column}"
                )

    # -----------------------------------------------------

    def run(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        self.log("Running Structure Engine")

        self.validate(swings)

        structure = []

        previous_high = None
        previous_low = None

        for _, row in swings.iterrows():

            classification = row["Classification"]

            # ----------------------------
            # Bullish Structure
            # ----------------------------

            if classification in (
                "Swing High",
                "Higher High",
            ):

                if (
                    previous_high is not None
                    and row["Price"] > previous_high
                ):

                    structure.append({

                        "Index": row["Index"],
                        "Signal": "Bullish BOS",
                        "Price": row["Price"],

                    })

                previous_high = row["Price"]

            # ----------------------------
            # Bearish Structure
            # ----------------------------

            elif classification in (
                "Swing Low",
                "Lower Low",
            ):

                if (
                    previous_low is not None
                    and row["Price"] < previous_low
                ):

                    structure.append({

                        "Index": row["Index"],
                        "Signal": "Bearish BOS",
                        "Price": row["Price"],

                    })

                previous_low = row["Price"]

        return pd.DataFrame(structure)