"""
=========================================================
PROJECT FALCON
Strategy Configuration
=========================================================

Central configuration file for all strategy parameters.

Changing values here changes the behaviour of the
entire trading system without modifying engine code.
"""

from dataclasses import dataclass
from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class StrategyConfig:

    # =====================================================
    # TIMEFRAMES
    # =====================================================

    BASE_TIMEFRAME = "15m"
    HTF_1 = "1H"
    HTF_2 = "4H"
    HTF_3 = "Daily"

    # =====================================================
    # MOVING AVERAGES
    # =====================================================

    FAST_EMA = 5
    SLOW_EMA = 29

    # =====================================================
    # RSI
    # =====================================================

    RSI_PERIOD = 14
    RSI_LONG = 60
    RSI_SHORT = 55

    # =====================================================
    # ADX
    # =====================================================

    ADX_PERIOD = 14
    ADX_MINIMUM = 20

    # =====================================================
    # ATR
    # =====================================================

    ATR_PERIOD = 14
    ATR_MULTIPLIER = 1.5

    # =====================================================
    # FIBONACCI
    # =====================================================

    GOLDEN_ZONE_LOW = 0.382
    GOLDEN_ZONE_HIGH = 0.618

    STOPLOSS_LEVEL = 0.236

    # =====================================================
    # RISK MANAGEMENT
    # =====================================================

    MINIMUM_RR = 2.0

    REWARD_RATIO = 2.0

    ATR_MULTIPLIER = 1.5
    ATR_MA_PERIOD = 50
    POSITION_SIZE = 1

    MAX_RISK_PER_TRADE = 1.0      # %

    MAX_OPEN_TRADES = 1

    # =====================================================
    # CONFIDENCE ENGINE
    # =====================================================

    CONFIDENCE_WEIGHTS = {

        "trend": 20,

        "structure": 20,

        "ema_alignment": 10,

        "bos": 10,

        "choch": 10,

        "golden_zone": 10,

        "adx": 10,

        "rsi": 5,

        "liquidity": 5,
    }

    MINIMUM_CONFIDENCE = 80

    HIGH_CONFIDENCE = 90

    # =====================================================
    # TRADING SESSION
    # =====================================================

    MARKET_OPEN = time(9, 15)

    ENTRY_START = time(9, 45)

    ENTRY_END = time(15, 0)

    FORCED_EXIT = time(15, 15)

    MARKET_CLOSE = time(15, 30)
    # =====================================================
    # BACKTEST
    # =====================================================
    INITIAL_CAPITAL = 1_000_000

    SLIPPAGE = 0.0005

    BROKERAGE_PER_ORDER = 20

    # =====================================================
    # LOGGING
    # =====================================================

ENABLE_LOGGING = True

ENABLE_DEBUG = False

SAVE_TRADE_LOG = True


# ==========================================================
# Global Config Instance
# ==========================================================

CONFIG = StrategyConfig()