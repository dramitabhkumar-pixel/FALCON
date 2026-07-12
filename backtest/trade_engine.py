"""
Simulated order execution for backtests.
"""

from __future__ import annotations

from models.enums import (
    Direction,
    TradeStatus,
)
from engine.execution_engine import ExecutionEngine

from backtest.trade_history import TradeHistory


class BacktestTradeEngine:
    """
    Paper execution wrapper with intrabar stop/target checks.
    """

    def __init__(self, symbol: str = "BANKNIFTY"):

        self.symbol = symbol

        self.execution = ExecutionEngine()

        self.history = TradeHistory()

        self.open_orders: list = []

    @property
    def open_position_count(self) -> int:

        return len(self.open_orders)

    # =====================================================
    # Entry
    # =====================================================

    def try_entry(
        self,
        side: Direction,
        entry: float,
        STOPLOSS: float,
        target: float,
        entry_time,
    ):

        order = self.execution.execute_trade(
            symbol=self.symbol,
            side=side,
            entry=entry,
            STOPLOSS=STOPLOSS,
            target=target,
            open_positions=self.open_position_count,
        )

        if order is not None:

            # Preserve original entry timestamp
            order.entry_time = entry_time

            self.open_orders.append(order)

        return order

    # =====================================================
    # Candle Processing
    # =====================================================

    def on_bar(self, bar) -> list:
        """
        Check all open orders against the latest candle.
        """

        closed_orders = []

        for order in list(self.open_orders):

            if order.status != TradeStatus.ACTIVE:
                continue

            exit_price = self._resolve_exit(order, bar)

            if exit_price is None:
                continue

            self.execution.orderbook.exit_order(
                order.order_id,
                exit_price,
            )

            self.history.record(
                order,
                entry_time=order.entry_time,
                exit_time=bar.name,
            )

            self.open_orders.remove(order)

            closed_orders.append(order)

        return closed_orders

    # =====================================================
    # Exit Resolution
    # =====================================================

    def _resolve_exit(
        self,
        order,
        bar,
    ) -> float | None:

        high = float(bar["High"])
        low = float(bar["Low"])

        # -------------------------------
        # BUY Position
        # -------------------------------

        if order.side == Direction.LONG:

            stop_hit = low <= order.STOPLOSS
            target_hit = high >= order.target

            # Conservative assumption:
            # Stop Loss is hit first if both occur
            if stop_hit and target_hit:
                return order.STOPLOSS

            if stop_hit:
                return order.STOPLOSS

            if target_hit:
                return order.target

            return None

        # -------------------------------
        # SELL Position
        # -------------------------------

        stop_hit = high >= order.STOPLOSS
        target_hit = low <= order.target

        if stop_hit and target_hit:
            return order.STOPLOSS

        if stop_hit:
            return order.STOPLOSS

        if target_hit:
            return order.target

        return None

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.execution = ExecutionEngine()

        self.history = TradeHistory()

        self.open_orders = []