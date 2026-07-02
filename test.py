from engine.swing_engine import SwingEngine
import pandas as pd

engine = SwingEngine()

df = pd.DataFrame({
    "Open":[1,2,3,4,5,6,5,4,3,4,5],
    "High":[2,3,4,5,8,6,5,4,3,5,6],
    "Low":[1,2,3,4,5,4,3,2,1,2,3],
    "Close":[2,3,4,5,6,5,4,3,2,4,5]
})

print(engine.run(df))