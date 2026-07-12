"""
=========================================================
PROJECT FALCON
Exit Engine
Version : 1.0
=========================================================

Manages the lifecycle of active trades.

Responsibilities
----------------
- Monitor active trades
- Update trade state
- Check Stop Loss
- Check Target
- Close completed trades

No entry logic belongs here.
"""

from core.base_engine import BaseEngine
from core.models import Candle

from models.trade_decision import TradeDecision
from models.enums import (
    Direction,
    TradeStatus,
    ExitReason,
)


class ExitEngine(BaseEngine):
    """
    Manages the lifecycle of an active trade.
    """

    def __init__(self):

        super().__init__()

    # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> TradeDecision:
        """
        Evaluate an active trade using the latest candle.
        """

        self._update_extremes(
            trade,
            candle,
        )

        self._update_trailing_stop(
            trade,
        )

        if self._check_stop_loss(
            trade,
            candle,
        ):

            self._close_trade(
                trade,
                candle,
                ExitReason.STOPLOSS,
            )

            return trade

        if self._check_target(
            trade,
            candle,
        ):

            self._close_trade(
                trade,
                candle,
                ExitReason.TARGET,
            )

            return trade

        return trade
        
    # =====================================================
    # Private Methods
    # =====================================================

    def _update_extremes(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> None:
        """
        Update highest and lowest prices seen
        since the trade was opened.
        """

        if trade.highest_price == 0:
            trade.highest_price = candle.high

        if trade.lowest_price == 0:
            trade.lowest_price = candle.low

        trade.highest_price = max(
            trade.highest_price,
            candle.high,
        )

        trade.lowest_price = min(
            trade.lowest_price,
            candle.low,
        )

    def _update_trailing_stop(
        self,
        trade: TradeDecision,
    ) -> None:
        """
        Placeholder for future trailing stop logic.

        V1.0:
            No trailing stop.
        """

        return
    def _check_stop_loss(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> bool:
        """
        Returns True if the stop loss has been hit.
        """

        if trade.direction == Direction.LONG:
            return candle.low <= trade.stop_loss

        if trade.direction == Direction.SHORT:
            return candle.high >= trade.stop_loss

        return False

    def _check_target(
        self,
        trade: TradeDecision,
        candle: Candle,
    ) -> bool:
        """
        Returns True if the target has been hit.
        """

        if trade.direction == Direction.LONG:
            return candle.high >= trade.target

        if trade.direction == Direction.SHORT:
            return candle.low <= trade.target

        return False
    def _close_trade(
        self,
        trade: TradeDecision,
        candle: Candle,
        reason: ExitReason,
    ) -> None:
        """
        Close the trade and update its final state.
        """

        trade.status = TradeStatus.CLOSED
        trade.exit_reason = reason
        trade.exit_time = candle.timestamp

        if reason == ExitReason.STOPLOSS:
            trade.exit_price = trade.stop_loss

        elif reason == ExitReason.TARGET:
            trade.exit_price = trade.target

        self._calculate_pnl(trade)

    def _calculate_pnl(
        self,
        trade: TradeDecision,
    ) -> None:
        """
        Calculate trade profit/loss.
        """

        if trade.direction == Direction.LONG:

            trade.pnl_points = (
                trade.exit_price - trade.entry_price
            )

        elif trade.direction == Direction.SHORT:

            trade.pnl_points = (
                trade.entry_price - trade.exit_price
            )

        else:

            trade.pnl_points = 0.0

        trade.pnl = (
            trade.pnl_points
            * trade.quantity
        )

        if trade.entry_price > 0:

            trade.pnl_percent = (
                trade.pnl_points
                / trade.entry_price
            ) * 100
    