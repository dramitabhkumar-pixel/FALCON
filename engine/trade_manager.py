from enums import OrderStatus


class TradeManager:

    def __init__(self):
        pass

    def check_stop_loss(self, order, current_price):

        if order.status != OrderStatus.FILLED:
            return False

        if order.side.name == "BUY":

            return current_price <= order.stop_loss

        else:

            return current_price >= order.stop_loss

    def check_target(self, order, current_price):

        if order.status != OrderStatus.FILLED:
            return False

        if order.side.name == "BUY":

            return current_price >= order.target

        else:

            return current_price <= order.target

    def move_to_breakeven(self, order):

        if order.filled_price is not None:
            order.stop_loss = order.filled_price

    def trail_stop_loss(self, order, new_sl):

        if order.side.name == "BUY":

            if new_sl > order.stop_loss:
                order.stop_loss = new_sl

        else:

            if new_sl < order.stop_loss:
                order.stop_loss = new_sl