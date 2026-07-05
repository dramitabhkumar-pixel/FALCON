"""
=========================================================
Project FALCON
Risk Management Engine
Version : 1.0
=========================================================
"""

from core.base_engine import BaseEngine
from models.risk_result import RiskResult

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

        # Check max open positions
        if open_positions >= MAX_OPEN_TRADES:
            self.log(f"Cannot trade: open_positions({open_positions}) >= MAX_OPEN_TRADES({MAX_OPEN_TRADES})")
            return False

        # Check daily loss threshold (account size is assumed 500000)
        threshold = MAX_DAILY_LOSS * 500_000
        if self.daily_loss >= threshold:
            self.log(f"Cannot trade: daily_loss({self.daily_loss}) >= MAX_DAILY_LOSS*account({threshold})")
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

    # -----------------------------------------------------

    def run(
        self,
        account_balance: float,
        entry_price: float,
        stop_loss: float,
        target_price: float,
        open_positions: int = 0,
    ) -> RiskResult:
        """
        Runs risk checks and returns RiskResult.
        """
        can_tr = self.can_trade(open_positions)
        valid_tr = self.validate_trade(entry_price, stop_loss, target_price)

        approved = can_tr and valid_tr
        qty = self.calculate_position_size(entry_price, stop_loss, account_balance)

        risk_per_unit = abs(entry_price - stop_loss)
        reward_per_unit = abs(target_price - entry_price)

        risk_amount = qty * risk_per_unit
        risk_percent = (risk_amount / account_balance * 100) if account_balance > 0 else 0.0
        risk_reward = (reward_per_unit / risk_per_unit) if risk_per_unit > 0 else 0.0

        if not can_tr:
            message = f"Rejected: Limit hit (open_positions={open_positions}, daily_loss={self.daily_loss})"
        elif not valid_tr:
            message = f"Rejected: Invalid parameters or bad risk-reward (entry={entry_price}, sl={stop_loss}, target={target_price})"
        else:
            message = "Approved"

        return RiskResult(
            approved=approved,
            account_balance=account_balance,
            risk_percent=round(risk_percent, 2),
            risk_amount=round(risk_amount, 2),
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            quantity=qty,
            risk_reward=round(risk_reward, 2),
            message=message,
        )