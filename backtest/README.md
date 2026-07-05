# Backtest Runner

Run end-to-end backtests and generate reports.

Usage:

- Synthetic data:

```
python -m backtest.runner -o journal -v
```

- From CSV:

```
python -m backtest.runner -c path/to/ohlc.csv -o journal
```

Outputs written to `journal/` by default:

- `trades.csv` — closed trade journal
- `equity.csv` — equity curve
- `performance.csv` — summary metrics
