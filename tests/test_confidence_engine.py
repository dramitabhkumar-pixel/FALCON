"""
=========================================================
PROJECT FALCON
Confidence Engine Tests
=========================================================
"""

import pytest

from engine.confidence_engine import ConfidenceEngine
from models.confluence_result import ConfluenceResult


def test_full_confidence_score():

    engine = ConfidenceEngine()

    confluence = ConfluenceResult(

        trend_alignment=True,
        structure_alignment=True,
        ema_alignment=True,
        momentum_confirmation=True,
        liquidity_confirmation=True,
        fibonacci_confirmation=True,
        golden_zone_confirmation=True,
        bos_confirmation=True,
        choch_confirmation=True,
        order_block_confirmation=True,
        fair_value_gap_confirmation=True,
        valid=True,
    )

    result = engine.run(confluence)

    assert result.confidence_score == 100
    assert result.grade == "A+"
    assert result.minimum_confidence_met is True
    assert result.valid is True


def test_zero_confidence_score():

    engine = ConfidenceEngine()

    confluence = ConfluenceResult()

    result = engine.run(confluence)

    assert result.confidence_score == 0
    assert result.grade == "D"
    assert result.minimum_confidence_met is False


@pytest.mark.parametrize(
    "score_flags, expected_score, expected_grade",
    [

        (
            dict(
                trend_alignment=True,
                structure_alignment=True,
                ema_alignment=True,
                momentum_confirmation=True,
                liquidity_confirmation=True,
                fibonacci_confirmation=True,
                golden_zone_confirmation=True,
                bos_confirmation=True,
            ),
            85,
            "A",
        ),

        (
            dict(
                trend_alignment=True,
                structure_alignment=True,
                ema_alignment=True,
                momentum_confirmation=True,
                liquidity_confirmation=True,
                fibonacci_confirmation=True,
            ),
            70,
            "B",
        ),

        (
            dict(
                trend_alignment=True,
                structure_alignment=True,
                ema_alignment=True,
                momentum_confirmation=True,
                liquidity_confirmation=True,
            ),
            60,
            "C",
        ),
    ],
)
def test_confidence_grades(score_flags, expected_score, expected_grade):

    engine = ConfidenceEngine()

    confluence = ConfluenceResult(**score_flags)

    result = engine.run(confluence)

    assert result.confidence_score == expected_score
    assert result.grade == expected_grade


def test_reasons_generated():

    engine = ConfidenceEngine()

    confluence = ConfluenceResult(
        trend_alignment=True,
        ema_alignment=True,
    )

    result = engine.run(confluence)

    assert len(result.reasons) == len(engine.WEIGHTS)