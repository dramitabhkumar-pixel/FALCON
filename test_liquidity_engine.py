from engine.liquidity_engine import LiquidityEngine

engine = LiquidityEngine()

swings = [

    {"type":"LOW","price":100},

    {"type":"HIGH","price":120},

    {"type":"LOW","price":110},

    {"type":"HIGH","price":120.1},

    {"type":"LOW","price":109.9},

]

result = engine.analyze(swings)

print()

print("Equal Highs :", result.equal_highs)

print("Equal Lows :", result.equal_lows)

print("Buy Side Liquidity :", result.buy_side_liquidity)

print("Sell Side Liquidity :", result.sell_side_liquidity)