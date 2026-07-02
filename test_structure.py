from engine.swing_engine import SwingEngine
from engine.structure_engine import StructureEngine

import pandas as pd

df = pd.DataFrame({

    "Open":[1,2,3,4,5,6,5,4,3,4,5,6,7,8,9],
    "High":[2,3,4,5,8,6,5,4,3,5,6,7,9,8,7],
    "Low":[1,2,3,4,5,4,3,2,1,2,3,4,5,6,5],
    "Close":[2,3,4,5,6,5,4,3,2,4,5,6,8,7,6]

})

swing_engine = SwingEngine()

swings = swing_engine.run(df)

print("\nSWINGS")
print(swings)

structure_engine = StructureEngine()

structure = structure_engine.run(swings)

print("\nSTRUCTURE")
print(structure)