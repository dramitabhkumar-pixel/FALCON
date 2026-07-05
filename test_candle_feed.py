import pandas as pd

from data.candle_feed import CandleFeed

df = pd.DataFrame(

    {

        "datetime":[

            "2026-07-05 09:15",

            "2026-07-05 09:30",

            "2026-07-05 09:45"

        ],

        "open":[100,104,108],

        "high":[105,109,112],

        "low":[99,103,107],

        "close":[104,108,111],

        "volume":[15000,18000,21000]

    }

)

feed = CandleFeed()

candles = feed.load_dataframe(df)

for candle in candles:

    print()

    print(candle.timestamp)

    print("Bullish :", candle.bullish)

    print("Bearish :", candle.bearish)

    print("Body :", candle.body)

    print("Upper Wick :", candle.upper_wick)

    print("Lower Wick :", candle.lower_wick)

    print("Range :", candle.range)