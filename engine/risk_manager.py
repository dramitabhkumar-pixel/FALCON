class RiskManager:

    def __init__(
        self,
        capital=100000,
        risk_percent=1.0,
        max_daily_loss=3000,
        max_open_positions=3,
        max_trades_per_day=5,
        min_rr=2.0
    ):

        self.capital = capital

        self.risk_percent = risk_percent

        self.max_daily_loss = max_daily_loss

        self.max_open_positions = max_open_positions

        self.max_trades_per_day = max_trades_per_day

        self.min_rr = min_rr

        self.daily_loss = 0

        self.trades_today = 0

    def calculate_position_size(
        self,
        entry_price,
        stop_loss
    ):

        risk_amount = self.capital * (self.risk_percent / 100)

        risk_per_unit = abs(entry_price - stop_loss)

        if risk_per_unit == 0:
            return 0

        quantity = int(risk_amount / risk_per_unit)

        return quantity

    def validate_trade(
        self,
        entry,
        stop_loss,
        target
    ):

        if stop_loss >= entry:
            return False

        risk = abs(entry - stop_loss)

        reward = abs(target - entry)

        if risk == 0:
            return False

        rr = reward / risk

        if rr < self.min_rr:
            return False

        return True

    def can_trade(
        self,
        open_positions
    ):

        if self.daily_loss >= self.max_daily_loss:
            return False

        if self.trades_today >= self.max_trades_per_day:
            return False

        if open_positions >= self.max_open_positions:
            return False

        return True

    def update_daily_loss(
        self,
        loss
    ):

        self.daily_loss += abs(loss)

    def increment_trade(self):

        self.trades_today += 1

    def reset_day(self):

        self.daily_loss = 0

        self.trades_today = 0