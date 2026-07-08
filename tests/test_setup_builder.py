"""
=========================================================
PROJECT FALCON
Setup Builder Validation
=========================================================
"""

import pandas as pd

from strategy.setup_builder import SetupBuilder
from engine.swing_engine import SwingEngine


# =========================================================
# LOAD REAL MARKET DATA
# =========================================================

def load_test_data():

    df = pd.read_csv("data/bank_nifty_15min.csv")

    df = df.tail(500).reset_index(drop=True)

    return df


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 70)
    print("SETUP BUILDER VALIDATION")
    print("=" * 70)

    # -----------------------------------------------------
    # Load Data
    # -----------------------------------------------------

    df = load_test_data()

    print(f"\nLoaded Candles : {len(df)}")

    # -----------------------------------------------------
    # Swing Engine Precheck
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("SWING ENGINE PRECHECK")
    print("=" * 70)

    swing_engine = SwingEngine()

    swings = swing_engine.run(df)

    print(f"\nDetected Swings : {len(swings)}")

    if swings.empty:

        raise RuntimeError(
            "Swing Engine detected no swings on BankNifty data."
        )

    print("\nLatest Swings\n")
    print(swings.tail())

    # -----------------------------------------------------
    # Setup Builder
    # -----------------------------------------------------

    builder = SetupBuilder()

    latest = df.iloc[-1]

    setup = builder.build(

        dataframe=df,

        ema_fast=float(latest["Close"]),

        ema_slow=float(df["Close"].tail(20).mean()),

        rsi=65.0,

        adx=30.0,

        atr=100.0,

        avg_atr=80.0,

        volume=float(latest["Volume"]),

        close=float(latest["Close"]),

        liquidity="BUY_SIDE",

    )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    print()

    print("=" * 70)
    print("TRADE SETUP")
    print("=" * 70)

    print(f"Trend            : {setup.trend}")
    print(f"Structure        : {setup.structure}")
    print(f"Market Context   : {setup.market_context}")

    print()

    print(f"EMA Alignment    : {setup.ema_alignment}")
    print(f"Golden Zone      : {setup.golden_zone}")
    print(f"Liquidity        : {setup.liquidity}")
    print(f"Fibonacci        : {setup.fibonacci}")

    print()

    print(f"Direction        : {setup.direction}")
    print(f"Entry            : {setup.entry_price}")
    print(f"Stop Loss        : {setup.stop_loss}")
    print(f"Target           : {setup.target_price}")
    print(f"Risk Reward      : {setup.risk_reward}")

    print()

    print(f"Confluence       : {setup.confluence}")
    print(f"Valid            : {setup.valid}")

    print()

    print("Reasons")

    if setup.reasons:

        for reason in setup.reasons:

            print(f" - {reason}")

    else:

        print(" None")

    print()

    print("=" * 70)
    print("TEST PASSED")
    print("=" * 70)


# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":

    main()