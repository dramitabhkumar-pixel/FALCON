# Backtest Runner

Run end-to-end backtests and generate reports.

Usage:

- Synthetic data:

```
python -m backtest -o journal -v
```

- From CSV:

```
python -m backtest -c path/to/ohlc.csv -d 8 -o journal
```

This command backtests only the last 8 calendar days of data from the CSV.

Outputs written to `journal/` by default:

- `trades.csv` — closed trade journal
- `equity.csv` — equity curve
- `performance.csv` — summary metrics
