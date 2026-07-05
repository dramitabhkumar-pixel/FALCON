"""
Simulated order execution for backtests.
"""

from __future__ import annotations

from enums import OrderSide, OrderStatus

from engine.execution_engine import ExecutionEngine

from backtest.trade_history import TradeHistory


class BacktestTradeEngine:
    """Paper execution wrapper with intrabar stop/target checks."""

    def __init__(self, symbol: str = "BANKNIFTY"):
        self.symbol = symbol
        self.execution = ExecutionEngine()
        self.history = TradeHistory()
        self.open_orders: list = []

    @property
    def open_position_count(self) -> int:
        return len(self.open_orders)

    def try_entry(
        self,
        side: OrderSide,
        entry: float,
        stop_loss: float,
        target: float,
    ):
        order = self.execution.execute_trade(
            symbol=self.symbol,
            side=side,
            entry=entry,
            stop_loss=stop_loss,
            target=target,
            open_positions=self.open_position_count,
        )

        if order is not None:
            self.open_orders.append(order)

        return order

    def on_bar(self, bar, entry_time=None) -> list:
        """Check open orders against the current bar high/low."""

        closed = []

        for order in list(self.open_orders):
            if order.status != OrderStatus.FILLED:
                continue

            exit_price = self._resolve_exit(order, bar)
            if exit_price is None:
                continue

            self.execution.orderbook.exit_order(order.order_id, exit_price)
            self.history.record(order, entry_time=entry_time, exit_time=bar.name)
            self.open_orders.remove(order)
            closed.append(order)

        return closed

    def _resolve_exit(self, order, bar) -> float | None:
        high = float(bar["High"])
        low = float(bar["Low"])

        if order.side.name == "BUY":
            stop_hit = low <= order.stop_loss
            target_hit = high >= order.target

            if stop_hit and target_hit:
                return order.stop_loss

            if stop_hit:
                return order.stop_loss

            if target_hit:
                return order.target

            return None

        stop_hit = high >= order.stop_loss
        target_hit = low <= order.target

        if stop_hit and target_hit:
            return order.stop_loss

        if stop_hit:
            return order.stop_loss

        if target_hit:
            return order.target

        return None

    def reset(self):
        self.execution = ExecutionEngine()
        self.history = TradeHistory()
        self.open_orders = []
