from engine.risk_manager import RiskManager
from engine.orderbook_engine import OrderBookEngine
from engine.trade_manager import TradeManager


class ExecutionEngine:

    def __init__(self):

        self.risk = RiskManager()

        self.orderbook = OrderBookEngine()

        self.trade_manager = TradeManager()

    def execute_trade(
        self,
        symbol,
        side,
        entry,
        STOPLOSS,
        target,
        open_positions=0
    ):

        # Risk Check
        if not self.risk.can_trade(open_positions):
            print("[Execution] Trade rejected by Risk Manager")
            return None

        # Strategy Validation
        if not self.risk.validate_trade(
            entry,
            STOPLOSS,
            target
        ):
            print("[Execution] Invalid Trade")
            return None

        # Position Size
        qty = self.risk.calculate_position_size(
            entry,
            STOPLOSS
        )

        # Create Order
        order = self.orderbook.create_order(
            symbol=symbol,
            side=side,
            quantity=qty,
            entry=entry,
            sl=STOPLOSS,
            target=target
        )

        # Paper Fill
        self.orderbook.fill_order(
            order.order_id,
            entry
        )

        self.risk.increment_trade()

        print(f"[Execution] Order Executed | Qty = {qty}")

        return order

    def monitor_trade(
        self,
        order,
        current_price
    ):

        if self.trade_manager.check_STOPLOSS(
            order,
            current_price
        ):

            self.orderbook.exit_order(
                order.order_id,
                current_price
            )

            print("[Execution] Stop Loss Hit")

            return

        if self.trade_manager.check_target(
            order,
            current_price
        ):

            self.orderbook.exit_order(
                order.order_id,
                current_price
            )

            print("[Execution] Target Hit")

            return