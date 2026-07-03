"""
=========================================================
Project FALCON
Swing Data Model
Version : 2.0
=========================================================
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from models.enums import Direction


# =========================================================
# SWING TYPE
# =========================================================

class SwingType:
    """
    Swing Point Type
    """

    HIGH = "HIGH"
    LOW = "LOW"


# =========================================================
# STRUCTURE CLASSIFICATION
# =========================================================

class SwingClassification:
    """
    Structure Classification
    """

    UNKNOWN = "UNKNOWN"

    HH = "HH"      # Higher High
    HL = "HL"      # Higher Low

    LH = "LH"      # Lower High
    LL = "LL"      # Lower Low


# =========================================================
# SWING POINT
# =========================================================

@dataclass(slots=True)
class SwingPoint:
    """
    Represents one confirmed market swing.
    """

    # Candle Index
    index: int

    # Candle Timestamp
    datetime: Optional[pd.Timestamp]

    # Swing Price
    price: float

    # HIGH / LOW
    swing_type: str

    # HH / HL / LH / LL
    classification: str = SwingClassification.UNKNOWN

    # Used by Structure Engine
    confirmed: bool = False

    # Used by Liquidity Engine
    liquidity_taken: bool = False

    # Used by BOS / CHoCH Engine
    broken: bool = False

    # Optional score for future swing-quality ranking
    strength: float = 0.0

    # Trend direction inferred from this swing
    direction: Direction = Direction.NONE

    def is_high(self) -> bool:
        return self.swing_type == SwingType.HIGH

    def is_low(self) -> bool:
        return self.swing_type == SwingType.LOW

    def is_hh(self) -> bool:
        return self.classification == SwingClassification.HH

    def is_hl(self) -> bool:
        return self.classification == SwingClassification.HL

    def is_lh(self) -> bool:
        return self.classification == SwingClassification.LH

    def is_ll(self) -> bool:
        return self.classification == SwingClassification.LL

    def __str__(self) -> str:
        return (
            f"[{self.index}] "
            f"{self.swing_type} "
            f"{self.classification} "
            f"{self.price:.2f}"
        )