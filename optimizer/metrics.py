import numpy as np


def profit_factor(trades):
    wins = [t.pnl for t in trades if t.pnl > 0]
    losses = [abs(t.pnl) for t in trades if t.pnl < 0]

    if not losses:
        return float("inf")

    return sum(wins) / sum(losses)


def win_rate(trades):
    if len(trades) == 0:
        return 0

    wins = sum(t.pnl > 0 for t in trades)

    return wins / len(trades)


def expectancy(trades):
    if len(trades) == 0:
        return 0

    return np.mean([t.pnl for t in trades])


def max_drawdown(equity):
    peak = equity[0]
    max_dd = 0

    for value in equity:

        if value > peak:
            peak = value

        dd = peak - value

        if dd > max_dd:
            max_dd = dd

    return max_dd