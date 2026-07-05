import csv
import os


class JournalEngine:

    def __init__(self, file_path="journal/trades.csv"):

        self.file_path = file_path

        header = [
            "TradeID",
            "Symbol",
            "Side",
            "Entry",
            "Exit",
            "Quantity",
            "StopLoss",
            "Target",
            "PnL",
            "Status"
        ]

        write_header = (
            not os.path.exists(self.file_path)
            or os.path.getsize(self.file_path) == 0
        )

        if write_header:

            with open(self.file_path, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow(header)

    def record_trade(self, order):

        with open(self.file_path, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                order.order_id,
                order.symbol,
                order.side.value,
                order.entry_price,
                order.exit_price,
                order.quantity,
                order.stop_loss,
                order.target,
                order.pnl,
                order.status.value
            ])

    def load_trades(self):

        with open(self.file_path, "r", newline="") as file:

            reader = csv.DictReader(file)

            return list(reader)

    def total_pnl(self):

        trades = self.load_trades()

        total = 0.0

        for trade in trades:

            total += float(trade["PnL"])

        return total