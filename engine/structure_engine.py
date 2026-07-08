"""
=========================================================
PROJECT FALCON
Structure Engine
Version : 2.1
=========================================================

Converts Swing Engine classifications into
institutional market structure.

Pipeline

Validation
    ↓
Bullish BOS Detection
    ↓
Bearish BOS Detection
    ↓
Output Structure

Compatible with:

HIGH
LOW
HH
HL
LH
LL

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from __future__ import annotations

import pandas as pd

from core.base_engine import BaseEngine


class StructureEngine(BaseEngine):
    """
    Detects institutional market structure
    from Swing Engine output.
    """

    def __init__(self):

        super().__init__("StructureEngine")

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        swings: pd.DataFrame,
    ) -> None:

        if swings is None:

            raise ValueError(
                "Swing DataFrame is None."
            )

        if swings.empty:

            raise ValueError(
                "Swing DataFrame is empty."
            )

        required = [

            "Index",

            "Price",

            "Type",

            "Classification",

        ]

        for column in required:

            if column not in swings.columns:

                raise ValueError(

                    f"Missing required column: {column}"

                )

    # =====================================================
    # STRUCTURE DETECTION
    # =====================================================

    def detect_structure(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Detect Bullish and Bearish
        Break of Structure (BOS).
        """

        structure = []

        for _, row in swings.iterrows():

            classification = str(
                row["Classification"]
            ).upper()

            signal = None

            # ----------------------------------------
            # Bullish BOS
            # ----------------------------------------

            if classification == "HH":

                signal = "Bullish BOS"

            # ----------------------------------------
            # Bearish BOS
            # ----------------------------------------

            elif classification == "LL":

                signal = "Bearish BOS"

            if signal is None:

                continue

            structure.append(

                {

                    "Index": row["Index"],

                    "Signal": signal,

                    "Price": row["Price"],

                }

            )

        return pd.DataFrame(structure)
    
    # =====================================================
    # FINALIZE
    # =====================================================

    def finalize(
        self,
        structure: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Final cleanup before returning.
        """

        if structure.empty:

            return structure

        structure = structure.copy()

        structure.sort_values(
            "Index",
            inplace=True,
        )

        structure.reset_index(
            drop=True,
            inplace=True,
        )

        return structure

    # =====================================================
    # RUN ENGINE
    # =====================================================

    def run(
        self,
        swings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute Structure Detection Pipeline.
        """

        self.log(
            "Running Structure Engine V2.1"
        )

        # --------------------------------------------
        # Validate
        # --------------------------------------------

        self.validate(swings)

        # --------------------------------------------
        # Detect Structure
        # --------------------------------------------

        structure = self.detect_structure(
            swings
        )

        if structure.empty:

            self.log(
                "No market structure detected."
            )

            return structure

        # --------------------------------------------
        # Finalize
        # --------------------------------------------

        structure = self.finalize(
            structure
        )

        self.log(
            f"{len(structure)} structure events detected."
        )

        return structure