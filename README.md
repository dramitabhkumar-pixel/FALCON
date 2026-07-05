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

```bash
python -m backtest.runner -c "c:\\Users\\pc\\Downloads\\bank_nifty_15min.csv" -o journal -v
```

Generated reports will be written to `journal/`:

- `journal/trades.csv`
- `journal/equity.csv`
- `journal/performance.csv`

For synthetic data (no CSV):

```bash
python -m backtest.runner -o journal -v
```
