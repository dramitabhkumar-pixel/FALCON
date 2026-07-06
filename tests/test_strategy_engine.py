from models.trade_setup import TradeSetup

from strategy.strategy_engine import StrategyEngine


setup = TradeSetup(

    trend="UP",

    structure="BULLISH",

    ema_alignment=True,

    bos=True,

    golden_zone=True,

    liquidity=True,

    rsi=65,

    adx=30,

    volume=1500,

    market_context="TRENDING",

    confluence=90,

    entry_price=100,

    stop_loss=95,

    target_price=115,

)

engine = StrategyEngine()

decision = engine.process(setup)

print()

if decision is None:

    print("Trade Rejected")

else:

    print("Trade Accepted")

    print()

    print(decision)