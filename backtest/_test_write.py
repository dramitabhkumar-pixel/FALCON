"""Internal test helper to write reports using backtest.report_generator."""
from pathlib import Path
import pandas as pd
from .report_generator import generate_reports

metrics = {"total_trades": 0}
trades = pd.DataFrame()
equity = pd.DataFrame()

out = Path(__file__).resolve().parent.parent / "test_reports"
print("Writing to:", out)
files = generate_reports(metrics, trades, equity, out_dir=out)
print(files)