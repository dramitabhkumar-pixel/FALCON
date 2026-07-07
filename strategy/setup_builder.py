"""
=========================================================
PROJECT FALCON
Setup Builder
Version : 1.0
=========================================================

Builds a complete TradeSetup object from raw market data.

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from turtle import setup

from models.trade_setup import TradeSetup

from engine.market_context_engine import MarketContextEngine
from engine.fibonacci_engine import FibonacciEngine
from engine.structure_engine import StructureEngine
from engine.confluence_engine import ConfluenceEngine


class SetupBuilder:
    """
    Builds a validated TradeSetup from indicator values
    and engine outputs.
    """

    def __init__(self):

        self.market_context_engine = MarketContextEngine()
        self.fibonacci_engine = FibonacciEngine()
        self.structure_engine = StructureEngine()
        self.confluence_engine = ConfluenceEngine()

    # =====================================================
    # MAIN BUILDER
    # =====================================================

    def build(
        self,
        *,
        ema_fast: float,
        ema_slow: float,
        rsi: float,
        adx: float,
        atr: float,
        avg_atr: float,
        volume: float,
        high: float,
        low: float,
        close: float,
        swings,
        liquidity: str,
    ) -> TradeSetup:
        """
        Build a complete TradeSetup from the supplied
        market information.
        """

        setup = TradeSetup()

        # -------------------------------------------------
        # Basic Indicators
        # -------------------------------------------------

        setup.ema_fast = ema_fast
        setup.ema_slow = ema_slow

        setup.rsi = rsi
        setup.adx = adx
        setup.atr = atr
        setup.volume = volume

        setup.ema_alignment = ema_fast > ema_slow

        # -------------------------------------------------
        # Market Context
        # -------------------------------------------------

        market_context = self.market_context_engine.analyze(
            adx=adx,
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            rsi=rsi,
            atr=atr,
            avg_atr=avg_atr,
        )

        setup.market_context = market_context.trend
        setup.trend = market_context.trend

        # -------------------------------------------------
        # Fibonacci
        # -------------------------------------------------

        fibonacci = self.fibonacci_engine.calculate(
            high=high,
            low=low,
            trend=market_context.trend,
        )

        setup.fibonacci = True

# -----------------------------------------
# Golden Zone Detection
# -----------------------------------------

        if market_context.trend == "UPTREND":

         setup.golden_zone = (
        fibonacci.golden_zone_bottom
        <= close
        <= fibonacci.golden_zone_top
    )

        elif market_context.trend == "DOWNTREND":

            setup.golden_zone = (
        fibonacci.golden_zone_top
        <= close
        <= fibonacci.golden_zone_bottom
    )

        else:

            setup.golden_zone = False

        # -------------------------------------------------
        # Structure Engine
        # -------------------------------------------------

        structure_df = self.structure_engine.run(swings)

        setup.structure = "NEUTRAL"
        setup.bos = False
        setup.choch = False

        if not structure_df.empty:

            latest = structure_df.iloc[-1]

            signal = str(latest["Signal"]).upper()

            if "BULLISH" in signal:
                setup.structure = "BULLISH"
                setup.bos = True

            elif "BEARISH" in signal:
                setup.structure = "BEARISH"
                setup.bos = True

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        setup.liquidity = liquidity in (
            "BUY_SIDE",
            "SELL_SIDE",
        )

        # -------------------------------------------------
        # Confluence Engine
        # -------------------------------------------------

        swing_direction = "UNKNOWN"

        if setup.structure == "BULLISH":
            swing_direction = "HH_HL"

        elif setup.structure == "BEARISH":
            swing_direction = "LH_LL"

        confluence = self.confluence_engine.evaluate(

            market_structure=setup.structure,

            market_context=setup.market_context,

            swing_direction=swing_direction,

            liquidity=liquidity,

            ema_bullish=setup.ema_alignment,

            adx=adx,

            rsi=rsi,

            atr_high=(atr >= avg_atr),

            fib_golden_zone=setup.golden_zone,
        )

        setup.confluence = confluence.score
        setup.reasons.extend(confluence.reasons)
        # -------------------------------------------------
        # Trading Direction
        # -------------------------------------------------

        if confluence.signal in ("BUY", "STRONG BUY"):

            setup.direction = "BUY"

        elif confluence.signal in ("SELL", "STRONG SELL"):

            setup.direction = "SELL"

        else:

            setup.direction = "NONE"

        # -------------------------------------------------
        # Trade Levels
        # -------------------------------------------------

        if setup.direction == "BUY":

            setup.entry_price = close

            setup.stop_loss = fibonacci.fib_61_8

            risk = setup.entry_price - setup.stop_loss

            if risk > 0:

                setup.target_price = (
                    setup.entry_price
                    + risk * 2.5
                )

        elif setup.direction == "SELL":

            setup.entry_price = close

            setup.stop_loss = fibonacci.fib_38_2

            risk = setup.stop_loss - setup.entry_price

            if risk > 0:

                setup.target_price = (
                    setup.entry_price
                    - risk * 2.5
                )

        # -------------------------------------------------
        # Final Builder Validation
        # -------------------------------------------------

        setup.valid = (
            setup.direction != "NONE"
            and setup.structure != "NEUTRAL"
            and setup.entry_price > 0
            and setup.stop_loss > 0
            and setup.target_price > 0
        )


        return setup
    