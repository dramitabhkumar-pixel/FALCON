"""
=========================================================
Project FALCON
Market Structure Engine
Version : 1.0
=========================================================
"""

import pandas as pd


class StructureEngine:
    """
    Detects market structure from classified swings.
    """

    def detect_structure(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        if swings.empty:
            return swings

        structure = []

        previous_high = None
        previous_low = None

        for _, row in swings.iterrows():

            if row["Classification"] in ["Swing High", "Higher High"]:

                if previous_high is not None:

                    if row["Price"] > previous_high:

                        structure.append({
                            "Index": row["Index"],
                            "Signal": "BOS Bullish"
                        })

                previous_high = row["Price"]

            elif row["Classification"] in ["Swing Low", "Lower Low"]:

                if previous_low is not None:

                    if row["Price"] < previous_low:

                        structure.append({
                            "Index": row["Index"],
                            "Signal": "BOS Bearish"
                        })

                previous_low = row["Price"]

        return pd.DataFrame(structure)