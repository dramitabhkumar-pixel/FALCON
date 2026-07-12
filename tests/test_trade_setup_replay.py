"""
=========================================================
PROJECT FALCON
Trade Setup Replay
=========================================================
"""

import pandas as pd

from strategy.setup_builder import SetupBuilder


def load_data():

    df = pd.read_csv("data/bank_nifty_15min.csv")

    df = df.reset_index(drop=True)

    return df


def main():

    print("=" * 70)
    print("PROJECT FALCON TRADE REPLAY")
    print("=" * 70)

    df = load_data()

    builder = SetupBuilder()

    trades = 0

    # ----------------------------------------
    # Replay
    # ----------------------------------------

    for i in range(150, len(df)):

        window = df.iloc[: i + 1].copy()

        latest = window.iloc[-1]
        try:

            setup = builder.build(

                dataframe=window,

                ema_fast=float(latest["Close"]),

                ema_slow=float(
                    window["Close"].tail(20).mean()
                ),

                rsi=65.0,

                adx=30.0,

                atr=100.0,

                avg_atr=80.0,

                volume=float(latest["Volume"]),

                close=float(latest["Close"]),

                liquidity="BUY_SIDE",

            )

        except Exception:

            continue

        if not setup.valid:

            continue

        trades += 1

        print()
        print("=" * 70)
        print(f"TRADE #{trades}")
        print("=" * 70)

        if "Datetime" in latest.index:

            print(
                f"Datetime      : {latest['Datetime']}"
            )

        elif "Date" in latest.index:

            print(
                f"Date          : {latest['Date']}"
            )

        print(
            f"Direction     : {setup.direction}"
        )

        print(
            f"Entry         : {setup.entry_price:.2f}"
        )

        print(
            f"Stop Loss     : {setup.STOPLOSS:.2f}"
        )

        print(
            f"Target        : {setup.target_price:.2f}"
        )

        print(
            f"Risk Reward   : {setup.risk_reward:.2f}"
        )

        print(
            f"Confluence    : {setup.confluence}"
        )

        print(
            f"Trend         : {setup.trend}"
        )

        print(
            f"Structure     : {setup.structure}"
        )

        print(
            f"Golden Zone   : {setup.golden_zone}"
        )

        print()

        if setup.reasons:

            print("Reasons:")

            for reason in setup.reasons:

                print(f"  • {reason}")

    print()
    print("=" * 70)
    print("REPLAY SUMMARY")
    print("=" * 70)

    print(f"Total Trades : {trades}")

    if trades == 0:

        print()

        print(
            "No valid trade setups were generated."
        )

        print(
            "This indicates that either:"
        )

        print(
            "1. Market conditions never met all strategy rules."
        )

        print(
            "2. Strategy thresholds are too restrictive."
        )

    else:

        print()

        print(
            "Replay completed successfully."
        )

    print("=" * 70)


if __name__ == "__main__":

    main()