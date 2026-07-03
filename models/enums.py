"""
=========================================================
Project FALCON
Enums
Version : 1.0
=========================================================
"""

from enum import Enum, auto


# =========================================================
# Trend
# =========================================================

class Trend(Enum):

    UNKNOWN = auto()

    RANGE = auto()

    POTENTIAL_UPTREND = auto()

    CONFIRMED_UPTREND = auto()

    WEAKENING_UPTREND = auto()

    POTENTIAL_DOWNTREND = auto()

    CONFIRMED_DOWNTREND = auto()

    WEAKENING_DOWNTREND = auto()


# =========================================================
# Market Bias
# =========================================================

class Bias(Enum):

    NEUTRAL = auto()

    BULLISH = auto()

    BEARISH = auto()


# =========================================================
# Market Strength
# =========================================================

class Strength(Enum):

    VERY_WEAK = auto()

    WEAK = auto()

    NORMAL = auto()

    STRONG = auto()

    VERY_STRONG = auto()


# =========================================================
# Structure Events
# =========================================================

class StructureEvent(Enum):

    NONE = auto()

    BOS_BULLISH = auto()

    BOS_BEARISH = auto()

    CHOCH_BULLISH = auto()

    CHOCH_BEARISH = auto()

    LIQUIDITY_SWEEP = auto()


# =========================================================
# Trade Signal
# =========================================================

class Signal(Enum):

    NO_TRADE = auto()

    WATCHLIST = auto()

    BUY = auto()

    SELL = auto()


# =========================================================
# Session
# =========================================================

class Session(Enum):

    PREMARKET = auto()

    OPENING = auto()

    MORNING = auto()

    MIDDAY = auto()

    AFTERNOON = auto()

    CLOSING = auto()

    CLOSED = auto()


# =========================================================
# Volatility
# =========================================================

class Volatility(Enum):

    LOW = auto()

    NORMAL = auto()

    HIGH = auto()


# =========================================================
# Trade Direction
# =========================================================

class Direction(Enum):

    LONG = auto()

    SHORT = auto()

    NONE = auto()