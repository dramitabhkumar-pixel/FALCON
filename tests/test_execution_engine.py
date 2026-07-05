from engine.execution_engine import ExecutionEngine
from enums import OrderSide


engine = ExecutionEngine()


order = engine.execute_trade(

    symbol="BANKNIFTY",

    side=OrderSide.BUY,

    entry=51000,

    stop_loss=50950,

    target=51200,

    open_positions=0

)


engine.monitor_trade(

    order,

    51220

)


engine.orderbook.summary()