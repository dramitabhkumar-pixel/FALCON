# ============================================================
# FALCON Trading System
# File: core/enums.py
#
# Description:
# Centralized Enumerations used throughout the FALCON framework.
# Every engine should import enums from this file instead of using
# raw strings.
#
# Author : OpenAI + Amitabh Kumar
# ============================================================

from enum import Enum, auto


# ============================================================
# MARKET CONTEXT
# ============================================================

class Trend(Enum):
    """Overall market trend."""

    UPTREND = auto()
    DOWNTREND = auto()
    RANGE = auto()


class Bias(Enum):
    """Directional bias."""

    BULLISH = auto()
    BEARISH = auto()
    NEUTRAL = auto()


class Strength(Enum):
    """Strength of the current trend."""

    WEAK = auto()
    NORMAL = auto()
    STRONG = auto()


# ============================================================
# SWING ENGINE
# ============================================================

class SwingType(Enum):
    """Swing point classification."""

    HIGH = auto()
    LOW = auto()


class SwingStrength(Enum):
    """Quality of a swing."""

    MINOR = auto()
    MAJOR = auto()


# ============================================================
# MARKET STRUCTURE
# ============================================================

class StructureType(Enum):
    """Market structure labels."""

    HH = auto()      # Higher High
    HL = auto()      # Higher Low
    LH = auto()      # Lower High
    LL = auto()      # Lower Low


class BreakType(Enum):
    """Structure break type."""

    BOS = auto()     # Break of Structure
    CHOCH = auto()   # Change of Character


# ============================================================
# LIQUIDITY
# ============================================================

class LiquidityType(Enum):
    """Liquidity classification."""

    BUY_SIDE = auto()
    SELL_SIDE = auto()
    INTERNAL = auto()
    EXTERNAL = auto()


# ============================================================
# FAIR VALUE GAP
# ============================================================

class FVGType(Enum):
    """Fair Value Gap direction."""

    BULLISH = auto()
    BEARISH = auto()


class FVGStatus(Enum):
    """Current state of the FVG."""

    OPEN = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()


# ============================================================
# ORDER BLOCK
# ============================================================

class OrderBlockType(Enum):
    """Order Block direction."""

    BULLISH = auto()
    BEARISH = auto()


class OrderBlockStatus(Enum):
    """Order Block state."""

    ACTIVE = auto()
    MITIGATED = auto()
    INVALIDATED = auto()


# ============================================================
# PREMIUM / DISCOUNT
# ============================================================

class PriceZone(Enum):
    """Premium / Discount classification."""

    PREMIUM = auto()
    EQUILIBRIUM = auto()
    DISCOUNT = auto()


# ============================================================
# ENTRY ENGINE
# ============================================================

class SignalType(Enum):
    """Trading signal."""

    BUY = auto()
    SELL = auto()
    HOLD = auto()


class EntryQuality(Enum):
    """Confidence of an entry."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    INSTITUTIONAL = auto()


# ============================================================
# EXECUTION
# ============================================================

class OrderSide(Enum):
    """Trade direction."""

    LONG = auto()
    SHORT = auto()


class OrderType(Enum):
    """Execution order type."""

    MARKET = auto()
    LIMIT = auto()
    STOP = auto()


class OrderStatus(Enum):
    """Order lifecycle."""

    CREATED = auto()
    PENDING = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()


# ============================================================
# POSITION MANAGEMENT
# ============================================================

class PositionStatus(Enum):
    """Current position state."""

    OPEN = auto()
    CLOSED = auto()


class ExitReason(Enum):
    """Reason for exiting a trade."""

    TARGET = auto()
    STOPLOSS = auto()
    TRAILING_STOP = auto()
    MANUAL = auto()
    TIME_EXIT = auto()
    INVALIDATION = auto()


class TradeResult(Enum):
    """Final trade outcome."""

    WIN = auto()
    LOSS = auto()
    BREAKEVEN = auto()


# ============================================================
# RISK ENGINE
# ============================================================

class RiskLevel(Enum):
    """Risk profile."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


# ============================================================
# SESSION ENGINE
# ============================================================

class TradingSession(Enum):
    """Market session."""

    PRE_MARKET = auto()
    OPENING = auto()
    MORNING = auto()
    MIDDAY = auto()
    AFTERNOON = auto()
    CLOSING = auto()
    CLOSED = auto()


# ============================================================
# MULTI-TIMEFRAME ENGINE
# ============================================================

class Timeframe(Enum):
    """Supported chart timeframes."""

    M1 = "1m"
    M3 = "3m"
    M5 = "5m"
    M10 = "10m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"


# ============================================================
# FALCON SYSTEM
# ============================================================

class EngineState(Enum):
    """State of an engine."""

    IDLE = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()