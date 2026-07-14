"""
=========================================================
PROJECT FALCON
Journal Writer
Version : 1.0
=========================================================

Writes completed trades to CSV.

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
import csv

from models.trade_record import TradeRecord


class JournalWriter:
    """
    Writes completed trades to journal files.
    """

    def __init__(self, folder: str = "journal") -> None:

        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

        self.trade_file = self.folder / "trades.csv"

        if not self.trade_file.exists():

            with self.trade_file.open(
                "w",
                newline="",
                encoding="utf-8",
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "trade_id",
                    "symbol",
                    "direction",
                    "entry_time",
                    "exit_time",
                    "entry_price",
                    "exit_price",
                    "stop_loss",
                    "target",
                    "quantity",
                    "pnl",
                    "exit_reason",
                    "confidence",
                    "winner",
                ])

    # -------------------------------------------------

    def write_trade(
        self,
        trade: TradeRecord,
    ) -> None:
        """
        Append one completed trade.
        """
        print(">>> WRITE_TRADE CALLED <<<")
        print("Trade ID:", trade.trade_id)
        print("CSV File:", self.trade_file.resolve())

        with self.trade_file.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                trade.trade_id,
                trade.symbol,
                trade.direction.name,
                trade.entry_time,
                trade.exit_time,
                trade.entry_price,
                trade.exit_price,
                trade.stop_loss,
                trade.target,
                trade.quantity,
                trade.pnl,
                trade.exit_reason.name,
                trade.confidence,
                trade.winner,
            ])
            print(">>> ROW WRITTEN <<<")