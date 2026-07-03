import pandas as pd
import numpy as np

from engine.swing_engine_v3 import SwingEngine


# --------------------------------------
# Create Sample OHLC Data
# --------------------------------------

np.random.seed(42)

close = np.cumsum(np.random.randn(100)) + 100

high = close + np.random.uniform(0.3, 1.2, 100)
low = close - np.random.uniform(0.3, 1.2, 100)
open_ = close + np.random.uniform(-0.5, 0.5, 100)

df = pd.DataFrame(
    {
        "Open": open_,
        "High": high,
        "Low": low,
        "Close": close,
    }
)

# --------------------------------------
# Run Swing Engine
# --------------------------------------

engine = SwingEngine()

swings = engine.run(df)

print(swings)
print()
print(f"Total Swings : {len(swings)}")