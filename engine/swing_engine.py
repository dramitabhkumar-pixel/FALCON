"""
=========================================================
Project FALCON
Swing Detection Engine
Version : 1.0
=========================================================
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class SwingPoint:
    """Represents a confirmed swing point."""

    index: int
    datetime: pd.Timestamp
    price: float
    swing_type: str


class SwingEngine:
    """Detects swing highs and swing lows."""

    def __init__(self, left_bars: int = 3, right_bars: int = 3):
        self.left_bars = left_bars
        self.right_bars = right_bars

    def validate_dataframe(self, df: pd.DataFrame) -> None:
        """Validate OHLC dataframe."""

        required_columns = ["Open", "High", "Low", "Close"]

        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Missing required column: {column}")

        if df.empty:
            raise ValueError("Input dataframe is empty.")

        if len(df) < (self.left_bars + self.right_bars + 1):
            raise ValueError("Not enough candles for swing detection.")

    def detect_swings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect swing highs and swing lows."""

        self.validate_dataframe(df)

        swings = []

        start = self.left_bars
        end = len(df) - self.right_bars

        for i in range(start, end):

            current_high = df.iloc[i]["High"]
            current_low = df.iloc[i]["Low"]

            left_highs = df.iloc[i-self.left_bars:i]["High"]
            right_highs = df.iloc[i+1:i+self.right_bars+1]["High"]

            left_lows = df.iloc[i-self.left_bars:i]["Low"]
            right_lows = df.iloc[i+1:i+self.right_bars+1]["Low"]

            if current_high > left_highs.max() and current_high > right_highs.max():
                swings.append({
                    "Index": i,
                    "Price": current_high,
                    "Type": "Swing High"
                })

            if current_low < left_lows.min() and current_low < right_lows.min():
                swings.append({
                    "Index": i,
                    "Price": current_low,
                    "Type": "Swing Low"
                })

        return pd.DataFrame(swings)