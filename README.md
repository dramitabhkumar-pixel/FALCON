# Project FALCON

An institutional-grade algorithmic trading framework.

## Current Version

v0.2

## Completed

- BaseEngine
- SwingEngine
- StructureEngine
- Modular Models
- Test Framework

## Next Milestone

- Trend State Machine
- BOS Detection
- CHoCH Detection
- Fibonacci Engine

## Planned Modules

- Indicator Engine
- Confluence Engine
- Trade Engine
- Risk Engine
- Zerodha Integration

## Backtesting

Run the BankNIFTY 15-minute backtest using a CSV file with columns: Date/Datetime, Open, High, Low, Close, Volume.

Use `--csv` to specify the input file and `--days` to limit the backtest to the last N unique trading days:

```bash
python -m backtest.runner -c "c:\\Users\\pc\\Downloads\\bank_nifty_15min.csv" -d 8 -o journal -v
```

Available options:

- `--csv`, `-c`: path to the OHLC CSV file
- `--days`, `-d`: include only the last N unique trading days from the CSV
- `--symbol`, `-s`: symbol label for the backtest (default: `BANKNIFTY`)
- `--warmup`, `-w`: number of warmup bars before live trading begins (default: 50)
- `--initial-capital`, `-i`: initial capital for equity calculations (default: 500000)
- `--out`, `-o`: output directory for reports (default: `journal`)
- `--verbose`, `-v`: enable detailed logging

Generated reports will be written to `journal/`:

- `journal/trades.csv`
- `journal/equity.csv`
- `journal/performance.csv`
- `journal/report.html`

If the backtest generates no closed trades, `equity.csv` may be empty while `performance.csv` and `report.html` are still created.

For synthetic data (no CSV):

```bash
python -m backtest.runner -o journal -v
```
