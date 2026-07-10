"""
=========================================================
PROJECT FALCON
Daily Pivot Engine
=========================================================

Calculates Floor Trader Pivot Levels
using the previous trading day's OHLC.
"""

from models.daily_pivot import DailyPivot


class DailyPivotEngine:
    """
    Calculates Floor Trader Pivot Levels
    from the previous trading day's OHLC.
    """

    def __init__(self):
        """Initialize Daily Pivot Engine."""
        pass

    def calculate(
        self,
        high: float,
        low: float,
        close: float,
    ) -> DailyPivot:
        """
        Calculate Floor Trader Pivot Levels.

        Parameters
        ----------
        high : float
            Previous Day High

        low : float
            Previous Day Low

        close : float
            Previous Day Close

        Returns
        -------
        DailyPivot
        """

        # -------------------------
        # Input Validation
        # -------------------------
        if high <= low:
            raise ValueError(
                "Previous day High must be greater than Previous day Low."
            )

        if not (low <= close <= high):
            raise ValueError(
                "Previous day Close must lie between High and Low."
            )

        # -------------------------
        # Central Pivot
        # -------------------------
        pp = (high + low + close) / 3

        # -------------------------
        # Central Pivot Range
        # -------------------------
        bc = (high + low) / 2
        tc = (2 * pp) - bc

        # -------------------------
        # Resistance Levels
        # -------------------------
        r1 = (2 * pp) - low
        r2 = pp + (high - low)
        r3 = high + (2 * (pp - low))

        # -------------------------
        # Support Levels
        # -------------------------
        s1 = (2 * pp) - high
        s2 = pp - (high - low)
        s3 = low - (2 * (high - pp))

        # -------------------------
        # Return Immutable Model
        # -------------------------
        return DailyPivot(
            pp=round(pp, 2),
            bc=round(bc, 2),
            tc=round(tc, 2),
            r1=round(r1, 2),
            r2=round(r2, 2),
            r3=round(r3, 2),
            s1=round(s1, 2),
            s2=round(s2, 2),
            s3=round(s3, 2),
        )