"""
==========================================================
FALCON MARKET CONTEXT ENGINE
Version : 2.0

Determines overall market context from technical
indicators.

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from core.base_engine import BaseEngine
from core.models import MarketContext
from core.constants import (
    ADX_THRESHOLD,
    RSI_BUY_LEVEL,
    RSI_SELL_LEVEL,
)


class MarketContextEngine(BaseEngine):

    def __init__(self):
        super().__init__()

    def analyze(
        self,
        adx: float,
        ema_fast: float,
        ema_slow: float,
        rsi: float,
        atr: float,
        avg_atr: float,
    ) -> MarketContext:

        self.log("Running Market Context Engine")

        # -----------------------------------------
        # Trend
        # -----------------------------------------

        if ema_fast > ema_slow:
            trend = "UPTREND"

        elif ema_fast < ema_slow:
            trend = "DOWNTREND"

        else:
            trend = "RANGE"

        # -----------------------------------------
        # Strength
        # -----------------------------------------

        if adx >= ADX_THRESHOLD:
            strength = "STRONG"

        else:
            strength = "WEAK"

        # -----------------------------------------
        # Volatility
        # -----------------------------------------

        if atr >= avg_atr:
            volatility = "HIGH"

        else:
            volatility = "NORMAL"

        # -----------------------------------------
        # Bias
        # -----------------------------------------

        if trend == "UPTREND" and rsi >= RSI_BUY_LEVEL:
            bias = "BULLISH"

        elif trend == "DOWNTREND" and rsi <= RSI_SELL_LEVEL:
            bias = "BEARISH"

        else:
            bias = "NEUTRAL"

        # -----------------------------------------
        # Session
        # -----------------------------------------

        session = "REGULAR"

        return MarketContext(
            trend=trend,
            bias=bias,
            strength=strength,
            volatility=volatility,
            session=session,
        )