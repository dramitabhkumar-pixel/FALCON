import pandas as pd
from backtest.performance import compute_metrics
from pathlib import Path

trades_path = Path('journal') / 'trades.csv'
if not trades_path.exists():
    print('No trades.csv found at', trades_path)
    raise SystemExit(1)

df = pd.read_csv(trades_path)
if 'PnL' in df.columns:
    df = df.rename(columns={'PnL': 'pnl'})

metrics = compute_metrics(df, initial_capital=500_000)

print('Metrics:')
for k, v in metrics.items():
    print(f"{k:20}: {v}")

print('\nReport files present:')
for name in ['trades.csv', 'equity.csv', 'performance.csv']:
    p = Path('journal') / name
    print(f"- {p}: {'exists' if p.exists() else 'missing'}")
