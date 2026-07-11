"""
=========================================================
PROJECT FALCON
Strategy Engine Test
Version : 1.0
=========================================================
"""

from models.trade_setup import TradeSetup
from models.enums import (
    Trend,
    Bias,
    Strength,
    Structure,
    Direction,
)

from strategy.strategy_engine import StrategyEngine


def test_strategy_engine():

    setup = TradeSetup(

        trend=Trend.CONFIRMED_UPTREND,

        bias=Bias.BULLISH,

        strength=Strength.STRONG,

        structure=Structure.BULLISH,

        ema_fast=105,

        ema_slow=100,

        ema_alignment=True,

        rsi=65,

        adx=30,

        atr=12,

        high_volatility=True,

        volume=1500,

        liquidity=True,

        fibonacci=True,

        golden_zone=True,

        bos=True,

        choch=False,

        equal_highs=False,

        equal_lows=False,

        order_block=True,

        fair_value_gap=True,

        direction=Direction.LONG,

        valid=True,

        swing_high=110,

        swing_low=95,

        golden_zone_low=100,

        golden_zone_high=104,

        current_price=102,

    )

    engine = StrategyEngine()

    decision = engine.process(setup)

    assert decision is not None