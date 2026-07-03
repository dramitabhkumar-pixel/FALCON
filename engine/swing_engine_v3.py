"""
=========================================================
Project FALCON
Swing Detection Engine
Version : 3.0

Author : Amitabh Kumar
=========================================================

Institutional Swing Detection Engine

Pipeline

Validation
    ↓
Pivot Detection
    ↓
Classification
    ↓
Alternation
    ↓
Noise Filtering
    ↓
Strength Calculation
    ↓
Output
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from core.base_engine import BaseEngine


# =========================================================
# CONFIGURATION
# =========================================================

@dataclass(slots=True)
class SwingConfig:
    """
    Swing Engine Configuration.
    """

    left_bars: int = 3

    right_bars: int = 3

    minimum_price_distance: float = 0.0

    minimum_candle_distance: int = 1

    equal_high_tolerance: float = 0.0

    equal_low_tolerance: float = 0.0

    calculate_strength: bool = True

    filter_duplicates: bool = True


# =========================================================
# ENGINE
# =========================================================

class SwingEngine(BaseEngine):

    """
    Detects institutional swing highs and lows.

    Output Columns

    Index
    Datetime
    Price
    Type
    Classification
    Strength
    """

    def __init__(

        self,

        config: SwingConfig | None = None,

    ):

        super().__init__("SwingEngine")

        if config is None:

            config = SwingConfig()

        self.config = config

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(

        self,

        df: pd.DataFrame,

    ) -> None:

        if df is None:

            raise ValueError(
                "DataFrame is None."
            )

        if df.empty:

            raise ValueError(
                "DataFrame is empty."
            )

        required = [

            "Open",

            "High",

            "Low",

            "Close",

        ]

        for column in required:

            if column not in df.columns:

                raise ValueError(

                    f"Missing column '{column}'."

                )

        minimum = (

            self.config.left_bars

            + self.config.right_bars

            + 1

        )

        if len(df) < minimum:

            raise ValueError(

                f"Need at least {minimum} candles."

            )

    # =====================================================
    # PIVOT DETECTION
    # =====================================================

    def detect_pivots(

        self,

        df: pd.DataFrame,

    ) -> pd.DataFrame:

        """
        Detect pivot highs and pivot lows.
        """

        swings = []

        start = self.config.left_bars

        end = len(df) - self.config.right_bars

        for i in range(start, end):

            current_high = df.iloc[i]["High"]

            current_low = df.iloc[i]["Low"]

            left_highs = df.iloc[
                i-self.config.left_bars:i
            ]["High"]

            right_highs = df.iloc[
                i+1:i+self.config.right_bars+1
            ]["High"]

            left_lows = df.iloc[
                i-self.config.left_bars:i
            ]["Low"]

            right_lows = df.iloc[
                i+1:i+self.config.right_bars+1
            ]["Low"]            # --------------------------------------------
            # Swing High
            # --------------------------------------------

            if (
                current_high > left_highs.max()
                and current_high > right_highs.max()
            ):

                swings.append(
                    {
                        "Index": i,
                        "Datetime": df.index[i],
                        "Price": current_high,
                        "Type": "HIGH",
                    }
                )

            # --------------------------------------------
            # Swing Low
            # --------------------------------------------

            if (
                current_low < left_lows.min()
                and current_low < right_lows.min()
            ):

                swings.append(
                    {
                        "Index": i,
                        "Datetime": df.index[i],
                        "Price": current_low,
                        "Type": "LOW",
                    }
                )

        result = pd.DataFrame(swings)

        if result.empty:
            return result

        result.sort_values(
            "Index",
            inplace=True,
        )

        result.reset_index(
            drop=True,
            inplace=True,
        )

        return result

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    def remove_duplicates(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Remove duplicate consecutive highs/lows.

        If multiple HIGHs occur consecutively,
        keep the highest.

        If multiple LOWs occur consecutively,
        keep the lowest.
        """

        if swings.empty:

            return swings

        filtered = []

        current = swings.iloc[0]

        for i in range(1, len(swings)):

            nxt = swings.iloc[i]

            if current["Type"] == nxt["Type"]:

                if current["Type"] == "HIGH":

                    if nxt["Price"] > current["Price"]:

                        current = nxt

                else:

                    if nxt["Price"] < current["Price"]:

                        current = nxt

            else:

                filtered.append(current)

                current = nxt

        filtered.append(current)

        result = pd.DataFrame(filtered)

        result.reset_index(
            drop=True,
            inplace=True,
        )

        return result

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    def classify_swings(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        HH
        HL
        LH
        LL
        """

        if swings.empty:

            return swings

        last_high = None
        last_low = None

        labels = []

        for _, row in swings.iterrows():

            if row["Type"] == "HIGH":

                if last_high is None:

                    labels.append("HIGH")

                elif row["Price"] > last_high:

                    labels.append("HH")

                else:

                    labels.append("LH")

                last_high = row["Price"]

            else:

                if last_low is None:

                    labels.append("LOW")

                elif row["Price"] > last_low:

                    labels.append("HL")

                else:

                    labels.append("LL")

                last_low = row["Price"]

        swings = swings.copy()

        swings["Classification"] = labels

        return swings
            # =====================================================
    # STRENGTH CALCULATION
    # =====================================================

    def calculate_strength(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate swing strength based on
        price movement from previous swing.
        """

        if swings.empty:

            return swings

        strengths = []

        previous_price = None

        for _, row in swings.iterrows():

            if previous_price is None:

                strengths.append(0.0)

            else:

                strength = abs(
                    row["Price"] - previous_price
                )

                strengths.append(round(strength, 2))

            previous_price = row["Price"]

        swings = swings.copy()

        swings["Strength"] = strengths

        return swings

    # =====================================================
    # NOISE FILTER
    # =====================================================

    def filter_noise(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove insignificant swings using
        configurable thresholds.
        """

        if swings.empty:

            return swings

        filtered = []

        previous = None

        for _, row in swings.iterrows():

            if previous is None:

                filtered.append(row)

                previous = row

                continue

            price_distance = abs(
                row["Price"] - previous["Price"]
            )

            candle_distance = (
                row["Index"] - previous["Index"]
            )

            if (
                price_distance
                < self.config.minimum_price_distance
            ):

                continue

            if (
                candle_distance
                < self.config.minimum_candle_distance
            ):

                continue

            filtered.append(row)

            previous = row

        result = pd.DataFrame(filtered)

        result.reset_index(
            drop=True,
            inplace=True,
        )

        return result

    # =====================================================
    # FINALIZE
    # =====================================================

    def finalize(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Final cleanup before returning.
        """

        if swings.empty:

            return swings

        swings = swings.copy()

        swings.sort_values(
            "Index",
            inplace=True,
        )

        swings.reset_index(
            drop=True,
            inplace=True,
        )

        return swings
            # =====================================================
    # RUN ENGINE
    # =====================================================

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute Swing Detection Pipeline.

        Pipeline
        --------
        1. Validate input
        2. Detect pivot highs/lows
        3. Remove duplicate swings
        4. Classify HH/HL/LH/LL
        5. Calculate swing strength
        6. Filter insignificant swings
        7. Finalize output

        Returns
        -------
        pandas.DataFrame
        """

        self.log("Running Swing Engine V3")

        # --------------------------------------------
        # Validate
        # --------------------------------------------

        self.validate(df)

        # --------------------------------------------
        # Detect pivots
        # --------------------------------------------

        swings = self.detect_pivots(df)

        if swings.empty:

            self.log("No swings detected.")

            return swings

        # --------------------------------------------
        # Remove duplicate highs/lows
        # --------------------------------------------

        if self.config.filter_duplicates:

            swings = self.remove_duplicates(swings)

        # --------------------------------------------
        # Classify
        # --------------------------------------------

        swings = self.classify_swings(swings)

        # --------------------------------------------
        # Swing Strength
        # --------------------------------------------

        if self.config.calculate_strength:

            swings = self.calculate_strength(swings)

        # --------------------------------------------
        # Noise Filter
        # --------------------------------------------

        swings = self.filter_noise(swings)

        # --------------------------------------------
        # Final Cleanup
        # --------------------------------------------

        swings = self.finalize(swings)

        self.log(
            f"{len(swings)} swings detected."
        )

        return swings