"""
=========================================================
PROJECT FALCON
Indicator Engine Test
=========================================================
"""

import pandas as pd
import numpy as np

from engine.indicator_engine import IndicatorEngine
from models.indicator_result import IndicatorResult


def create_test_dataframe(rows: int = 100) -> pd.DataFrame:

    np.random.seed(42)

    close = np.cumsum(np.random.randn(rows)) + 100

    high = close + np.random.rand(rows)

    low = close - np.random.rand(rows)

    open_ = close + np.random.randn(rows) * 0.2

    volume = np.random.randint(1000, 5000, rows)

    return pd.DataFrame({
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    })


def test_indicator_engine():

    df = create_test_dataframe()

    engine = IndicatorEngine()

    result = engine.analyze(df)

    assert isinstance(result, IndicatorResult)

    assert result.valid is True

    assert result.ema_fast > 0

    assert result.ema_slow > 0

    assert 0 <= result.rsi <= 100

    assert result.adx >= 0

    assert result.atr >= 0

    assert result.avg_atr >= 0

    assert isinstance(result.ema_alignment, bool)

    assert isinstance(result.high_volatility, bool)

    print()

    print("========== INDICATOR ENGINE ==========")
    print(result)
    print("======================================")