from engine.orderbook_engine import OrderBookEngine
from enums import OrderSide


engine = OrderBookEngine()


order = engine.create_order(

    symbol="BANKNIFTY",

    side=OrderSide.BUY,

    quantity=25,

    entry=51000,

    sl=50850,

    target=51300

)


engine.fill_order(order.order_id, 51005)

engine.exit_order(order.order_id, 51200)

engine.summary()


print(engine.get_closed_orders()[0])