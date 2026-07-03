"""
=========================================================
Project FALCON
Master Market Context
Version : 2.0
=========================================================
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from models.enums import (
    Trend,
    Bias,
    Strength,
    StructureEvent,
    Signal,
)


# =========================================================
# TREND STATE
# =========================================================

@dataclass(slots=True)
class TrendState:
    """
    Stores the current market trend.
    """

    trend: Trend = Trend.UNKNOWN

    strength: Strength = Strength.NORMAL

    bias: Bias = Bias.NEUTRAL


# =========================================================
# STRUCTURE STATE
# =========================================================

@dataclass(slots=True)
class StructureState:
    """
    Market Structure Information.
    """

    bos: bool = False

    choch: bool = False

    liquidity_sweep: bool = False

    last_event: StructureEvent = StructureEvent.NONE


# =========================================================
# FIBONACCI STATE
# =========================================================

@dataclass(slots=True)
class FibonacciState:
    """
    Fibonacci information.
    """

    swing_high: Optional[float] = None

    swing_low: Optional[float] = None

    golden_zone_low: Optional[float] = None

    golden_zone_high: Optional[float] = None

    premium: Optional[float] = None

    equilibrium: Optional[float] = None

    discount: Optional[float] = None


# =========================================================
# INDICATOR STATE
# =========================================================

@dataclass(slots=True)
class IndicatorState:
    """
    Indicator values.
    """

    ema_fast: Optional[float] = None

    ema_slow: Optional[float] = None

    adx: Optional[float] = None

    atr: Optional[float] = None

    rsi: Optional[float] = None

    volume: Optional[float] = None


# =========================================================
# CONFLUENCE STATE
# =========================================================

@dataclass(slots=True)
class ConfluenceState:
    """
    Strategy confluence.
    """

    score: int = 0

    signal: Signal = Signal.NO_TRADE

    confidence: float = 0.0


# =========================================================
# TRADE STATE
# =========================================================

@dataclass(slots=True)
class TradeState:
    """
    Current trade setup.
    """

    entry: Optional[float] = None

    stop_loss: Optional[float] = None

    target: Optional[float] = None

    risk_reward: Optional[float] = None


# =========================================================
# MASTER MARKET CONTEXT
# =========================================================

@dataclass(slots=True)
class MarketContext:
    """
    Shared object passed between every engine.

    Swing Engine
        ↓
    Structure Engine
        ↓
    Trend Engine
        ↓
    Liquidity Engine
        ↓
    Fibonacci Engine
        ↓
    Indicator Engine
        ↓
    Confluence Engine
        ↓
    Entry Engine
    """

    # Raw Data
    swings: List[Any] = field(default_factory=list)

    candles: List[Any] = field(default_factory=list)

    # Engine States
    trend: TrendState = field(default_factory=TrendState)

    structure: StructureState = field(default_factory=StructureState)

    fibonacci: FibonacciState = field(default_factory=FibonacciState)

    indicators: IndicatorState = field(default_factory=IndicatorState)

    confluence: ConfluenceState = field(default_factory=ConfluenceState)

    trade: TradeState = field(default_factory=TradeState)