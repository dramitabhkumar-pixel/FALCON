"""
=========================================================
Project FALCON
Swing Engine Validation
=========================================================
"""

import pandas as pd

from engine.swing_engine import SwingEngine, SwingConfig


def print_result(title, result):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if result.empty:

        print("NO SWINGS DETECTED")
        return

    print(result)

    print("\nColumns")

    print(result.columns.tolist())

    print("\nTotal Swings :", len(result))


# ------------------------------------------------------
# Create Sample Data
# ------------------------------------------------------

data = {

    "Open": [
        100,102,104,107,110,108,106,109,112,115,
        113,110,108,111,114,118,116,114,112,110,
        108,106,109,112,115,117,116,114,113,111
    ],

    "High": [
        102,104,107,111,112,110,108,112,116,118,
        115,112,110,114,118,120,118,116,114,112,
        110,109,112,116,118,119,118,116,114,112
    ],

    "Low": [
        99,101,103,106,108,105,104,107,110,112,
        110,107,105,108,112,115,113,111,109,107,
        105,104,107,110,113,115,114,112,110,109
    ],

    "Close": [
        101,103,106,110,109,106,107,111,115,114,
        111,108,109,113,117,116,114,112,110,108,
        106,108,111,115,117,116,115,113,111,110
    ]

}

df = pd.DataFrame(data)

engine = SwingEngine(

    SwingConfig(

        left_bars=2,

        right_bars=2,

        minimum_price_distance=0,

        minimum_candle_distance=1,

    )

)

result = engine.run(df)

print_result(

    "SWING ENGINE TEST",

    result,

)

print("\nValidation")

print("---------------------------")

print("Chronological :",

      result["Index"].is_monotonic_increasing)

print("Duplicate Types :",

      any(

          result["Type"].iloc[i]

          ==

          result["Type"].iloc[i+1]

          for i in range(len(result)-1)

      ))

print("Strength Exists :",

      "Strength" in result.columns)

print("Classification Exists :",

      "Classification" in result.columns)

print("\nTEST COMPLETED")