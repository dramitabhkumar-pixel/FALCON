"""
Strategy orchestration for backtests.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from config.risk_config import MIN_RISK_REWARD
from core.constants import (
    ADX_PERIOD,
    ATR_PERIOD,
    EMA_FAST,
    EMA_SLOW,
    RSI_PERIOD,
)
from engine.confluence_engine import ConfluenceEngine
from engine.fibonacci_engine import FibonacciEngine
from engine.liquidity_engine import LiquidityEngine
from engine.market_context_engine import MarketContextEngine
from engine.market_structure_engine import MarketStructureEngine
from engine.swing_engine_v3 import SwingEngine
from enums import OrderSide
from models.confluence_result import ConfluenceResult


@dataclass
class TradeSetup:
    side: OrderSide
    entry: float
    stop_loss: float
    target: float
    confluence: ConfluenceResult


def swings_to_dicts(swings: pd.DataFrame) -> list[dict]:
    return [
        {"type": row["Type"], "price": float(row["Price"])}
        for _, row in swings.iterrows()
    ]


class StrategyRunner:
    """Run FALCON analysis engines and produce trade setups."""

    def __init__(self):
        self.swing_engine = SwingEngine()
        self.structure_engine = MarketStructureEngine()
        self.context_engine = MarketContextEngine()
        self.liquidity_engine = LiquidityEngine()
        self.fib_engine = FibonacciEngine()
        self.confluence_engine = ConfluenceEngine()

    def evaluate(self, df: pd.DataFrame) -> TradeSetup | None:
        if len(df) < max(EMA_SLOW, ADX_PERIOD, RSI_PERIOD, ATR_PERIOD) + 5:
            return None

        swings = self.swing_engine.run(df)
        if swings.empty:
            return None

        swings_dicts = swings_to_dicts(swings)
        structure = self.structure_engine.analyze(swings_dicts)
        indicators = self._compute_indicators(df)
        latest = indicators.iloc[-1]

        if pd.isna(latest["adx"]) or pd.isna(latest["rsi"]):
            return None

        context = self.context_engine.analyze(
            adx=float(latest["adx"]),
            ema_fast=float(latest["ema_fast"]),
            ema_slow=float(latest["ema_slow"]),
            rsi=float(latest["rsi"]),
            atr=float(latest["atr"]),
            avg_atr=float(latest["avg_atr"]),
        )

        liquidity = self.liquidity_engine.analyze(swings_dicts)
        fib_golden_zone = self._in_golden_zone(df, context.trend, swings)

        swing_direction = "HH_HL"
        if not (
            structure.last_high_type == "HH"
            and structure.last_low_type == "HL"
        ):
            swing_direction = "OTHER"

        structure_bias = {
            "UPTREND": "BULLISH",
            "DOWNTREND": "BEARISH",
            "RANGE": "NEUTRAL",
        }.get(structure.trend, "NEUTRAL")

        liquidity_side = (
            "BUY_SIDE"
            if liquidity.buy_side_liquidity
            else "NONE"
        )

        confluence = self.confluence_engine.evaluate(
            market_structure=structure_bias,
            market_context=context.trend,
            swing_direction=swing_direction,
            liquidity=liquidity_side,
            ema_bullish=latest["ema_fast"] > latest["ema_slow"],
            adx=float(latest["adx"]),
            rsi=float(latest["rsi"]),
            atr_high=latest["atr"] >= latest["avg_atr"],
            fib_golden_zone=fib_golden_zone,
        )

        if confluence.signal not in ("BUY", "STRONG BUY"):
            return None

        entry = float(df.iloc[-1]["Close"])
        stop_loss = self._build_stop_loss(structure, entry)
        if stop_loss is None or stop_loss >= entry:
            return None

        risk = entry - stop_loss
        target = entry + risk * MIN_RISK_REWARD

        return TradeSetup(
            side=OrderSide.BUY,
            entry=round(entry, 2),
            stop_loss=round(stop_loss, 2),
            target=round(target, 2),
            confluence=confluence,
        )

    def _build_stop_loss(self, structure, entry: float) -> float | None:
        if structure.protected_low is not None:
            return float(structure.protected_low)

        if structure.protected_high is not None and entry < structure.protected_high:
            return float(structure.protected_high)

        return None

    def _in_golden_zone(
        self,
        df: pd.DataFrame,
        trend: str,
        swings: pd.DataFrame,
    ) -> bool:
        if trend not in ("UPTREND", "DOWNTREND") or swings.empty:
            return False

        highs = swings[swings["Type"] == "HIGH"]
        lows = swings[swings["Type"] == "LOW"]
        if highs.empty or lows.empty:
            return False

        swing_high = float(highs.iloc[-1]["Price"])
        swing_low = float(lows.iloc[-1]["Price"])
        price = float(df.iloc[-1]["Close"])

        try:
            levels = self.fib_engine.calculate(swing_high, swing_low, trend)
        except Exception:
            return False

        zone_top = max(levels.golden_zone_top, levels.golden_zone_bottom)
        zone_bottom = min(levels.golden_zone_top, levels.golden_zone_bottom)
        return zone_bottom <= price <= zone_top

    def _compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        output = df.copy()

        output["ema_fast"] = output["Close"].ewm(
            span=EMA_FAST,
            adjust=False,
        ).mean()
        output["ema_slow"] = output["Close"].ewm(
            span=EMA_SLOW,
            adjust=False,
        ).mean()

        output["rsi"] = self._rsi(output["Close"], RSI_PERIOD)
        output["atr"] = self._atr(output, ATR_PERIOD)
        output["avg_atr"] = output["atr"].rolling(ATR_PERIOD).mean()
        output["adx"] = self._adx(output, ADX_PERIOD)

        return output

    @staticmethod
    def _rsi(series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def _atr(df: pd.DataFrame, period: int) -> pd.Series:
        high_low = df["High"] - df["Low"]
        high_close = (df["High"] - df["Close"].shift()).abs()
        low_close = (df["Low"] - df["Close"].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.ewm(alpha=1 / period, adjust=False).mean()

    @staticmethod
    def _adx(df: pd.DataFrame, period: int) -> pd.Series:
        up_move = df["High"].diff()
        down_move = -df["Low"].diff()

        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

        tr = StrategyRunner._atr(df, period)
        plus_di = 100 * pd.Series(plus_dm, index=df.index).ewm(
            alpha=1 / period,
            adjust=False,
        ).mean() / tr
        minus_di = 100 * pd.Series(minus_dm, index=df.index).ewm(
            alpha=1 / period,
            adjust=False,
        ).mean() / tr

        dx = (abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, np.nan)) * 100
        return dx.ewm(alpha=1 / period, adjust=False).mean()
