"""
=========================================================
PROJECT FALCON
Setup Builder
Version : 2.1
=========================================================

Builds a validated TradeSetup using the frozen
Project FALCON architecture.

Pipeline

Market Context
        ↓
Swing Engine V3.1
        ↓
Swing Fibonacci Engine V1.0
        ↓
Structure Engine V2.1
        ↓
Confluence Engine
        ↓
TradeSetup

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from __future__ import annotations
from turtle import setup

from models.trade_setup import TradeSetup
from models.market_context import MarketContext
from models.indicator_result import IndicatorResult
from models.enums import Direction, Structure
from engine.market_context_engine import MarketContextEngine
from engine.structure_engine import StructureEngine
from strategy.confluence_engine import ConfluenceEngine
from engine.swing_engine import SwingEngine
from engine.liquidity_engine import LiquidityEngine
from engine.swing_fibonacci_engine import SwingFibonacciEngine
   


class SetupBuilder:
    """
    Builds a fully validated TradeSetup by integrating
    all frozen Project FALCON engines.
    """

    def __init__(self):

        self.market_context_engine = MarketContextEngine()
        self.swing_engine = SwingEngine()
        self.liquidity_engine = LiquidityEngine()
        self.swing_fibonacci_engine = SwingFibonacciEngine()
        self.structure_engine = StructureEngine()
        self.confluence_engine = ConfluenceEngine()

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _inside_golden_zone(
        close: float,
        fibonacci,
    ) -> bool:
        """
        Check whether the current price lies inside the
        Golden Zone.
        """

        lower = min(
            fibonacci.golden_lower,
            fibonacci.golden_upper,
        )

        upper = max(
            fibonacci.golden_lower,
            fibonacci.golden_upper,
        )

        return lower <= close <= upper

    @staticmethod
    def _validate_swings(
        swings,
    ):

        if swings is None:

            raise ValueError(
                "Swing Engine returned None."
            )

        if swings.empty:

            raise ValueError(
                "Swing Engine returned no swings."
            )

    @staticmethod
    def _validate_structure(
        structure,
    ):

        if structure is None:

            raise ValueError(
                "Structure Engine returned None."
            )

    # =====================================================
    # MAIN BUILDER
    # =====================================================

    def build(
        self,
        *,
        dataframe,
        ema_fast: float,
        ema_slow: float,
        rsi: float,
        adx: float,
        atr: float,
        avg_atr: float,
        volume: float,
        close: float,
        
    ) -> TradeSetup:

        setup = TradeSetup()


        # -------------------------------------------------
        # Current Market State
        # -------------------------------------------------
        setup.current_price=close
        

        

        # -------------------------------------------------
        # Indicators
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
        indicators= IndicatorResult(
        
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            ema_alignment=ema_fast > ema_slow,
            rsi=rsi,
            atr=atr,
            avg_atr=avg_atr,
            high_volatility=atr >= avg_atr,
            adx=adx,
            volume=volume,
            valid=True

        )
        context=MarketContext()
        context = self.market_context_engine.analyze(
            context=context,
            indicators=indicators,
        )

        setup.trend = context.trend.trend
        setup.bias = context.trend.bias
        setup.strength = context.trend.strength

        # -------------------------------------------------
        # Swing Engine
        # -------------------------------------------------
        legacy_dataframe = dataframe.copy()
        legacy_dataframe.columns = [
            str(column).capitalize()
            for column in legacy_dataframe.columns
        ]
        swings = self.swing_engine.run(
            dataframe
        )

        self._validate_swings(
            swings
        )

        print("\n================ LAST 10 SWINGS ================")
        print(swings.tail(10))
        print("================================================\n")

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        liquidity = self.liquidity_engine.analyze(
           swings=swings,
              atr=atr,
        )
        print("\n========== LIQUIDITY DEBUG ==========")
        print("Buy Side :", liquidity.buy_side_liquidity)
        print("Sell Side:", liquidity.sell_side_liquidity)
        print("Equal Highs:", liquidity.equal_highs)
        print("Equal Lows :", liquidity.equal_lows)
        print("=====================================\n")

        # -------------------------------------------------
        # Swing Fibonacci
        # -------------------------------------------------

        fibonacci = self.swing_fibonacci_engine.calculate(

            df=dataframe,

            swings=swings,

        )

        if fibonacci is None:

            raise ValueError(
                "Swing Fibonacci calculation failed."
            )

        setup.fibonacci = True

        setup.golden_zone = self._inside_golden_zone(

            close=close,

            fibonacci=fibonacci,

        )
        # -------------------------------------------------
        # Populate TradeSetup
        # -------------------------------------------------
        setup.current_price = close

        setup.swing_high = fibonacci.swing_high
        setup.swing_low = fibonacci.swing_low

        setup.golden_zone_high = fibonacci.golden_upper
        setup.golden_zone_low = fibonacci.golden_lower

        print("\n===== FIBONACCI DEBUG =====")
        print("Close         :", close)
        print("Fib 38.2      :", fibonacci.fib_382)
        print("Fib 61.8      :", fibonacci.fib_618)
        print("Golden Lower  :", fibonacci.golden_lower)
        print("Golden Upper  :", fibonacci.golden_upper)
        print("Pullback      :", fibonacci.pullback_valid)
        print("===========================\n")

        setup.fibonacci = True

        setup.golden_zone = self._inside_golden_zone(
            close=close,
            fibonacci=fibonacci,
        )


        # -------------------------------------------------
        # Execution Inputs
        # -------------------------------------------------
        setup.current_price = close
        setup.swing_high = fibonacci.swing_high
        setup.swing_low = fibonacci.swing_low
        setup.golden_zone_low = fibonacci.golden_lower
        setup.golden_zone_high = fibonacci.golden_upper
        setup.fibonacci = True
        setup.golden_zone = self._inside_golden_zone(
            close=close,
            fibonacci=fibonacci,
        )

        # -------------------------------------------------
        # Structure Engine
        # -------------------------------------------------

        structure = self.structure_engine.run(
            swings
        )

        self._validate_structure(
            structure
        )

        setup.structure = Structure.UNKNOWN

        setup.bos = False

        setup.choch = False


        # -------------------------------------------------
        # Structure Interpretation
        # -------------------------------------------------

        if not structure.empty:

            latest = structure.iloc[-1]

            signal = str(
                latest["Signal"]
            ).upper()

            if "BULLISH" in signal:

                setup.structure = Structure.BULLISH
                setup.bos = True

            elif "BEARISH" in signal:

                setup.structure = Structure.BEARISH
                setup.bos = True

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        setup.liquidity = (
            bool(liquidity.buy_side_liquidity)
            or
            bool(liquidity.sell_side_liquidity)
        )

        # -------------------------------------------------
        # Swing Direction
        # -------------------------------------------------

        if setup.structure == Structure.BULLISH:

            swing_direction = "HH_HL"

        elif setup.structure == Structure.BEARISH:

            swing_direction = "LH_LL"

        else:

            swing_direction = "UNKNOWN"

        # -------------------------------------------------
        # Trading Direction
        # -------------------------------------------------
        if setup.structure == Structure.BULLISH:
            setup.direction = Direction.LONG
        elif setup.structure == Structure.BEARISH:
            setup.direction = Direction.SHORT
        else:
             setup.direction = Direction.NONE
        if setup.direction == Direction.LONG:
            setup.ema_alignment = ema_fast > ema_slow
        elif setup.direction == Direction.SHORT:
            setup.ema_alignment = ema_fast < ema_slow
        else:
            setup.ema_alignment = False



        # -------------------------------------------------
        # Confluence
        # -------------------------------------------------
        setup.valid=True
        print("DEBUG setup.valid before Confluence =", setup.valid)
        confluence = self.confluence_engine.evaluate(

            setup
            

        )


        setup.direction = confluence.direction

        setup.reasons.extend(
            confluence.reasons
        )

        

       

        # -------------------------------------------------
        # Final Validation
        # -------------------------------------------------


        print("\n========== SETUP DEBUG ==========")
        print("Direction      :", setup.direction)
        print("Structure      :", setup.structure)
        print("Fibonacci      :", setup.fibonacci)
        print("Pullback       :", fibonacci.pullback_valid)
        print("Golden Zone    :", setup.golden_zone)
        print("Trend          :", setup.trend)
        print("Bias           :", setup.bias)
        print("current price   :",setup.current_price)
        print("setup.valid     :",setup.valid)
        print("Swing High     :", setup.swing_high)
        print("Swing Low      :", setup.swing_low)
        print("Fib 38.2       :", fibonacci.fib_382)
        print("Fib 61.8       :", fibonacci.fib_618)
        print("Golden Lower   :", setup.golden_zone_low)
        print("Golden Upper   :", setup.golden_zone_high)

        print("Golden Zone    :", setup.golden_zone)
        print("Pullback       :", fibonacci.pullback_valid)
        print("Confluence     :", confluence.valid)
        print("=================================\n")


        
        
        
        print("=================================\n")

        
        setup.valid = (

            setup.direction != Direction.NONE

            and setup.structure != Structure.RANGE

            and setup.fibonacci

            and fibonacci.pullback_valid

            and setup.golden_zone

            and confluence.valid

        )

        return setup
        