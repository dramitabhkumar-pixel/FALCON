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
from engine.confluence_engine import ConfluenceEngine
from engine.swing_engine import SwingEngine
from engine.swing_fibonacci_engine import SwingFibonacciEngine


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
        liquidity: str,
    ) -> TradeSetup:

        setup = TradeSetup()

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

        context = self.market_context_engine.analyze(

            adx=adx,

            ema_fast=ema_fast,

            ema_slow=ema_slow,

            rsi=rsi,

            atr=atr,

            avg_atr=avg_atr,

        )

        setup.market_context = context.trend
        setup.trend = context.trend

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

        setup.structure = "NEUTRAL"

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

                setup.structure = "BULLISH"
                setup.bos = True

            elif "BEARISH" in signal:

                setup.structure = "BEARISH"
                setup.bos = True

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        setup.liquidity = str(
            liquidity
        ).upper() in (

            "BUY_SIDE",

            "SELL_SIDE",

        )

        # -------------------------------------------------
        # Swing Direction
        # -------------------------------------------------

        if setup.structure == "BULLISH":

            swing_direction = "HH_HL"

        elif setup.structure == "BEARISH":

            swing_direction = "LH_LL"

        else:

            swing_direction = "UNKNOWN"

        # -------------------------------------------------
        # Confluence
        # -------------------------------------------------

        confluence = self.confluence_engine.evaluate(

            market_structure=setup.structure,

            market_context=setup.market_context,

            swing_direction=swing_direction,

            liquidity=liquidity,

            ema_bullish=setup.ema_alignment,

            adx=adx,

            rsi=rsi,

            atr_high=atr >= avg_atr,

            fib_golden_zone=setup.golden_zone,

        )

        setup.confluence = confluence.score

        setup.reasons.extend(
            confluence.reasons
        )

        # -------------------------------------------------
        # Trading Direction
        # -------------------------------------------------

        if confluence.signal in (

            "BUY",

            "STRONG BUY",

        ):

            setup.direction = "BUY"

        elif confluence.signal in (

            "SELL",

            "STRONG SELL",

        ):

            setup.direction = "SELL"

        else:

            setup.direction = "NONE"

        # -------------------------------------------------
        # Entry / SL / Target
        # -------------------------------------------------

        if setup.direction == "BUY":

            setup.entry_price = close

            setup.stop_loss = fibonacci.fib_618

            risk = (

                setup.entry_price

                - setup.stop_loss

            )

            if risk > 0:

                setup.target_price = (

                    setup.entry_price

                    + risk * 2.5

                )

        elif setup.direction == "SELL":

            setup.entry_price = close

            setup.stop_loss = fibonacci.fib_382

            risk = (

                setup.stop_loss

                - setup.entry_price

            )

            if risk > 0:

                setup.target_price = (

                    setup.entry_price

                    - risk * 2.5

                )

        # -------------------------------------------------
        # Risk Reward
        # -------------------------------------------------

        if (

            setup.entry_price > 0

            and setup.stop_loss > 0

            and setup.target_price > 0

        ):

            if setup.direction == "BUY":

                risk = (

                    setup.entry_price

                    - setup.stop_loss

                )

                reward = (

                    setup.target_price

                    - setup.entry_price

                )

            elif setup.direction == "SELL":

                risk = (

                    setup.stop_loss

                    - setup.entry_price

                )

                reward = (

                    setup.entry_price

                    - setup.target_price

                )

            else:

                risk = 0.0
                reward = 0.0

            if risk > 0:

                setup.risk_reward = round(

                    reward / risk,

                    2,

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
        print("Entry Price    :", setup.entry_price)
        print("Stop Loss      :", setup.stop_loss)
        print("Target Price   :", setup.target_price)
        print("Risk Reward    :", setup.risk_reward)
        print("=================================\n")

        
        setup.valid = (

            setup.direction != "NONE"

            and setup.structure != "NEUTRAL"

            and setup.fibonacci

            and fibonacci.pullback_valid

            and setup.golden_zone

            and setup.entry_price > 0

            and setup.stop_loss > 0

            and setup.target_price > 0

            and setup.risk_reward >= 2.5

        )

        return setup