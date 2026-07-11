"""
=========================================================
PROJECT FALCON
Confidence Configuration
Version : 1.0
=========================================================

Central configuration for the Confidence Engine.

Contains all scoring weights, confidence thresholds,
and grading cutoffs.
"""

# =========================================================
# Confidence Weights
# =========================================================

TREND_WEIGHT = 15

STRUCTURE_WEIGHT = 15

EMA_WEIGHT = 10

MOMENTUM_WEIGHT = 10

LIQUIDITY_WEIGHT = 10

FIBONACCI_WEIGHT = 10

GOLDEN_ZONE_WEIGHT = 10

BOS_WEIGHT = 5

CHOCH_WEIGHT = 5

ORDER_BLOCK_WEIGHT = 5

FAIR_VALUE_GAP_WEIGHT = 5

# =========================================================
# Confidence Thresholds
# =========================================================

MINIMUM_CONFIDENCE = 80

# =========================================================
# Confidence Grades
# =========================================================

GRADE_A_PLUS = 90

GRADE_A = 80

GRADE_B = 70

GRADE_C = 60