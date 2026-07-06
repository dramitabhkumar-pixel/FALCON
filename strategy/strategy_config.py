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