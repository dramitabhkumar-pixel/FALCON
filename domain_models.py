"""
==========================================================
FALCON MODELS
Version : 1.0

Centralized dataclasses used across the entire FALCON
trading system.

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from dataclasses import dataclass, field
from typing import Optional, List


# ==========================================================
# SWING
# ==========================================================

@dataclass
class Swing:

    index: int
    price: float
    type: str          # HIGH / LOW
    timestamp: Optional[str] = None


# ==========================================================
# MARKET CONTEXT
# ==========================================================

@dataclass
class MarketContext:

    trend: str
    bias: str
    strength: str
    volatility: str
    session: str


# ==========================================================
# MARKET STRUCTURE
# ==========================================================

@dataclass
class MarketStructure:

    trend: str

    last_high_type: str
    last_low_type: str

    protected_high: Optional[float]
    protected_low: Optional[float]

    bos: bool
    choch: bool


# ==========================================================
# FIBONACCI
# ==========================================================

@dataclass
class FibonacciLevels:

    high: float
    low: float

    fib_0: float
    fib_23_6: float
    fib_38_2: float
    fib_50: float
    fib_61_8: float
    fib_78_6: float
    fib_100: float

    golden_zone_top: float
    golden_zone_bottom: float


# ==========================================================
# TRENDLINE
# ==========================================================

@dataclass
class TrendLine:

    slope: float
    intercept: float

    start_index: int
    end_index: int

    direction: str


# ==========================================================
# LIQUIDITY
# ==========================================================

@dataclass
class LiquidityZone:

    level: float

    zone_type: str

    swept: bool = False


# ==========================================================
# ORDER BLOCK
# ==========================================================

@dataclass
class OrderBlock:

    high: float
    low: float

    bullish: bool
    mitigated: bool = False


# ==========================================================
# FAIR VALUE GAP
# ==========================================================

@dataclass
class FairValueGap:

    high: float
    low: float

    bullish: bool
    filled: bool = False


# ==========================================================
# TRADE SIGNAL
# ==========================================================

@dataclass
class TradeSignal:

    symbol: str

    direction: str

    entry: float

    STOPLOSS: float

    target: float

    confidence: float

    reason: str


# ==========================================================
# POSITION
# ==========================================================

@dataclass
class Position:

    symbol: str

    quantity: int

    entry_price: float

    STOPLOSS: float

    target: float

    pnl: float = 0.0

    open: bool = True


# ==========================================================
# RISK PROFILE
# ==========================================================

@dataclass
class RiskProfile:

    account_size: float

    risk_percent: float

    max_loss: float

    max_position_size: float


# ==========================================================
# CONFLUENCE
# ==========================================================

@dataclass
class ConfluenceScore:

    score: float

    reasons: List[str] = field(default_factory=list)


# ==========================================================
# EXECUTION RESULT
# ==========================================================

@dataclass
class ExecutionResult:

    success: bool

    order_id: Optional[str]

    message: str


# ==========================================================
# CANDLE
# ==========================================================

@dataclass
class Candle:

    timestamp: str

    open: float

    high: float

    low: float

    close: float

    volume: float


# ==========================================================
# MARKET SESSION
# ==========================================================

@dataclass
class SessionInfo:

    name: str

    start_time: str

    end_time: str

    active: bool