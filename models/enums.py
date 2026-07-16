"""
=========================================================
Project FALCON
Core Enums
Version : 2.0
=========================================================

Centralized enumerations used across the entire FALCON
architecture.
"""

from enum import Enum


class FalconEnum(str, Enum):
    """Base class for all FALCON enums."""

    def __str__(self) -> str:
        return self.value


class Trend(FalconEnum):
    UNKNOWN = "UNKNOWN"
    RANGE = "RANGE"
    POTENTIAL_UPTREND = "POTENTIAL_UPTREND"
    CONFIRMED_UPTREND = "CONFIRMED_UPTREND"
    WEAKENING_UPTREND = "WEAKENING_UPTREND"
    POTENTIAL_DOWNTREND = "POTENTIAL_DOWNTREND"
    CONFIRMED_DOWNTREND = "CONFIRMED_DOWNTREND"
    WEAKENING_DOWNTREND = "WEAKENING_DOWNTREND"


class Bias(FalconEnum):
    NEUTRAL = "NEUTRAL"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class Strength(FalconEnum):
    VERY_WEAK = "VERY_WEAK"
    WEAK = "WEAK"
    NORMAL = "NORMAL"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"


class Structure(FalconEnum):
    UNKNOWN = "UNKNOWN"
    RANGE = "RANGE"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class StructureEvent(FalconEnum):
    NONE = "NONE"
    BOS_BULLISH = "BOS_BULLISH"
    BOS_BEARISH = "BOS_BEARISH"
    CHOCH_BULLISH = "CHOCH_BULLISH"
    CHOCH_BEARISH = "CHOCH_BEARISH"
    LIQUIDITY_SWEEP = "LIQUIDITY_SWEEP"


class SwingType(FalconEnum):
    HIGH = "HIGH"
    LOW = "LOW"


class SwingClassification(FalconEnum):
    UNKNOWN = "UNKNOWN"
    HH = "HH"
    HL = "HL"
    LH = "LH"
    LL = "LL"


class FibonacciDirection(FalconEnum):
    NONE = "NONE"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class LiquidityType(FalconEnum):
    NONE = "NONE"
    EQUAL_HIGHS = "EQUAL_HIGHS"
    EQUAL_LOWS = "EQUAL_LOWS"
    BUY_SIDE = "BUY_SIDE"
    SELL_SIDE = "SELL_SIDE"


class Signal(FalconEnum):
    NO_TRADE = "NO_TRADE"
    WATCHLIST = "WATCHLIST"
    BUY = "BUY"
    SELL = "SELL"


class Session(FalconEnum):
    PREMARKET = "PREMARKET"
    OPENING = "OPENING"
    MORNING = "MORNING"
    MIDDAY = "MIDDAY"
    AFTERNOON = "AFTERNOON"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"


class Volatility(FalconEnum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class Direction(FalconEnum):
    NONE = "NONE"
    LONG = "LONG"
    SHORT = "SHORT"

# =========================================================
# TREND / MOMENTUM
# =========================================================

class Momentum(FalconEnum):
    """
    RSI based momentum confirmation.
    """

    WEAK = "WEAK"
    CONFIRMED = "CONFIRMED"


# =========================================================
# DAILY CONTEXT
# =========================================================

class CPRRelation(FalconEnum):
    """
    Current price position relative to the Central Pivot Range.
    """

    ABOVE = "ABOVE"
    INSIDE = "INSIDE"
    BELOW = "BELOW"


class CPRWidth(FalconEnum):
    """
    Width classification of the Central Pivot Range.
    """

    NARROW = "NARROW"
    NORMAL = "NORMAL"
    WIDE = "WIDE"


class GapType(FalconEnum):
    """
    Opening gap classification.
    """

    NONE = "NONE"
    GAP_UP = "GAP_UP"
    GAP_DOWN = "GAP_DOWN"


class ConfidenceGrade(FalconEnum):
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    A_PLUS = "A_PLUS"


class TradeStatus(FalconEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class ExitReason(FalconEnum):
    NONE = "NONE"
    TARGET = "TARGET"
    STOPLOSS = "STOPLOSS"
    TRAILING_STOP = "TRAILING_STOP"
    TIME_EXIT = "TIME_EXIT"
    OPPOSITE_SIGNAL = "OPPOSITE_SIGNAL"
    MARKET_CLOSE = "MARKET_CLOSE"
    MANUAL = "MANUAL"


class OrderBlockType(FalconEnum):
    NONE = "NONE"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class FVGType(FalconEnum):
    NONE = "NONE"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
