"""
=========================================================
PROJECT FALCON
TradeSetup Validation
=========================================================
"""

from models.trade_setup import TradeSetup
from models.enums import (
    Trend,
    Bias,
    Strength,
    Structure,
    Direction,
)


def main():

    setup = TradeSetup()

    assert setup.trend == Trend.RANGE
    assert setup.bias == Bias.NEUTRAL
    assert setup.strength == Strength.NORMAL
    assert setup.structure == Structure.RANGE
    assert setup.direction == Direction.NONE

    print("========== TRADE SETUP ==========")
    print(setup)
    print()
    print("TradeSetup import successful.")
    print("Default values validated.")
    print("========== PASSED ==========")


if __name__ == "__main__":
    main()