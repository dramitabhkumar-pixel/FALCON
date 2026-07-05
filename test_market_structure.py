from engine.market_structure_engine import MarketStructureEngine

engine = MarketStructureEngine()

swings = [

    {"type": "LOW", "price": 100},
    {"type": "HIGH", "price": 120},

    {"type": "LOW", "price": 110},
    {"type": "HIGH", "price": 130},
]

result = engine.analyze(swings)

print()

print("Trend          :", result.trend)
print("High Structure :", result.last_high_type)
print("Low Structure  :", result.last_low_type)
print("Protected High :", result.protected_high)
print("Protected Low  :", result.protected_low)
print("BOS            :", result.bos)
print("CHOCH          :", result.choch)