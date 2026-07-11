"""
=========================================================
PROJECT FALCON
Strategy Configuration
Version : 2.0
=========================================================

Central configuration for the Strategy Layer.

Changing values here changes the behaviour of the
entire trading system without modifying engine code.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
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

    RSI_SHORT = 40

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

    ATR_BUFFER = 1.0

    # =====================================================
    # FIBONACCI
    # =====================================================

    GOLDEN_ZONE_LOW = 0.382

    GOLDEN_ZONE_HIGH = 0.618

    STOPLOSS_LEVEL = 0.236

    # =====================================================
    # RISK MANAGEMENT
    # =====================================================

    MINIMUM_RR = 2.5

    REWARD_RATIO = 2.5

    MAX_RISK_PER_TRADE = 1.0      # %

    MAX_OPEN_TRADES = 1

    MINIMUM_POSITION_SIZE = 1

    # =====================================================
    # CONFIDENCE
    # =====================================================

    MINIMUM_CONFIDENCE = 80

    HIGH_CONFIDENCE = 90

    # =====================================================
    # TRADING SESSION
    # =====================================================

    MARKET_OPEN = "09:15"

    ENTRY_START = "09:30"

    ENTRY_END = "15:00"

    MARKET_CLOSE = "15:30"

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