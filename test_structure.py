from engine.swing_engine import SwingEngine
from engine.structure_engine import StructureEngine
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Open":  [1,2,3,4,5,6,5,4,3,4,5,6,7,8,9],
    "High":  [2,3,4,5,8,6,5,4,3,5,6,7,9,8,7],
    "Low":   [1,2,3,4,5,4,3,2,1,2,3,4,5,6,5],
    "Close": [2,3,4,5,6,5,4,3,2,4,5,6,8,7,6]
})

# Run Swing Engine
swing_engine = SwingEngine()
swings = swing_engine.detect_swings(df)

print("========== SWINGS ==========")
print(swings)

# Run Structure Engine
structure_engine = StructureEngine()
structure = structure_engine.detect_structure(swings)

print("\n========== STRUCTURE ==========")
print(structure)