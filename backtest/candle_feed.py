"""
Bar-by-bar candle iterator for backtesting.
"""

from __future__ import annotations

import pandas as pd


class BacktestCandleFeed:
    """Walk forward through historical candles with a warmup period."""

    def __init__(self, df: pd.DataFrame, warmup_bars: int = 50):
        if len(df) <= warmup_bars:
            raise ValueError(
                f"Need more bars than warmup ({warmup_bars}), got {len(df)}"
            )

        self.df = df.reset_index(drop=True)
        self.warmup_bars = warmup_bars
        self._index = warmup_bars

    @property
    def current_index(self) -> int:
        return self._index

    def has_next(self) -> bool:
        return self._index < len(self.df)

    def window(self) -> pd.DataFrame:
        """Return all candles up to and including the current bar."""

        return self.df.iloc[: self._index + 1].copy()

    def current_bar(self) -> pd.Series:
        return self.df.iloc[self._index]

    def advance(self) -> None:
        self._index += 1

    def __iter__(self):
        while self.has_next():
            yield self.window(), self.current_bar()
            self.advance()
