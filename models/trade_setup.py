"""
=========================================================
PROJECT FALCON
Trade Setup Model
=========================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TradeSetup:
    # -------------------------
    # Market Trend
    # -------------------------
    trend: str = "RANGE"
    structure: str = "NEUTRAL"
    market_context: str = "NEUTRAL"

    # -------------------------
    # Technical Indicators
    # -------------------------
    ema_fast: float = 0.0
    ema_slow: float = 0.0
    ema_alignment: bool = False

    rsi: float = 50.0
    adx: float = 0.0
    atr: float = 0.0
    volume: float = 0.0

    # -------------------------
    # Smart Money Concepts
    # -------------------------
    liquidity: bool = False
    fibonacci: bool = False
    golden_zone: bool = False

    bos: bool = False
    choch: bool = False

    equal_highs: bool = False
    equal_lows: bool = False

    order_block: bool = False
    fair_value_gap: bool = False

    # -------------------------
    # Trade Information
    # -------------------------
    direction: str = "NONE"

    entry_price: float = 0.0
    stop_loss: float = 0.0
    target_price: float = 0.0

    risk_reward: float = 0.0

    # -------------------------
    # Strategy
    # -------------------------
    confidence: float = 0.0
    confluence: float = 0.0

    reasons: List[str] = field(default_factory=list)

    # -------------------------
    # Trade State
    # -------------------------
    valid: bool = False