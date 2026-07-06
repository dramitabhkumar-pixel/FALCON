from optimizer.parameter_grid import GRID


class Optimizer:

    def __init__(self, engine):

        self.engine = engine

    def optimize(self):

        results = []

        for ema_fast, ema_slow, adx, rsi, rr in GRID:

            self.engine.config.EMA_FAST = ema_fast
            self.engine.config.EMA_SLOW = ema_slow
            self.engine.config.ADX = adx
            self.engine.config.RSI = rsi
            self.engine.config.RR = rr

            metrics = self.engine.run()

            results.append({
                "ema_fast": ema_fast,
                "ema_slow": ema_slow,
                "adx": adx,
                "rsi": rsi,
                "rr": rr,
                "profit": metrics.net_profit,
                "pf": metrics.profit_factor,
                "win": metrics.win_rate
            })

        results.sort(
            key=lambda x: x["profit"],
            reverse=True
        )

        return results