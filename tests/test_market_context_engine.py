"""
=========================================================
PROJECT FALCON
Test Market Context Engine
=========================================================
"""

from engine.market_context_engine import MarketContextEngine
from models.enums import (
    Bias,
    Strength,
    Trend,
)
from models.indicator_result import IndicatorResult
from models.market_context import MarketContext


def test_bullish_market_context():

    engine = MarketContextEngine()

    context = MarketContext()

    indicators = IndicatorResult(

        ema_fast=105.0,

        ema_slow=100.0,

        ema_alignment=True,

        rsi=65.0,

        adx=28.0,

        atr=120.0,

        avg_atr=100.0,

        high_volatility=True,

        volume=100000,

        valid=True,

    )

    result = engine.analyze(
        context,
        indicators,
    )

    assert result.trend.trend == Trend.CONFIRMED_UPTREND

    assert result.trend.bias == Bias.BULLISH

    assert result.trend.strength == Strength.STRONG

    assert result.indicators.ema_fast == 105.0

    assert result.indicators.ema_slow == 100.0


def test_bearish_market_context():

    engine = MarketContextEngine()

    context = MarketContext()

    indicators = IndicatorResult(

        ema_fast=95.0,

        ema_slow=100.0,

        ema_alignment=False,

        rsi=35.0,

        adx=30.0,

        atr=90.0,

        avg_atr=100.0,

        high_volatility=False,

        volume=90000,

        valid=True,

    )

    result = engine.analyze(
        context,
        indicators,
    )

    assert result.trend.trend == Trend.CONFIRMED_DOWNTREND

    assert result.trend.bias == Bias.BEARISH

    assert result.trend.strength == Strength.STRONG


def test_range_market_context():

    engine = MarketContextEngine()

    context = MarketContext()

    indicators = IndicatorResult(

        ema_fast=100.0,

        ema_slow=100.0,

        ema_alignment=False,

        rsi=50.0,

        adx=12.0,

        atr=80.0,

        avg_atr=100.0,

        high_volatility=False,

        volume=50000,

        valid=True,

    )

    result = engine.analyze(
        context,
        indicators,
    )

    assert result.trend.trend == Trend.RANGE

    assert result.trend.bias == Bias.NEUTRAL

    assert result.trend.strength == Strength.NORMAL


def test_invalid_indicator_result():

    engine = MarketContextEngine()

    context = MarketContext()

    indicators = IndicatorResult(
        valid=False,
    )

    try:

        engine.analyze(
            context,
            indicators,
        )

        assert False

    except ValueError:

        assert True


def test_none_context():

    engine = MarketContextEngine()

    indicators = IndicatorResult(
        valid=True,
    )

    try:

        engine.analyze(
            None,
            indicators,
        )

        assert False

    except ValueError:

        assert True


def test_none_indicator_result():

    engine = MarketContextEngine()

    context = MarketContext()

    try:

        engine.analyze(
            context,
            None,
        )

        assert False

    except ValueError:

        assert True