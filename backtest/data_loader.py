"""
Load and normalize OHLC data for backtesting.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_ALIASES = {
    "datetime": "datetime",
    "date": "datetime",
    "time": "datetime",
    "timestamp": "datetime",
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "volume": "volume",
    "vol": "volume",
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to Open, High, Low, Close, Volume."""

    renamed = {}

    for column in df.columns:
        key = str(column).strip().lower()
        if key in COLUMN_ALIASES:
            renamed[column] = COLUMN_ALIASES[key]

    normalized = df.rename(columns=renamed)

    required = ["open", "high", "low", "close"]
    missing = [col for col in required if col not in normalized.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if "volume" not in normalized.columns:
        normalized["volume"] = 0.0

    if "datetime" in normalized.columns:
        normalized["datetime"] = pd.to_datetime(normalized["datetime"])
        normalized = normalized.sort_values("datetime")
        normalized = normalized.set_index("datetime")

    output = normalized.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        output[col] = pd.to_numeric(output[col], errors="coerce")

    output = output.dropna(subset=["Open", "High", "Low", "Close"])

    return output


def _filter_last_n_days(df: pd.DataFrame, days: int) -> pd.DataFrame:
    if days <= 0:
        raise ValueError("days must be a positive integer")

    if df.index.empty:
        return df

    df = df.sort_index()
    unique_dates = pd.Series(df.index.date).drop_duplicates().tolist()
    if len(unique_dates) <= days:
        return df

    last_dates = unique_dates[-days:]
    last_dates_set = {d.isoformat() for d in last_dates}
    index_dates = pd.Index(df.index.date).astype(str)
    mask = index_dates.isin(last_dates_set)
    return df[mask]


def load_csv(path: str | Path, last_days: int | None = None) -> pd.DataFrame:
    """Load OHLCV data from a CSV file."""

    df = pd.read_csv(path)
    normalized = normalize_columns(df)

    if last_days is not None:
        normalized = _filter_last_n_days(normalized, last_days)

    return normalized


def make_synthetic_ohlc(
    bars: int = 200,
    seed: int = 42,
    start_price: float = 100.0,
) -> pd.DataFrame:
    """Build deterministic synthetic OHLC data for tests."""

    import numpy as np

    rng = np.random.default_rng(seed)
    close = start_price + np.cumsum(rng.normal(0.15, 0.8, bars))
    high = close + rng.uniform(0.2, 1.0, bars)
    low = close - rng.uniform(0.2, 1.0, bars)
    open_ = close + rng.uniform(-0.4, 0.4, bars)
    volume = rng.integers(1000, 5000, bars)

    index = pd.date_range("2024-01-01 09:15", periods=bars, freq="15min")

    df = pd.DataFrame(
        {
            "Open": open_,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        },
        index=index,
    )

    return df
