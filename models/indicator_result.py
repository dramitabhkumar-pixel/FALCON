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


@dataclass(frozen=True, slots=True)
class IndicatorResult:

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
    atr_ma: float = 0.0
    atr_expanding: bool = False

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = False