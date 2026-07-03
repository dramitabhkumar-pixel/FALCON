from engine.swing_engine import SwingEngine
from engine.market_context_engine import MarketContextEngine

from models.market_context import MarketContext

import pandas as pd

df = pd.DataFrame({

    "Open":[1,2,3,4,5,6,5,4,3,4,5,6,7,8,9],
    "High":[2,3,4,5,8,6,5,4,3,5,6,7,9,8,7],
    "Low":[1,2,3,4,5,4,3,2,1,2,3,4,5,6,5],
    "Close":[2,3,4,5,6,5,4,3,2,4,5,6,8,7,6]

})

context = MarketContext()

context.swings = SwingEngine().run(df)

context = MarketContextEngine().run(context)

print()

print("Trend      :", context.trend.trend)
print("Bias       :", context.trend.bias)
print("Strength   :", context.trend.strength)