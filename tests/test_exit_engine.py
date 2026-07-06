from models.trade_decision import TradeDecision

from strategy.exit_engine import ExitEngine


trade = TradeDecision(

    valid=True,

    signal="BUY",

    entry_price=100,

    stop_loss=95,

    target_price=115,

)

engine = ExitEngine()

prices = [

    101,

    104,

    110,

    116,

]

for p in prices:

    exit_trade, reason = engine.should_exit(

        trade,

        p

    )

    print(

        f"{p:5} -> Exit={exit_trade} Reason={reason}"

    )