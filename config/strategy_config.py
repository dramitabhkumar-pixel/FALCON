"""
Project FALCON
Strategy Configuration

Every backtest receives one StrategyConfig object.
No hardcoded parameters should exist inside engines.
"""

from dataclasses import dataclass


@dataclass
class StrategyConfig:
    # ========= Trend =========
    ema_fast: int = 5
    ema_slow: int = 29

    # ========= Momentum =========
    adx_period: int = 14
    adx_threshold: float = 20

    rsi_period: int = 14
    rsi_buy: float = 60
    rsi_sell: float = 40

    # ========= ATR =========
    atr_period: int = 14
    atr_multiplier: float = 1.5

    # ========= Fibonacci =========
    fib_low: float = 0.382
    fib_high: float = 0.618

    # ========= Risk =========
    risk_per_trade: float = 1.0
    reward_ratio: float = 2.0

    # ========= Filters =========
    use_market_context: bool = True
    use_liquidity: bool = True
    use_structure: bool = True
    use_fibonacci: bool = True
    use_volume: bool = False

    # ========= Trading Session =========
    session_start = "09:30"
    session_end = "15:00"

    # ========= Confidence =========
    minimum_score: int = 80