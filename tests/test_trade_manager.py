from engine.orderbook_engine import OrderBookEngine
from engine.trade_manager import TradeManager
from enums import OrderSide


ob = OrderBookEngine()

tm = TradeManager()


order = ob.create_order(

    symbol="BANKNIFTY",

    side=OrderSide.BUY,

    quantity=25,

    entry=51000,

    sl=50900,

    target=51200

)

ob.fill_order(order.order_id, 51000)


print(

    "SL Hit :",

    tm.check_stop_loss(

        order,

        50890

    )

)


print(

    "Target Hit :",

    tm.check_target(

        order,

        51220

    )

)


tm.move_to_breakeven(order)

print("Breakeven SL :", order.stop_loss)


tm.trail_stop_loss(order, 51050)

print("Trailing SL :", order.stop_loss)