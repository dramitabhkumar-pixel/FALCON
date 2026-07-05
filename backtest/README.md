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

This command backtests only the last 8 unique trading days from the CSV.

Available options:

- `--csv`, `-c`: path to the OHLC CSV file
- `--days`, `-d`: include only the last N unique trading days from the CSV
- `--symbol`, `-s`: backtest symbol label (default: `BANKNIFTY`)
- `--warmup`, `-w`: warmup bar count before live trading starts (default: 50)
- `--initial-capital`, `-i`: starting capital for performance metrics (default: 500000)
- `--out`, `-o`: output directory for reports (default: `journal`)
- `--verbose`, `-v`: enable verbose logging

Outputs written to `journal/` by default:

- `trades.csv` — closed trade journal
- `equity.csv` — equity curve
- `performance.csv` — summary metrics
- `report.html` — HTML report
