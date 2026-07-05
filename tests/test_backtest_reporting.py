import tempfile
from pathlib import Path
import pandas as pd

from backtest.equity_curve import build_equity_curve
from backtest.report_generator import generate_reports


def test_build_equity_curve_empty():
    df = build_equity_curve(pd.DataFrame(), initial_capital=1000)
    assert list(df.columns) == ["timestamp", "pnl", "cumulative_pnl", "equity"]


def test_generate_reports_writes_files(tmp_path):
    metrics = {"total_trades": 0}
    trades = pd.DataFrame()
    equity = pd.DataFrame()

    out = tmp_path / "journal"
    files = generate_reports(metrics, trades, equity, out_dir=out)

    assert (out / "trades.csv").exists()
    assert (out / "equity.csv").exists()
    assert (out / "performance.csv").exists()


def test_build_equity_curve_without_timestamps():
    trades = pd.DataFrame(
        [
            {"pnl": 100.0, "exit_time": None},
            {"pnl": -20.0, "exit_time": None},
        ]
    )
    equity = build_equity_curve(trades, initial_capital=1000)

    assert len(equity) == 2
    assert list(equity.columns) == ["timestamp", "pnl", "cumulative_pnl", "equity"]
    assert equity.iloc[0]["equity"] == 1100
    assert equity.iloc[1]["equity"] == 1080
