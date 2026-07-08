"""
=========================================================
PROJECT FALCON
Structure Engine Validation
=========================================================
"""

import pandas as pd

from engine.swing_engine import SwingEngine
from engine.structure_engine import StructureEngine


def load_data():

    df = pd.read_csv("data/bank_nifty_15min.csv")

    df = df.tail(500).reset_index(drop=True)

    return df


def main():

    print("=" * 70)
    print("STRUCTURE ENGINE VALIDATION")
    print("=" * 70)

    df = load_data()

    print(f"\nLoaded Candles : {len(df)}")

    # -------------------------------------------------
    # Swing Engine
    # -------------------------------------------------

    swing_engine = SwingEngine()

    swings = swing_engine.run(df)

    print(f"\nDetected Swings : {len(swings)}")

    if swings.empty:

        raise RuntimeError(
            "Swing Engine produced no swings."
        )

    print("\nLatest Swings\n")

    print(swings.tail())

    # -------------------------------------------------
    # Structure Engine
    # -------------------------------------------------

    structure_engine = StructureEngine()

    structure = structure_engine.run(swings)

    print()

    print("=" * 70)
    print("MARKET STRUCTURE")
    print("=" * 70)

    print(f"\nStructure Events : {len(structure)}")

    if structure.empty:

        print("\nNo BOS detected.")

    else:

        print()

        print(structure)

    print()

    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()