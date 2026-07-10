"""
=========================================================
PROJECT FALCON
Daily Pivot Engine Validation
=========================================================
"""

from engine.daily_pivot_engine import DailyPivotEngine


def main():

    engine = DailyPivotEngine()

    # Previous Day OHLC
    high = 120.0
    low = 100.0
    close = 116.0

    pivot = engine.calculate(
        high=high,
        low=low,
        close=close,
    )

    print("=" * 60)
    print("DAILY PIVOT ENGINE VALIDATION")
    print("=" * 60)

    print(f"High  : {high}")
    print(f"Low   : {low}")
    print(f"Close : {close}")

    print()

    print(f"PP : {pivot.pp}")
    print(f"BC : {pivot.bc}")
    print(f"TC : {pivot.tc}")

    print()

    print(f"R1 : {pivot.r1}")
    print(f"R2 : {pivot.r2}")
    print(f"R3 : {pivot.r3}")

    print()

    print(f"S1 : {pivot.s1}")
    print(f"S2 : {pivot.s2}")
    print(f"S3 : {pivot.s3}")

    print()
    print("✅ Daily Pivot Engine Validation Passed")


if __name__ == "__main__":
    main()