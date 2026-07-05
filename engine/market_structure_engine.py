"""
==========================================================
FALCON MARKET STRUCTURE ENGINE
Version : 2.0

Determines market structure from swing points.

Author : Amitabh Kumar + ChatGPT
==========================================================
"""

from core.base_engine import BaseEngine
from core.models import MarketStructure


class MarketStructureEngine(BaseEngine):

    def __init__(self):
        super().__init__()

        self.previous_structure = None

    def analyze(self, swings):

        self.log("Running Market Structure Engine")

        highs = []
        lows = []

        for swing in swings:

            if swing["type"] == "HIGH":
                highs.append(swing)

            elif swing["type"] == "LOW":
                lows.append(swing)

        if len(highs) < 2 or len(lows) < 2:

            return MarketStructure(

                trend="UNKNOWN",

                last_high_type="NA",

                last_low_type="NA",

                protected_high=None,

                protected_low=None,

                bos=False,

                choch=False
            )

        # ============================================
        # HIGHS
        # ============================================

        previous_high = highs[-2]["price"]
        current_high = highs[-1]["price"]

        if current_high > previous_high:
            high_type = "HH"
        else:
            high_type = "LH"

        # ============================================
        # LOWS
        # ============================================

        previous_low = lows[-2]["price"]
        current_low = lows[-1]["price"]

        if current_low > previous_low:
            low_type = "HL"
        else:
            low_type = "LL"

        # ============================================
        # TREND
        # ============================================

        if high_type == "HH" and low_type == "HL":

            trend = "UPTREND"

        elif high_type == "LH" and low_type == "LL":

            trend = "DOWNTREND"

        else:

            trend = "RANGE"

        # ============================================
        # PROTECTED LEVELS
        # ============================================

        protected_high = previous_high
        protected_low = previous_low

        # ============================================
        # BOS
        # ============================================

        bos = False

        if trend == "UPTREND":

            if current_high > protected_high:
                bos = True

        elif trend == "DOWNTREND":

            if current_low < protected_low:
                bos = True

        # ============================================
        # CHOCH
        # ============================================

        choch = False

        if self.previous_structure is not None:

            if self.previous_structure.trend != trend:

                if trend != "RANGE":

                    choch = True

        structure = MarketStructure(

            trend=trend,

            last_high_type=high_type,

            last_low_type=low_type,

            protected_high=protected_high,

            protected_low=protected_low,

            bos=bos,

            choch=choch
        )

        self.previous_structure = structure

        return structure