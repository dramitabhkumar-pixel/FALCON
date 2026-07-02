"""
=========================================================
Project FALCON
Swing Data Model
=========================================================
"""

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class SwingPoint:
    """
    Represents a market swing.
    """

    index: int
    datetime: Optional[pd.Timestamp]
    price: float
    swing_type: str
    classification: str = ""