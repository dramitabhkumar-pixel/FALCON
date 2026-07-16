"""
=========================================================
Project FALCON
Master Market Context
Version : 2.1
=========================================================

Shared object passed between every engine.

Pipeline
--------
Daily Pivot Engine
        ↓
Daily Context Engine
        ↓
Indicator Engine
        ↓
Swing Engine
        ↓
Liquidity Engine
        ↓
Fibonacci Engine
        ↓
Confidence Engine
        ↓
Confluence Engine
        ↓
Entry Engine
        ↓
Trade Manager
        ↓
Structure Engine
        ↓
Exit Engine
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from models.enums import (
    Trend,
    Bias,
    Strength,
    StructureEvent,
    Signal,
    CPRRelation,
    CPRWidth,
    GapType,
)


# =========================================================
# TREND STATE
# =========================================================

@dataclass(slots=True)
class TrendState:
    """Stores the current market trend."""

    trend: Trend = Trend.UNKNOWN
    strength: Strength = Strength.NORMAL
    bias: Bias = Bias.NEUTRAL


# =========================================================
# STRUCTURE STATE
# =========================================================

@dataclass(slots=True)
class StructureState:
    """Market Structure information."""

    bos: bool = False
    choch: bool = False
    liquidity_sweep: bool = False
    last_event: StructureEvent = StructureEvent.NONE


# =========================================================
# FIBONACCI STATE
# =========================================================

@dataclass(slots=True)
class FibonacciState:
    """Fibonacci information."""

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
    """Indicator values."""

    ema_fast: Optional[float] = None
    ema_slow: Optional[float] = None
    ema_alignment: bool = False

    rsi: Optional[float] = None
    adx: Optional[float] = None

    atr: Optional[float] = None
    atr_ma: Optional[float] = None
    atr_expanding: bool = False


# =========================================================
# DAILY STATE
# =========================================================

@dataclass(slots=True)
class DailyState:
    """Daily market context."""

    bias: Bias = Bias.NEUTRAL
    cpr_relation: CPRRelation = CPRRelation.INSIDE
    cpr_width: CPRWidth = CPRWidth.NORMAL
    gap: GapType = GapType.NONE


# =========================================================
# CONFLUENCE STATE
# =========================================================

@dataclass(slots=True)
class ConfluenceState:
    """Strategy confluence."""

    score: int = 0
    signal: Signal = Signal.NO_TRADE
    confidence: float = 0.0


# =========================================================
# TRADE STATE
# =========================================================

@dataclass(slots=True)
class TradeState:
    """Current trade setup."""

    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    target: Optional[float] = None
    risk_reward: Optional[float] = None


# =========================================================
# MASTER MARKET CONTEXT
# =========================================================

@dataclass(slots=True)
class MarketContext:
    """Shared object passed between all engines."""

    swings: List[Any] = field(default_factory=list)
    candles: List[Any] = field(default_factory=list)

    trend: TrendState = field(default_factory=TrendState)
    structure: StructureState = field(default_factory=StructureState)
    fibonacci: FibonacciState = field(default_factory=FibonacciState)
    daily: DailyState = field(default_factory=DailyState)
    indicators: IndicatorState = field(default_factory=IndicatorState)
    confluence: ConfluenceState = field(default_factory=ConfluenceState)
    trade: TradeState = field(default_factory=TradeState)
