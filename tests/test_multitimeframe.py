import os
import sys
import pandas as pd

# ----------------------------------------------------------
# Project Root
# ----------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ----------------------------------------------------------

from strategy.multitimeframe_engine import MultiTimeframeEngine

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

df15 = pd.read_csv(os.path.join(DATA_DIR, "bank_nifty_15min.csv"))
df1h = pd.read_csv(os.path.join(DATA_DIR, "bank_nifty_1hour.csv"))
df4h = pd.read_csv(os.path.join(DATA_DIR, "bank_nifty_4hour.csv"))
dfd = pd.read_csv(os.path.join(DATA_DIR, "bank_nifty_daily.csv"))

# ----------------------------------------------------------
# Create Engine
# ----------------------------------------------------------

engine = MultiTimeframeEngine(
    df_15m=df15,
    df_1h=df1h,
    df_4h=df4h,
    df_daily=dfd,
)

# ----------------------------------------------------------
# Run Engine
# ----------------------------------------------------------

print("=" * 60)
print("PROJECT FALCON - MULTI TIMEFRAME ENGINE TEST")
print("=" * 60)

engine.validate_data()

merged = engine.align_timeframes()

engine.validate_alignment()

engine.info()

print("\nFirst 5 Rows:")
print(engine.head())

print("\nLast 5 Rows:")
print(engine.tail())

print("\nEngine Object:")
print(engine)

print("\nTotal Rows:")
print(len(engine))

print("\nSample Context (Row 100):")
print(engine.get_context(min(100, len(engine)-1)))

print("\n✅ MultiTimeframe Engine Test Completed")