"""
=========================================================
PROJECT FALCON
Indicator Result Model
Version : 1.0
=========================================================

Represents the output of the Indicator Engine.

Contains ONLY calculated indicator values.
No business logic.
No trading logic.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class IndicatorResult:
    """
    Output produced by Indicator Engine.
    """

    # =====================================================
    # Moving Averages
    # =====================================================

    ema_fast: float = 0.0

    ema_slow: float = 0.0

    ema_alignment: bool = False

    # =====================================================
    # Momentum
    # =====================================================

    rsi: float = 50.0

    adx: float = 0.0

    # =====================================================
    # Volatility
    # =====================================================

    atr: float = 0.0

    avg_atr: float = 0.0

    high_volatility: bool = False

    # =====================================================
    # Volume
    # =====================================================

    volume: float = 0.0

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False