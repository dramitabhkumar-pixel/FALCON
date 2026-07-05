import numpy as np
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
            "sharpe_ratio": 0.0,
            "expectancy": 0.0,
            "average_winner": 0.0,
            "average_loser": 0.0,
            "largest_winner": 0.0,
            "largest_loser": 0.0,
            "monthly_returns": {},
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
    win_rate = round(len(wins) / len(trades) * 100, 2)
    loss_rate = 100.0 - win_rate

    average_winner = round(float(wins.mean()), 2) if not wins.empty else 0.0
    average_loser = round(float(losses.mean()), 2) if not losses.empty else 0.0
    largest_winner = round(float(wins.max()), 2) if not wins.empty else 0.0
    largest_loser = round(float(losses.min()), 2) if not losses.empty else 0.0

    expectancy = round((win_rate / 100.0 * average_winner) + (loss_rate / 100.0 * average_loser), 2)

    sharpe = 0.0
    # Try calculating daily returns first
    if "exit_time" in trades.columns and trades["exit_time"].notna().any():
        try:
            temp_df = pd.DataFrame({
                "timestamp": pd.to_datetime(trades["exit_time"]),
                "equity": equity
            })
            temp_df = temp_df.set_index("timestamp").sort_index()
            daily_equity = temp_df["equity"].resample("D").last().ffill()
            if len(daily_equity) > 1:
                daily_returns = daily_equity.pct_change().dropna()
                if daily_returns.std() > 0:
                    sharpe = float((daily_returns.mean() / daily_returns.std()) * np.sqrt(252))
        except Exception:
            pass

    # Fallback to trade returns
    if sharpe == 0.0:
        try:
            prior_equity = initial_capital + pnl.cumsum().shift(1).fillna(0)
            trade_returns = pnl / prior_equity
            if len(trade_returns) > 1 and trade_returns.std() > 0:
                sharpe = float((trade_returns.mean() / trade_returns.std()) * np.sqrt(252))
        except Exception:
            pass

    monthly_dict = {}
    if "exit_time" in trades.columns and trades["exit_time"].notna().any():
        try:
            temp_df = pd.DataFrame({
                "timestamp": pd.to_datetime(trades["exit_time"]),
                "pnl": pnl
            })
            temp_df = temp_df.set_index("timestamp").sort_index()
            monthly_pnl = temp_df["pnl"].resample("ME").sum()
            for month, m_pnl in monthly_pnl.items():
                month_str = month.strftime("%Y-%m")
                prior_pnl = temp_df[:month]["pnl"].sum() - m_pnl
                start_equity = initial_capital + prior_pnl
                pct_return = (m_pnl / start_equity * 100) if start_equity > 0 else 0.0
                monthly_dict[month_str] = round(float(pct_return), 2)
        except Exception:
            pass

    return {
        "total_trades": int(len(trades)),
        "winning_trades": int(len(wins)),
        "losing_trades": int(len(losses)),
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "avg_pnl": round(float(pnl.mean()), 2),
        "profit_factor": round(
            gross_profit / gross_loss if gross_loss > 0 else float("inf"),
            2,
        ),
        "max_drawdown": round(float(max_drawdown) * 100, 2),
        "return_pct": round(total_pnl / initial_capital * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "expectancy": expectancy,
        "average_winner": average_winner,
        "average_loser": average_loser,
        "largest_winner": largest_winner,
        "largest_loser": largest_loser,
        "monthly_returns": monthly_dict,
    }
