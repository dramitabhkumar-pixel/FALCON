"""
=========================================================
Project FALCON
Risk Result Model
=========================================================
"""

from dataclasses import dataclass


@dataclass
class RiskResult:
    approved: bool

    account_balance: float

    risk_percent: float

    risk_amount: float

    entry_price: float

    STOPLOSS: float

    target_price: float

    quantity: int

    risk_reward: float

    message: str