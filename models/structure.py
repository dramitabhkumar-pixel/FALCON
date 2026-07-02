"""
=========================================================
Project FALCON
Structure Model
=========================================================
"""

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class StructurePoint:
    """
    Represents a market structure event.
    """

    index: int
    datetime: Optional[pd.Timestamp]
    signal: str
    price: float