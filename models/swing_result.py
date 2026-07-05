"""
=========================================================
Project FALCON
Swing Result Model
=========================================================
"""

from dataclasses import dataclass, field
import pandas as pd


@dataclass
class SwingResult:
    """
    Standard output from Swing Engine.
    """

    swings: pd.DataFrame = field(default_factory=pd.DataFrame)

    last_swing_high: float | None = None

    last_swing_low: float | None = None

    trend: str = "UNKNOWN"

    total_swings: int = 0

    is_valid: bool = False