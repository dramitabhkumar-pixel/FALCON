from models.trade_decision import TradeDecision

from strategy.trade_manager import TradeManager


trade = TradeDecision(

    valid=True,

    signal="BUY",

    entry_price=100,

    stop_loss=95,

    target_price=115,

)

manager = TradeManager()

print("\nInitial")

print(manager.summary())

manager.load_trade(trade)

print("\nLoaded")

print(manager.summary())

manager.open_trade()

manager.update_price(104)

print("\nPrice = 104")

print(manager.summary())

manager.move_to_breakeven()

print("\nBreakeven")

print(manager.summary())

manager.trail_stop(103)

print("\nTrailing")

print(manager.summary())

manager.update_price(110)

print("\nPrice = 110")

print(manager.summary())

manager.partial_exit()

print("\nPartial Exit")

print(manager.summary())

manager.target_hit()

print("\nTarget Hit")

print(manager.summary())

manager.close_trade()

print("\nClosed")

print(manager.summary())