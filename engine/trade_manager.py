"""
=========================================================
Project FALCON
Trade Manager
Version : 1.0
=========================================================
"""

from core.base_engine import BaseEngine
from enums import OrderStatus


class TradeManager(BaseEngine):
    """
    Trade Management Engine

    Handles:
    - Stop Loss
    - Target
    - Break Even
    - Trailing Stop Loss
    - PnL Calculation
    - Order Exit
    """

    def __init__(self):

        super().__init__()

        self.log("Trade Manager Initialized")

    # -----------------------------------------------------

    def check_stop_loss(
        self,
        order,
        current_price: float,
    ) -> bool:

        if order.status != OrderStatus.FILLED:
            return False

        if order.side.name == "BUY":
            return current_price <= order.stop_loss

        return current_price >= order.stop_loss

    # -----------------------------------------------------

    def check_target(
        self,
        order,
        current_price: float,
    ) -> bool:

        if order.status != OrderStatus.FILLED:
            return False

        if order.side.name == "BUY":
            return current_price >= order.target

        return current_price <= order.target

    # -----------------------------------------------------

    def move_to_breakeven(
        self,
        order,
    ):

        if order.status != OrderStatus.FILLED:
            return

        if order.filled_price is None:
            return

        order.stop_loss = order.filled_price

        self.log(
            f"Moved SL to Breakeven : {order.symbol}"
        )

    # -----------------------------------------------------

    def trail_stop_loss(
        self,
        order,
        new_stop_loss: float,
    ):

        if order.status != OrderStatus.FILLED:
            return

        if order.side.name == "BUY":

            if new_stop_loss > order.stop_loss:

                order.stop_loss = new_stop_loss

                self.log(
                    f"Trailing SL Updated : {order.symbol}"
                )

        else:

            if new_stop_loss < order.stop_loss:

                order.stop_loss = new_stop_loss

                self.log(
                    f"Trailing SL Updated : {order.symbol}"
                )

    # -----------------------------------------------------

    def calculate_pnl(
        self,
        order,
        exit_price: float,
    ) -> float:

        if order.filled_price is None:
            return 0.0

        if order.side.name == "BUY":

            pnl = (
                exit_price
                - order.filled_price
            ) * order.quantity

        else:

            pnl = (
                order.filled_price
                - exit_price
            ) * order.quantity

        return round(pnl, 2)

    # -----------------------------------------------------

    def close_order(
        self,
        order,
        exit_price: float,
        remarks: str,
    ):

        if order.status != OrderStatus.FILLED:
            return

        order.exit_price = exit_price

        order.pnl = self.calculate_pnl(
            order,
            exit_price,
        )

        order.status = OrderStatus.EXITED

        order.remarks = remarks

        self.log(

            f"Order Closed | "
            f"{order.symbol} | "
            f"Exit={exit_price} | "
            f"PnL={order.pnl}"

        )

    # -----------------------------------------------------

    def process(
        self,
        order,
        current_price: float,
    ):

        if self.check_stop_loss(
            order,
            current_price,
        ):

            self.close_order(

                order,

                current_price,

                "Stop Loss Hit",

            )

            return

        if self.check_target(
            order,
            current_price,
        ):

            self.close_order(

                order,

                current_price,

                "Target Hit",

            )

            return

    # -----------------------------------------------------

    def reset(self):

        self.log("Trade Manager Reset")