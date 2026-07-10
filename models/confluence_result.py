"""
=========================================================
PROJECT FALCON
Confluence Result Model
Version : 1.0
=========================================================

Pure domain model representing the output of the
Confluence Engine.

Contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from models.enums import (
    Trend,
    MarketBias,
    MarketStrength,
    StructureType,
    TradeDirection,
)


@dataclass(slots=True)
class ConfluenceResult:
    """
    Final confluence evaluation produced by
    Confluence Engine.

    This model is consumed by the Confidence Engine
    and Strategy Engine.
    """

    # -------------------------------------------------
    # Market Context
    # -------------------------------------------------

    trend: Trend = Trend.UNKNOWN
    bias: MarketBias = MarketBias.NEUTRAL
    strength: MarketStrength = MarketStrength.NORMAL

    # -------------------------------------------------
    # Structure
    # -------------------------------------------------

    structure: StructureType = StructureType.UNKNOWN

    # -------------------------------------------------
    # Direction
    # -------------------------------------------------

    direction: TradeDirection = TradeDirection.NONE

    # -------------------------------------------------
    # Confluence Components
    # -------------------------------------------------

    trend_alignment: bool = False

    structure_alignment: bool = False

    fibonacci_alignment: bool = False

    liquidity_alignment: bool = False

    ema_alignment: bool = False

    momentum_alignment: bool = False

    bos_confirmation: bool = False

    choch_confirmation: bool = False

    # -------------------------------------------------
    # Final Result
    # -------------------------------------------------

    score: float = 0.0

    valid: bool = False