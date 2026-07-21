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

from models.trade_setup import TradeSetup

from engine.market_context_engine import MarketContextEngine
from engine.structure_engine import StructureEngine
from strategy.confluence_engine import ConfluenceEngine
from engine.swing_engine import SwingEngine
from engine.swing_fibonacci_engine import SwingFibonacciEngine
from engine.liquidity_engine import LiquidityEngine
from models.market_context import MarketContext
from models.indicator_result import IndicatorResult
from models.enums import Structure
from models.enums import Direction

class SetupBuilder:
    """
    Builds a fully validated TradeSetup by integrating
    all frozen Project FALCON engines.
    """

    def __init__(self):

        self.market_context_engine = MarketContextEngine()
        self.swing_engine = SwingEngine()
        self.swing_fibonacci_engine = SwingFibonacciEngine()
        self.structure_engine = StructureEngine()
        self.confluence_engine = ConfluenceEngine()
        self.liquidity_engine = LiquidityEngine()

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
        atr_ma: float,
        close: float,
        
    ) -> TradeSetup:

        setup = TradeSetup()

        # -------------------------------------------------
        # Indicators
        # -------------------------------------------------

        setup.ema_fast = ema_fast
        setup.ema_slow = ema_slow
        setup.current_price = close
        setup.rsi = rsi
        setup.adx = adx
        setup.atr = atr

        setup.ema_alignment = ema_fast > ema_slow
        if ema_fast > ema_slow:
            setup.direction = Direction.LONG
        elif ema_fast < ema_slow:
            setup.direction = Direction.SHORT
        else:
            setup.direction = Direction.NONE
        setup.high_volatility = atr > atr_ma

        # -------------------------------------------------
        # Market Context
        # -------------------------------------------------
        
        
        context = MarketContext()
        indicators = IndicatorResult(

        
            adx=adx,

            ema_fast=ema_fast,

            ema_slow=ema_slow,
            ema_alignment=ema_fast > ema_slow,

            rsi=rsi,

            atr=atr,

            atr_ma=atr_ma,
            atr_expanding=atr > atr_ma,
            valid=True

        )
        context = self.market_context_engine.analyze(
            context=context,
            indicators=indicators,
        )

        setup.trend = context.trend.trend
        setup.bias = context.trend.bias
        setup.strength = context.trend.strength


        # -------------------------------------------------
        # Trading Direction
        # -------------------------------------------------

        if ema_fast > ema_slow:
            setup.direction = Direction.LONG

        elif ema_fast < ema_slow:
            setup.direction = Direction.SHORT

        else:
            setup.direction = Direction.NONE
        

        # -------------------------------------------------
        # Swing Engine
        # -------------------------------------------------

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
        # Structure Engine
        # -------------------------------------------------

        structure = self.structure_engine.run(
            swings
        )

        self._validate_structure(
            structure
        )

        setup.structure = Structure.RANGE

        

        


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
                

            elif "BEARISH" in signal:

                setup.structure = Structure.BEARISH
                

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        liquidity_result = self.liquidity_engine.analyze(

            swings=swings,

            atr=atr,

        )

        if liquidity_result.buy_side_liquidity:
            liquidity = "BUY_SIDE"
        elif liquidity_result.sell_side_liquidity:
            liquidity = "SELL_SIDE"
        else:
             liquidity = "NONE"

        setup.liquidity = liquidity != "NONE"

        print("\n========== SWING ASSIGNMENT ==========")
        print(swings.tail(5))
        print("======================================\n")
        

        # -------------------------------------------------
        # Assign Latest Swing Levels
        # -------------------------------------------------

        highs = swings[
            swings["Type"] == "HIGH"
        ]

        lows = swings[
            swings["Type"] == "LOW"
        ]

        if not highs.empty:
            setup.swing_high = float(
                highs.iloc[-1]["Price"]
            )

        if not lows.empty:
            setup.swing_low = float(
                lows.iloc[-1]["Price"]
            )

        print("\n========== ASSIGNED SWINGS ==========")
        print("Swing High :", setup.swing_high)
        print("Swing Low  :", setup.swing_low)
        print("=====================================\n")
        # -------------------------------------------------
        # Confluence
        # -------------------------------------------------
        confluence = self.confluence_engine.evaluate(setup)

        setup.reasons.extend(confluence.reasons)
        
        
        
        # -------------------------------------------------
        # Final Validation
        # -------------------------------------------------

        setup.valid = (

            setup.structure != Structure.UNKNOWN
            and setup.fibonacci
            and setup.golden_zone
            and setup.direction !=Direction.NONE
        )
        return setup