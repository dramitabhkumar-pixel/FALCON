"""
=========================================================
PROJECT FALCON
Trade Decision Model
=========================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TradeDecision:

    valid: bool = False

    signal: str = "NONE"

    entry_price: float = 0.0

    stop_loss: float = 0.0

    target_price: float = 0.0

    risk_reward: float = 0.0

    quantity: int = 0

    confidence: float = 0.0

    reasons: List[str] = field(default_factory=list)