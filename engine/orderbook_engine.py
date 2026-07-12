from datetime import datetime

from core.order import Order
from models.enums import (
     Direction,
     TradeStatus,
)


class OrderBookEngine:

    def __init__(self):

        self.open_orders = []

        self.closed_orders = []

        self.next_order_id = 1

    def create_order(
        self,
        symbol,
        side,
        quantity,
        entry,
        sl,
        target
    ):

        order = Order(

            order_id=self.next_order_id,

            symbol=symbol,

            side=side,

            quantity=quantity,

            entry_price=entry,

            STOPLOSS=sl,

            target=target

        )

        self.open_orders.append(order)

        self.next_order_id += 1

        return order

    def fill_order(self, order_id, fill_price):

        for order in self.open_orders:

            if order.order_id == order_id:

                order.status = TradeStatus.ACTIVE

                order.filled_price = fill_price

                return order

        return None

    def exit_order(self, order_id, exit_price):

        for order in self.open_orders:

            if order.order_id == order_id:

                order.exit_price = exit_price

                order.closed_at = datetime.now()

                order.status = TradeStatus.CLOSED

                if order.side == Direction.LONG:

                    order.pnl = (
                        exit_price -
                        order.filled_price
                    ) * order.quantity

                else:

                    order.pnl = (
                        order.filled_price -
                        exit_price
                    ) * order.quantity

                self.closed_orders.append(order)

                self.open_orders.remove(order)

                return order

        return None

    def get_open_orders(self):

        return self.open_orders

    def get_closed_orders(self):

        return self.closed_orders

    def summary(self):

        total = sum(x.pnl for x in self.closed_orders)

        print("=" * 50)

        print("OPEN :", len(self.open_orders))

        print("CLOSED :", len(self.closed_orders))

        print("TOTAL PNL :", round(total, 2))

        print("=" * 50)