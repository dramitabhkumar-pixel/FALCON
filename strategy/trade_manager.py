"""
=========================================================
PROJECT FALCON
Trade Manager
=========================================================

Manages complete lifecycle of a trade.
"""

from core.trade_state import TradeState
from models.trade_decision import TradeDecision


class TradeManager:

    def __init__(self):

        self.reset()

    # =========================================================

    def reset(self):

        self.trade = None

        self.state = TradeState.WAITING

        self.current_price = 0.0

        self.realized_pnl = 0.0

        self.unrealized_pnl = 0.0

    # =========================================================

    def load_trade(self, trade: TradeDecision):

        self.trade = trade

        if trade.valid:

            self.state = TradeState.READY

        else:

            self.state = TradeState.CANCELLED

    # =========================================================

    def open_trade(self):

        if self.state == TradeState.READY:

            self.state = TradeState.OPEN

    # =========================================================

    def update_price(self, price: float):

        self.current_price = price

        if self.trade is None:

            return

        if self.state not in (
            TradeState.OPEN,
            TradeState.BREAKEVEN,
            TradeState.TRAILING,
            TradeState.PARTIAL_EXIT,
        ):
            return

        if self.trade.signal == "BUY":

            self.unrealized_pnl = (
                price - self.trade.entry_price
            )

        elif self.trade.signal == "SELL":

            self.unrealized_pnl = (
                self.trade.entry_price - price
            )

    # =========================================================

    def move_to_breakeven(self):

        if self.state == TradeState.OPEN:

            self.trade.stop_loss = self.trade.entry_price

            self.state = TradeState.BREAKEVEN

    # =========================================================

    def trail_stop(self, new_stop):

        if self.state in (
            TradeState.OPEN,
            TradeState.BREAKEVEN,
            TradeState.TRAILING,
        ):

            self.trade.stop_loss = new_stop

            self.state = TradeState.TRAILING

    # =========================================================

    def partial_exit(self):

        if self.state in (
            TradeState.OPEN,
            TradeState.BREAKEVEN,
            TradeState.TRAILING,
        ):

            self.state = TradeState.PARTIAL_EXIT

    # =========================================================

    def target_hit(self):

        self.realized_pnl = self.unrealized_pnl

        self.state = TradeState.TARGET_HIT

    # =========================================================

    def stop_loss_hit(self):

        self.realized_pnl = self.unrealized_pnl

        self.state = TradeState.STOP_LOSS

    # =========================================================

    def close_trade(self):

        self.state = TradeState.CLOSED

    # =========================================================

    def summary(self):

        return {

            "state": self.state.value,

            "entry": self.trade.entry_price if self.trade else None,

            "stop_loss": self.trade.stop_loss if self.trade else None,

            "target": self.trade.target_price if self.trade else None,

            "current_price": self.current_price,

            "unrealized_pnl": round(self.unrealized_pnl, 2),

            "realized_pnl": round(self.realized_pnl, 2),
        }