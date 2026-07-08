"""
=========================================================
Project FALCON
Swing Fibonacci Engine
Version : 1.0
=========================================================
"""

from __future__ import annotations

import pandas as pd

from core.base_engine import BaseEngine


class SwingFibonacciEngine(BaseEngine):
    """
    Builds Institutional Fibonacci from the latest
    confirmed market structure.

    Bullish:
        Higher Low -> Higher High

    Bearish:
        Lower High -> Lower Low
    """

    def __init__(self):

        super().__init__("SwingFibonacciEngine")

    # --------------------------------------------------

    def validate(
        self,
        swings: pd.DataFrame,
    ):

        if swings is None or swings.empty:
            raise ValueError(
                "Swing dataframe is empty."
            )

        required = [

            "Price",
            "Classification",
            "Datetime",
            "Index",

        ]

        for column in required:

            if column not in swings.columns:

                raise ValueError(
                    f"Missing column: {column}"
                )

    # --------------------------------------------------

    def compress_swings(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Compress consecutive swings.

        HH HH HH -> highest HH

        HL HL HL -> highest HL

        LH LH LH -> lowest LH

        LL LL LL -> lowest LL
        """

        compressed = []

        i = 0

        while i < len(swings):

            current = swings.iloc[i]

            classification = current[
                "Classification"
            ]

            group = [current]

            j = i + 1

            while (

                j < len(swings)

                and

                swings.iloc[j][
                    "Classification"
                ] == classification

            ):

                group.append(
                    swings.iloc[j]
                )

                j += 1

            group_df = pd.DataFrame(group)

            if classification in (

                "Higher High",
                "Higher Low",

            ):

                selected = group_df.loc[
                    group_df["Price"].idxmax()
                ]

            elif classification in (

                "Lower High",
                "Lower Low",

            ):

                selected = group_df.loc[
                    group_df["Price"].idxmin()
                ]

            else:

                selected = group_df.iloc[-1]

            compressed.append(
                selected
            )

            i = j

        return (
            pd.DataFrame(compressed)
            .reset_index(drop=True)
        )

    # --------------------------------------------------

    def detect_latest_impulse(
        self,
        swings: pd.DataFrame,
    ):

        """
        Searches backwards.

        Bullish

            Higher Low
                  ↓
            Higher High

        Bearish

            Lower High
                  ↓
            Lower Low
        """

        for i in range(

            len(swings) - 1,
            0,
            -1,

        ):

            current = swings.iloc[i]

            previous = swings.iloc[i - 1]

            # -------------------------
            # Bullish
            # -------------------------

            if (

                previous["Classification"]
                == "Higher Low"

                and

                current["Classification"]
                == "Higher High"

            ):

                return (

                    "BULLISH",

                    previous,

                    current,

                )

            # -------------------------
            # Bearish
            # -------------------------

            if (

                previous["Classification"]
                == "Lower High"

                and

                current["Classification"]
                == "Lower Low"

            ):

                return (

                    "BEARISH",

                    previous,

                    current,

                )

        return None
        # --------------------------------------------------

    def build_levels(
        self,
        trend: str,
        start_price: float,
        end_price: float,
    ) -> dict:
        """
        Builds Fibonacci levels from the latest
        confirmed impulse.
        """

        distance = abs(
            end_price - start_price
        )

        if trend == "BULLISH":

            return {

                "0.0": float(start_price),

                "23.6": float(
                    start_price + distance * 0.236
                ),

                "38.2": float(
                    start_price + distance * 0.382
                ),

                "50.0": float(
                    start_price + distance * 0.500
                ),

                "61.8": float(
                    start_price + distance * 0.618
                ),

                "78.6": float(
                    start_price + distance * 0.786
                ),

                "100.0": float(end_price),

            }

        return {

            "0.0": float(start_price),

            "23.6": float(
                start_price - distance * 0.236
            ),

            "38.2": float(
                start_price - distance * 0.382
            ),

            "50.0": float(
                start_price - distance * 0.500
            ),

            "61.8": float(
                start_price - distance * 0.618
            ),

            "78.6": float(
                start_price - distance * 0.786
            ),

            "100.0": float(end_price),

        }

    # --------------------------------------------------

    def run(
        self,
        swings: pd.DataFrame,
        current_price: float,
    ) -> dict:

        self.log(
            "Building Institutional Fibonacci"
        )

        self.validate(swings)

        swings = self.compress_swings(
            swings
        )

        impulse = self.detect_latest_impulse(
            swings
        )

        if impulse is None:

            return {

                "structure_valid": False,

                "trend": None,

                "impulse_start": None,

                "impulse_end": None,

                "impulse_size": 0.0,

                "fib_levels": {},

                "golden_low": None,

                "golden_high": None,

                "inside_golden_zone": False,

            }

        trend, start, end = impulse

        fib = self.build_levels(

            trend,

            float(start["Price"]),

            float(end["Price"]),

        )

        golden_low = min(

            fib["38.2"],

            fib["61.8"],

        )

        golden_high = max(

            fib["38.2"],

            fib["61.8"],

        )

        return {

            "structure_valid": True,

            "trend": trend,

            "impulse_start": float(
                start["Price"]
            ),

            "impulse_end": float(
                end["Price"]
            ),

            "impulse_size": float(
                abs(
                    end["Price"]
                    - start["Price"]
                )
            ),

            "start_time": start[
                "Datetime"
            ],

            "end_time": end[
                "Datetime"
            ],

            "fib_levels": fib,

            "golden_low": float(
                golden_low
            ),

            "golden_high": float(
                golden_high
            ),

            "inside_golden_zone": bool(

                golden_low
                <= current_price
                <= golden_high

            ),

        }