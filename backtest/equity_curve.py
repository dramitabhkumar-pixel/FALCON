"""
Equity curve utilities for backtests.
"""
from __future__ import annotations

from typing import Tuple
from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def build_equity_curve(trades: pd.DataFrame, initial_capital: float = 500_000) -> pd.DataFrame:
    """Build a simple equity curve from closed trades.

    trades: dataframe returned by `TradeHistory.to_dataframe()` with at least
    the columns `exit_time` and `pnl`.

    Returns a dataframe with columns: `timestamp`, `pnl`, `cumulative_pnl`,
    `equity` sorted by timestamp.
    """

    if trades is None or trades.empty:
        logger.debug("No trades provided to build equity curve")
        return pd.DataFrame(columns=["timestamp", "pnl", "cumulative_pnl", "equity"])

    df = trades.copy()

    # Try to parse exit_time; fall back to index order if parsing fails
    if "exit_time" in df.columns and df["exit_time"].notna().any():
        try:
            df["timestamp"] = pd.to_datetime(df["exit_time"], errors="coerce")
        except Exception:
            df["timestamp"] = pd.NaT
    else:
        df["timestamp"] = pd.NaT

    # Fill missing timestamps with monotonically increasing values to preserve order
    missing_mask = df["timestamp"].isna()
    if missing_mask.any():
        filler = pd.date_range("1970-01-01", periods=missing_mask.sum(), freq="S")
        df.loc[missing_mask, "timestamp"] = filler

    df = df.sort_values("timestamp").reset_index(drop=True)

    df["pnl"] = pd.to_numeric(df.get("pnl", 0.0), errors="coerce").fillna(0.0)
    df["cumulative_pnl"] = df["pnl"].cumsum()
    df["equity"] = initial_capital + df["cumulative_pnl"]

    return df[["timestamp", "pnl", "cumulative_pnl", "equity"]]
