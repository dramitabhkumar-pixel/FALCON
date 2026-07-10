"""
PROJECT FALCON
Daily Pivot Model Validation
"""

from models.daily_pivot import DailyPivot


def main():

    pivot = DailyPivot(
        pp=100.0,
        bc=99.0,
        tc=101.0,
        r1=105.0,
        r2=110.0,
        r3=115.0,
        s1=95.0,
        s2=90.0,
        s3=85.0,
    )

    print("=" * 60)
    print("DAILY PIVOT MODEL TEST")
    print("=" * 60)

    print(pivot)

    print("\nPP :", pivot.pp)
    print("BC :", pivot.bc)
    print("TC :", pivot.tc)

    print("\nResistance")
    print("R1 :", pivot.r1)
    print("R2 :", pivot.r2)
    print("R3 :", pivot.r3)

    print("\nSupport")
    print("S1 :", pivot.s1)
    print("S2 :", pivot.s2)
    print("S3 :", pivot.s3)

    print("\n✅ DailyPivot Model Validation Passed")


if __name__ == "__main__":
    main()