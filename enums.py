from enum import Enum


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIAL = "PARTIAL"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXITED = "EXITED"


class Trend(Enum):
    UP = "UP"
    DOWN = "DOWN"
    RANGE = "RANGE"


class Bias(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class Strength(Enum):
    WEAK = "WEAK"
    NORMAL = "NORMAL"
    STRONG = "STRONG"


class Volatility(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class Session(Enum):
    PREMARKET = "PREMARKET"
    OPEN = "OPEN"
    MIDDAY = "MIDDAY"
    CLOSE = "CLOSE"
    UNKNOWN = "UNKNOWN"