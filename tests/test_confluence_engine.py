"""
=========================================================
PROJECT FALCON
Test Confluence Engine
=========================================================
"""

from engine.confluence_engine import ConfluenceEngine

from models.trade_setup import TradeSetup

from models.enums import (
    Trend,
    Structure,
    Direction,
    Bias,
    Strength,
)


def build_long_setup():

    return TradeSetup(

        trend=Trend.CONFIRMED_UPTREND,

        bias=Bias.BULLISH,

        strength=Strength.STRONG,

        structure=Structure.BULLISH,

        ema_fast=51000,

        ema_slow=50800,

        ema_alignment=True,

        rsi=65,

        adx=28,

        atr=100,

        high_volatility=True,

        volume=100000,

        liquidity=True,

        fibonacci=True,

        golden_zone=True,

        bos=True,

        choch=True,

        equal_highs=False,

        equal_lows=True,

        order_block=True,

        fair_value_gap=True,

        direction=Direction.LONG,

        valid=True,

    )


def build_short_setup():

    return TradeSetup(

        trend=Trend.CONFIRMED_DOWNTREND,

        bias=Bias.BEARISH,

        strength=Strength.STRONG,

        structure=Structure.BEARISH,

        ema_fast=50000,

        ema_slow=50200,

        ema_alignment=False,

        rsi=35,

        adx=30,

        atr=110,

        high_volatility=True,

        volume=120000,

        liquidity=True,

        fibonacci=True,

        golden_zone=True,

        bos=True,

        choch=True,

        equal_highs=True,

        equal_lows=False,

        order_block=True,

        fair_value_gap=True,

        direction=Direction.SHORT,

        valid=True,

    )


def test_long_confluence():

    engine = ConfluenceEngine()

    setup = build_long_setup()

    result = engine.evaluate(
        setup,
    )

    assert result.valid is True

    assert result.direction == Direction.LONG

    assert result.trend_alignment is True

    assert result.structure_alignment is True

    assert result.ema_alignment is True

    assert result.momentum_confirmation is True

    assert result.liquidity_confirmation is True

    assert result.golden_zone_confirmation is True

    assert len(result.reasons) > 0


def test_short_confluence():

    engine = ConfluenceEngine()

    setup = build_short_setup()

    result = engine.evaluate(
        setup,
    )

    assert result.valid is True

    assert result.direction == Direction.SHORT

    assert result.trend_alignment is True

    assert result.structure_alignment is True

    assert result.momentum_confirmation is True


def test_failed_alignment_detection():

    engine = ConfluenceEngine()

    setup = build_long_setup()

    setup.trend = Trend.CONFIRMED_DOWNTREND

    result = engine.evaluate(
        setup,
    )

    assert result.trend_alignment is False

    assert result.structure_alignment is True

    assert result.valid is True


def test_invalid_setup():

    engine = ConfluenceEngine()

    setup = TradeSetup(
        valid=False,
    )

    try:

        engine.evaluate(
            setup,
        )

        assert False

    except ValueError:

        assert True


def test_none_setup():

    engine = ConfluenceEngine()

    try:

        engine.evaluate(
            None,
        )

        assert False

    except ValueError:

        assert True