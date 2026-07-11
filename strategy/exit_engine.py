"""
==========================================================
PROJECT FALCON
Exit Engine
Version : 4.0
==========================================================

Evaluates whether an ACTIVE trade should be exited.

Responsibilities
----------------
• Stop Loss
• Target
• Opposite Signal
• Time Exit
• Market Close

This engine NEVER modifies a TradeDecision.

Instead, it returns an ExitDecision which is
applied by the TradeManager.

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.base_engine import BaseEngine
from core.candles import Candle

from models.trade_decision import TradeDecision
from models.exit_decision import ExitDecision

from models.enums import (
    Direction,
    ExitReason,
    TradeStatus,
)

from strategy.strategy_config import (
    FORCED_EXIT_TIME,
)


class ExitEngine(BaseEngine):
    """
    Evaluates whether an active trade should exit.

    This engine is completely stateless.

    Input:
        TradeDecision
        Candle

    Output:
        ExitDecision
    """

    def __init__(self):

        super().__init__()

    # =====================================================
    # Public API
    # =====================================================

    def evaluate_exit(
        self,
        trade: TradeDecision,
        candle: Candle,
        opposite_signal: bool = False,
    ) -> ExitDecision:
        """
        Evaluate all exit conditions.

        Parameters
        ----------
        trade
            Current active trade.

        candle
            Current market candle.

        opposite_signal
            True if strategy generated
            an opposite signal.

        Returns
        -------
        ExitDecision
        """

        if trade.status != TradeStatus.ACTIVE:

            return ExitDecision()

        decision = self._check_stop_loss(
            trade,
            candle,
        )

        if decision.should_exit:
            return decision

        decision = self._check_target(
            trade,
            candle,
        )

        if decision.should_exit:
            return decision

        decision = self._check_opposite_signal(
            trade,
            candle,
            opposite_signal,
        )

        if decision.should_exit:
            return decision

        decision = self._check_time_exit(
            trade,
            candle,
        )

        if decision.should_exit:
            return decision

        return self._check_market_close(
            trade,
            candle,
        )

    # =====================================================
    # Stop Loss
    # =====================================================

    def _check_stop_loss(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> ExitDecision:
        """
        Evaluate stop-loss exit.
        """

        if trade.direction == Direction.LONG:

            if candle.low <= trade.stop_loss:

                return self._build_exit_decision(
                    exit_reason=ExitReason.STOPLOSS,
                    exit_price=trade.stop_loss,
                    exit_time=candle.timestamp,
                    message="Long stop-loss hit.",
                )

        elif trade.direction == Direction.SHORT:

            if candle.high >= trade.stop_loss:

                return self._build_exit_decision(
                    exit_reason=ExitReason.STOPLOSS,
                    exit_price=trade.stop_loss,
                    exit_time=candle.timestamp,
                    message="Short stop-loss hit.",
                )

        return ExitDecision()

    # =====================================================
    # Target
    # =====================================================

    def _check_target(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> ExitDecision:
        """
        Evaluate target exit.
        """

        if trade.direction == Direction.LONG:

            if candle.high >= trade.target:

                return self._build_exit_decision(
                    exit_reason=ExitReason.TARGET,
                    exit_price=trade.target,
                    exit_time=candle.timestamp,
                    message="Long target achieved.",
                )

        elif trade.direction == Direction.SHORT:

            if candle.low <= trade.target:

                return self._build_exit_decision(
                    exit_reason=ExitReason.TARGET,
                    exit_price=trade.target,
                    exit_time=candle.timestamp,
                    message="Short target achieved.",
                )

        return ExitDecision()