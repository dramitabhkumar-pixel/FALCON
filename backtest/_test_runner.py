from pathlib import Path
from .backtest_engine import BacktestEngine
from .data_loader import make_synthetic_ohlc
from .equity_curve import build_equity_curve
from .report_generator import generate_reports

if __name__ == '__main__':
    df = make_synthetic_ohlc()
    engine = BacktestEngine(df)
    metrics, trades = engine.run_full()
    equity = build_equity_curve(trades)
    out = Path(__file__).resolve().parent.parent / 'test_reports_runner'
    print('Writing to', out)
    files = generate_reports(metrics, trades, equity, out_dir=out)
    print(files)
