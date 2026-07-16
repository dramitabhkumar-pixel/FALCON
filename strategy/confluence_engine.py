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
from models.enums import Trend, Structure, Direction
from strategy.strategy_config import CONFIG


class ConfluenceEngine:
    """Validates the confluence of a TradeSetup."""

    @staticmethod
    def _validate(setup: TradeSetup) -> None:
        if setup is None:
            raise ValueError("TradeSetup cannot be None.")
        if not setup.valid:
            raise ValueError("TradeSetup is invalid.")

    @staticmethod
    def _trend_alignment(setup: TradeSetup) -> bool:
        if setup.direction == Direction.LONG:
            return setup.trend == Trend.CONFIRMED_UPTREND
        if setup.direction == Direction.SHORT:
            return setup.trend == Trend.CONFIRMED_DOWNTREND
        return False

    @staticmethod
    def _structure_alignment(setup: TradeSetup) -> bool:
        if setup.direction == Direction.LONG:
            return setup.structure == Structure.BULLISH
        if setup.direction == Direction.SHORT:
            return setup.structure == Structure.BEARISH
        return False

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
            (result.trend_alignment, "Trend aligned."),
            (result.structure_alignment, "Structure aligned."),
            (result.ema_alignment, "EMA alignment confirmed."),
            (result.adx_confirmation, "ADX confirmed."),
            (result.rsi_confirmation, "RSI confirmed."),
            (result.liquidity_confirmation, "Liquidity confirmed."),
            (result.golden_zone_confirmation, "Golden Zone confirmed."),
            (result.bos_confirmation, "Break of Structure confirmed."),
            (result.choch_confirmation, "Change of Character confirmed."),
        ]
        for passed, msg in checks:
            if passed:
                result.reasons.append(msg)

    def evaluate(self, setup: TradeSetup) -> ConfluenceResult:
        self._validate(setup)

        result = ConfluenceResult()
        result.direction = setup.direction

        result.trend_alignment = self._trend_alignment(setup)
        result.structure_alignment = self._structure_alignment(setup)
        result.ema_alignment = setup.ema_alignment
        result.adx_confirmation = self._adx_confirmation(setup)
        result.rsi_confirmation = self._rsi_confirmation(setup)
        result.liquidity_confirmation = setup.liquidity
        result.golden_zone_confirmation = setup.golden_zone
        result.bos_confirmation = setup.bos
        result.choch_confirmation = setup.choch

        self._collect_reasons(result)

        result.valid = True
        return result

    def __call__(self, setup: TradeSetup) -> ConfluenceResult:
        return self.evaluate(setup)
