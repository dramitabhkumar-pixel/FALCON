"""
=========================================================
PROJECT FALCON
Strategy Analyzer
Version : 1.0
=========================================================

Observes every evaluated trading setup.

Responsibilities
----------------
• Record every evaluated setup
• Record accepted/rejected decisions
• Produce research statistics

This module NEVER influences trading decisions.

Author : Amitabh Kumar + ChatGPT
=========================================================
"""

from __future__ import annotations

from strategy.strategy_config import CONFIG


class StrategyAnalyzer:
    """
    Research engine for Project FALCON.

    Observes the strategy pipeline without
    affecting trading decisions.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self) -> None:

        self.records = []

        self.setup_counter = 0

    # =====================================================
    # Public API
    # =====================================================

    def record(
        self,
        *,
        timestamp,
        setup,
        confluence,
        confidence,
        accepted: bool,
    ) -> None:
        """
        Record one evaluated setup.
        """

        self.setup_counter += 1

        record = {

            "setup_id": self.setup_counter,

            "timestamp": timestamp,

            "direction": setup.direction,

            "trend": setup.trend,

            "structure": setup.structure,

            

            "adx_confirmation": confluence.adx_confirmation,

            "rsi_confirmation": confluence.rsi_confirmation,

            

            
            "atr_confirmation":
                confluence.atr_confirmation,

            "daily_bias_confirmation":
                confluence.daily_bias_confirmation,

            "golden_zone":
                setup.golden_zone,

            "liquidity":
                 setup.liquidity,

            "entry_type":
                 getattr(setup, "entry_type", None),

            "confidence_score":
                confidence.confidence_score,

            "confidence_grade":
                confidence.grade,

            "minimum_confidence_met":
                confidence.minimum_confidence_met,

            "accepted":
                accepted,

            "distance_to_acceptance": max(
                0,
                CONFIG.MINIMUM_CONFIDENCE
                - confidence.confidence_score,
            ),

            "reasons":
                confidence.reasons.copy(),

        }

        self.records.append(record)

    def summary(self) -> None:
        total = len(self.records)
        if total == 0:

            print("\n========== STRATEGY ANALYZER ==========")
            print("No setups recorded.")
            print("=======================================\n")
            return
        accepted = sum(
            1
            for record in self.records
            if record["accepted"]
        )
        rejected = total - accepted
        average_score = round(
            sum(
                record["confidence_score"]
                for record in self.records
            )/total,
            2,
        )
        highest_score = max (
            record["confidence_score"]
            for record in self.records
        )
    

    

           

        lowest_score = min(
            record["confidence_score"]
            for record in self.records
        )

        average_distance = round(
            sum(
                record["distance_to_acceptance"]
                for record in self.records
            ) / total,
            2,
        )

        print("\n========== STRATEGY ANALYZER ==========")
        print("Total Setups      :", total)
        print("Accepted          :", accepted)
        print("Rejected          :", rejected)
        print("Average Score     :", average_score)
        print("Highest Score     :", highest_score)
        print("Lowest Score      :", lowest_score)
        print("Average Distance  :", average_distance)
        print("=======================================\n")

    def reset(self) -> None:
        """
        Reset analyzer.
        """

        self.records.clear()

        self.setup_counter = 0

    def __len__(self) -> int:
        """
        Number of recorded setups.
        """

        return len(self.records)