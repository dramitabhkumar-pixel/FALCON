"""
=========================================================
Project FALCON
Risk Management Engine
Version : 1.0
=========================================================
"""

from core.base_engine import BaseEngine

from config.risk_config import (
    RISK_PER_TRADE,
    MAX_DAILY_LOSS,
    MAX_OPEN_TRADES,
    MIN_RISK_REWARD,
)


class RiskManager(BaseEngine):

    def __init__(self):

        super().__init__()

        self.trades_today = 0

        self.daily_loss = 0.0

        self.log("Risk Manager Initialized")

    # -----------------------------------------------------

    def calculate_position_size(

        self,

        entry_price: float,

        stop_loss: float,

        account_size: float = 500000,

    ) -> int:

        risk_amount = account_size * RISK_PER_TRADE

        risk_per_unit = abs(entry_price - stop_loss)

        if risk_per_unit <= 0:

            return 0

        qty = int(risk_amount // risk_per_unit)

        return qty

    # -----------------------------------------------------

    def validate_trade(

        self,

        entry: float,

        stop_loss: float,

        target: float,

    ) -> bool:

        risk = abs(entry - stop_loss)

        reward = abs(target - entry)

        if risk <= 0:

            return False

        rr = reward / risk

        return rr >= MIN_RISK_REWARD

    # -----------------------------------------------------

    def can_trade(

        self,

        open_positions: int,

    ) -> bool:

        if open_positions >= MAX_OPEN_TRADES:

            return False

        if self.daily_loss >= MAX_DAILY_LOSS * 500000:

            return False

        return True

    # -----------------------------------------------------

    def increment_trade(self):

        self.trades_today += 1

    # -----------------------------------------------------

    def update_daily_loss(

        self,

        loss: float,

    ):

        self.daily_loss += loss

    # -----------------------------------------------------

    def reset(self):

        self.trades_today = 0

        self.daily_loss = 0.0

        self.log("Risk Manager Reset")