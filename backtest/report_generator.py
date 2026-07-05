"""
Generate CSV reports for backtest runs.
"""
from __future__ import annotations

from pathlib import Path
import logging
import pandas as pd
from typing import Dict

logger = logging.getLogger(__name__)


def generate_reports(
    metrics: dict,
    trades: pd.DataFrame,
    equity: pd.DataFrame,
    out_dir: str | Path = "journal",
) -> Dict[str, Path]:
    """Write `trades`, `equity` and `metrics` to CSV files under `out_dir`.

    Returns a mapping of logical name -> path written.
    """

    out = Path(out_dir)
    # If a relative path is provided, write it relative to the repository root
    if not out.is_absolute():
        repo_root = Path(__file__).resolve().parent.parent
        out = repo_root / out
    out.mkdir(parents=True, exist_ok=True)

    files: Dict[str, Path] = {}

    trades_path = out / "trades.csv"
    trades.to_csv(trades_path, index=False)
    files["trades"] = trades_path

    equity_path = out / "equity.csv"
    equity.to_csv(equity_path, index=False)
    files["equity"] = equity_path

    perf_path = out / "performance.csv"
    pd.DataFrame([metrics]).to_csv(perf_path, index=False)
    files["performance"] = perf_path

    logger.info("Reports written to %s", out)
    return files
