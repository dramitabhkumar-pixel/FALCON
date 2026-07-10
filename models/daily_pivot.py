"""
=========================================================
PROJECT FALCON
Daily Pivot Model
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DailyPivot:
    """Floor Trader Pivot Levels"""

    pp: float
    bc: float
    tc: float

    r1: float
    r2: float
    r3: float

    s1: float
    s2: float
    s3: float