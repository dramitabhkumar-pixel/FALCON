"""
==========================================================
FALCON CANDLE FEED
==========================================================
"""

import pandas as pd

from core.candles import Candle


class CandleFeed:

    def __init__(self):

        self.candles = []

    def load_dataframe(self, df: pd.DataFrame):

        self.candles = []

        for _, row in df.iterrows():

            candle = Candle(

                timestamp=str(row["datetime"]),

                open=float(row["open"]),

                high=float(row["high"]),

                low=float(row["low"]),

                close=float(row["close"]),

                volume=float(row["volume"])

            )

            self.candles.append(candle)

        return self.candles

    def latest(self):

        return self.candles[-1]

    def all(self):

        return self.candles