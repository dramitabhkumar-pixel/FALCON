"""
=========================================================
Project FALCON
Master Market Context
=========================================================
"""

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class TrendState:
    trend: str = "UNKNOWN"
    strength: str = "UNKNOWN"
    bias: str = "NEUTRAL"


@dataclass
class StructureState:
    bos: bool = False
    choch: bool = False
    liquidity_sweep: bool = False


@dataclass
class FibonacciState:
    swing_high: float | None = None
    swing_low: float | None = None
    golden_zone_low: float | None = None
    golden_zone_high: float | None = None


@dataclass
class IndicatorState:
    ema_fast: float | None = None
    ema_slow: float | None = None
    adx: float | None = None
    atr: float | None = None
    rsi: float | None = None


@dataclass
class ConfluenceState:
    score: int = 0
    signal: str = "NO TRADE"


@dataclass
class TradeState:
    entry: float | None = None
    stop_loss: float | None = None
    target: float | None = None


@dataclass
class MarketContext:

    swings: List[Any] = field(default_factory=list)

    trend: TrendState = field(default_factory=TrendState)

    structure: StructureState = field(default_factory=StructureState)

    fibonacci: FibonacciState = field(default_factory=FibonacciState)

    indicators: IndicatorState = field(default_factory=IndicatorState)

    confluence: ConfluenceState = field(default_factory=ConfluenceState)

    trade: TradeState = field(default_factory=TradeState)