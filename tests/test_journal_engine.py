from engine.execution_engine import ExecutionEngine
from engine.journal_engine import JournalEngine
from enums import OrderSide


execution = ExecutionEngine()

journal = JournalEngine()


order = execution.execute_trade(

    symbol="BANKNIFTY",

    side=OrderSide.BUY,

    entry=51000,

    stop_loss=50950,

    target=51200

)


execution.monitor_trade(

    order,

    51220

)


journal.record_trade(order)


print(journal.load_trades())

print("Total PnL :", journal.total_pnl())