import pandas as pd
import pytest

from backtest.backtest_engine import BacktestEngine, run_backtest
from backtest.candle_feed import BacktestCandleFeed
from backtest.data_loader import load_csv, make_synthetic_ohlc, normalize_columns
from backtest.performance import compute_metrics
from backtest.strategy_runner import StrategyRunner
from backtest.trade_engine import BacktestTradeEngine
from backtest.trade_history import TradeHistory


def test_normalize_columns_lowercase():
    df = pd.DataFrame(
        {
            "datetime": ["2024-01-01", "2024-01-02"],
            "open": [100, 101],
            "high": [102, 103],
            "low": [99, 100],
            "close": [101, 102],
        }
    )

    normalized = normalize_columns(df)

    assert list(normalized.columns) == [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]
    assert len(normalized) == 2


def test_candle_feed_window_grows():
    df = make_synthetic_ohlc(bars=80, seed=1)
    feed = BacktestCandleFeed(df, warmup_bars=20)

    windows = [window for window, _ in feed]

    assert len(windows) == 60
    assert len(windows[0]) == 21
    assert len(windows[-1]) == 80


def test_trade_engine_records_closed_trade():
    from enums import OrderSide

    engine = BacktestTradeEngine(symbol="TEST")
    order = engine.try_entry(
        side=OrderSide.BUY,
        entry=100,
        stop_loss=95,
        target=110,
    )

    bar = pd.Series(
        {"Open": 100, "High": 111, "Low": 99, "Close": 110},
        name="2024-01-01",
    )

    closed = engine.on_bar(bar)

    assert order is not None
    assert len(closed) == 1
    assert engine.history.total_pnl() > 0


def test_performance_metrics_empty():
    metrics = compute_metrics(pd.DataFrame())

    assert metrics["total_trades"] == 0
    assert metrics["win_rate"] == 0.0


def test_backtest_engine_runs_without_error():
    df = make_synthetic_ohlc(bars=120, seed=7)
    result = BacktestEngine(df, warmup_bars=40).run()

    assert "total_trades" in result
    assert "total_pnl" in result
    assert "bars_processed" in result
    assert result["bars_processed"] == 80


def test_run_backtest_helper():
    result = run_backtest(df=make_synthetic_ohlc(bars=100, seed=3), warmup_bars=30)

    assert result["symbol"] == "BANKNIFTY"
    assert result["entries"] >= 0


def test_strategy_runner_returns_none_on_short_data():
    df = make_synthetic_ohlc(bars=10, seed=1)
    setup = StrategyRunner().evaluate(df)

    assert setup is None
