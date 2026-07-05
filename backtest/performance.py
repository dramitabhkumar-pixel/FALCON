"""
Backtest performance metrics.
"""

from __future__ import annotations

import pandas as pd


def compute_metrics(trades: pd.DataFrame, initial_capital: float = 500_000) -> dict:
    """Compute summary statistics from a trade history dataframe."""

    if trades.empty:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0,
            "total_pnl": 0.0,
            "avg_pnl": 0.0,
            "profit_factor": 0.0,
            "max_drawdown": 0.0,
            "return_pct": 0.0,
        }

    pnl = trades["pnl"].astype(float)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]

    gross_profit = wins.sum()
    gross_loss = abs(losses.sum())

    equity = initial_capital + pnl.cumsum()
    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = abs(drawdown.min()) if len(drawdown) else 0.0

    total_pnl = round(float(pnl.sum()), 2)

    return {
        "total_trades": int(len(trades)),
        "winning_trades": int(len(wins)),
        "losing_trades": int(len(losses)),
        "win_rate": round(len(wins) / len(trades) * 100, 2),
        "total_pnl": total_pnl,
        "avg_pnl": round(float(pnl.mean()), 2),
        "profit_factor": round(
            gross_profit / gross_loss if gross_loss > 0 else float("inf"),
            2,
        ),
        "max_drawdown": round(float(max_drawdown) * 100, 2),
        "return_pct": round(total_pnl / initial_capital * 100, 2),
    }
