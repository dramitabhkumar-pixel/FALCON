"""
Record closed trades during a backtest run.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime

import pandas as pd


@dataclass
class TradeRecord:
    order_id: int
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    quantity: int
    STOPLOSS: float
    target: float
    pnl: float
    status: str
    entry_time: str | None = None
    exit_time: str | None = None
    remarks: str = ""


class TradeHistory:
    """In-memory trade log for backtest performance reporting."""

    def __init__(self):
        self.trades: list[TradeRecord] = []

    def record(self, order, entry_time=None, exit_time=None) -> TradeRecord:
        record = TradeRecord(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side.name,
            entry_price=order.filled_price or order.entry_price,
            exit_price=order.exit_price or 0.0,
            quantity=order.quantity,
            STOPLOSS=order.STOPLOSS,
            target=order.target,
            pnl=order.pnl,
            status=order.status.value,
            entry_time=str(entry_time) if entry_time is not None else None,
            exit_time=str(exit_time) if exit_time is not None else None,
            remarks=getattr(order, "remarks", ""),
        )
        self.trades.append(record)
        return record

    def to_dataframe(self) -> pd.DataFrame:
        if not self.trades:
            return pd.DataFrame(
                columns=[
                    "order_id",
                    "symbol",
                    "side",
                    "entry_price",
                    "exit_price",
                    "quantity",
                    "STOPLOSS",
                    "target",
                    "pnl",
                    "status",
                    "entry_time",
                    "exit_time",
                    "remarks",
                ]
            )

        return pd.DataFrame([asdict(trade) for trade in self.trades])

    def total_pnl(self) -> float:
        return round(sum(trade.pnl for trade in self.trades), 2)
