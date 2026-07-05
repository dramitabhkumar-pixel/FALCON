from engine.trade_manager import TradeManager

from core.order import Order
from enums import OrderSide, OrderStatus


tm = TradeManager()

order = Order(
    order_id=1,
    symbol="BANKNIFTY",
    side=OrderSide.BUY,
    quantity=25,
    entry_price=50000,
    stop_loss=49900,
    target=50200,
)

order.status = OrderStatus.FILLED
order.filled_price = 50000

print("\n==============================")
print("FALCON TRADE MANAGER TEST")
print("==============================")

print("Stop Loss :", tm.check_stop_loss(order, 49950))
print("Target    :", tm.check_target(order, 50150))

tm.move_to_breakeven(order)
print("Breakeven SL :", order.stop_loss)

tm.trail_stop_loss(order, 50050)
print("Trailing SL  :", order.stop_loss)

print("PnL :", tm.calculate_pnl(order, 50120))

tm.process(order, 50220)

print("Status :", order.status)
print("Exit   :", order.exit_price)
print("PnL    :", order.pnl)
print("Remark :", order.remarks)