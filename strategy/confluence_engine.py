"""
=========================================================
PROJECT FALCON
Confluence Engine
Version : 3.1 (Frozen)
=========================================================

Validates a TradeSetup and produces a ConfluenceResult.
"""

from __future__ import annotations

from models.trade_setup import TradeSetup
from models.confluence_result import ConfluenceResult

from strategy.strategy_config import CONFIG
from models.enums import (
    Direction,
    Bias,
)


class ConfluenceEngine:
    """Validates the confluence of a TradeSetup."""

    @staticmethod
    def _validate(setup: TradeSetup) -> None:
        if setup is None:
            raise ValueError("TradeSetup cannot be None.")
        


    

    @staticmethod
    def _adx_confirmation(setup: TradeSetup) -> bool:
        return setup.adx >= CONFIG.ADX_MINIMUM

    @staticmethod
    def _rsi_confirmation(setup: TradeSetup) -> bool:
        if setup.direction == Direction.LONG:
            return setup.rsi >= CONFIG.RSI_LONG
        if setup.direction == Direction.SHORT:
            return setup.rsi <= CONFIG.RSI_SHORT
        return False

    @staticmethod
    def _collect_reasons(result: ConfluenceResult) -> None:
        checks = [
            
            
            (result.adx_confirmation, "ADX confirmed."),
            (result.rsi_confirmation, "RSI confirmed."),
            (result.liquidity_confirmation, "Liquidity confirmed."),
            (result.golden_zone_confirmation, "Golden Zone confirmed."),
            (result.atr_confirmation, "ATR expanding."),
            (result.daily_bias_confirmation, "Daily Bias confirmed."),
            
            
        ]
        for passed, msg in checks:
            if passed:
                result.reasons.append(msg)

    def evaluate(self, setup: TradeSetup) -> ConfluenceResult:
        self._validate(setup)

        result = ConfluenceResult()
        result.direction = setup.direction

        
        
        result.atr_confirmation = setup.high_volatility
        result.adx_confirmation = self._adx_confirmation(setup)
        result.rsi_confirmation = self._rsi_confirmation(setup)
        result.liquidity_confirmation = setup.liquidity
        result.golden_zone_confirmation = setup.golden_zone
        result.daily_bias_confirmation = (
            (setup.direction == Direction.LONG and setup.bias == Bias.BULLISH)
            or
            (setup.direction == Direction.SHORT and setup.bias == Bias.BEARISH)
        )
        self._collect_reasons(result)
        

        result.valid = True

        print("\n========== CONFLUENCE DEBUG ==========")

        print("Direction       :", setup.direction)
        print("Bias            :", setup.bias)

        print("ADX             :", setup.adx)
        print("ADX Pass        :", result.adx_confirmation)

        print("RSI             :", setup.rsi)
        print("RSI Pass        :", result.rsi_confirmation)

        print("ATR             :", setup.atr)
        print("High Volatility :", setup.high_volatility)
        print("ATR Pass        :", result.atr_confirmation)

        print("Golden Zone     :", setup.golden_zone)
        print("Golden Pass     :", result.golden_zone_confirmation)

        print("Liquidity       :", setup.liquidity)
        print("Liquidity Pass  :", result.liquidity_confirmation)

        print("Daily Bias Pass :", result.daily_bias_confirmation)

        print("Reasons         :", result.reasons)

        print("======================================\n")

        return result

        
        
        

       

    def __call__(self, setup: TradeSetup) -> ConfluenceResult:
        return self.evaluate(setup)
