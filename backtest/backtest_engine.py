"""
=========================================================
PROJECT FALCON
Backtest Engine
Version : 4.0
=========================================================

Historical replay engine for Project FALCON.

Responsibilities
----------------
• Replay historical candles
• Feed rolling DataFrame to StrategyRunner
• Collect TradeDecision objects
• Compute performance metrics

Contains NO trading logic.
=========================================================
"""

from __future__ import annotations


from typing import List

import pandas as pd

from models.trade_decision import TradeDecision

from backtest.strategy_runner import StrategyRunner
from strategy.strategy_config import CONFIG
from models.enums import TradeStatus
from models.trade_record import TradeRecord
from journal.journal_writer import JournalWriter


class BacktestEngine:
    """
    Historical replay engine.

    Replays candles sequentially through the
    frozen Project FALCON strategy pipeline.
    """

    def __init__(self) -> None:

        self.runner = StrategyRunner()

        self.trade_log: List[TradeDecision] = []
        self.journal = JournalWriter()

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate historical dataframe.
        """

        if dataframe is None:
            raise ValueError(
                "Historical dataframe cannot be None."
            )

        if dataframe.empty:
            raise ValueError(
                "Historical dataframe is empty."
            )

        dataframe.columns = [
            str(column).lower()
            for column in dataframe.columns
        ]

        required = [
            "open",
            "high",
            "low",
            "close",
        ]

        missing = [

            column

            for column in required

            if column not in dataframe.columns

        ]

        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )

    @staticmethod
    def _normalize(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize dataframe columns.
        """

        df = dataframe.copy()

        df.columns = [

            str(column).lower()

            for column in df.columns

        ]

        return df

    @staticmethod
    def _minimum_bars() -> int:
        """
        Minimum candles before strategy evaluation.
        """

        return max(

            CONFIG.SLOW_EMA,

            CONFIG.ADX_PERIOD,

            CONFIG.ATR_PERIOD,

            CONFIG.RSI_PERIOD,

            50,

        )

    # =====================================================
    # Public API
    # =====================================================

    def run(
      self,
      dataframe: pd.DataFrame,
      symbol: str = "",
) -> List[TradeDecision]:
        
    
        """
        Execute a historical backtest.

        Parameters
        ----------
        dataframe
            Historical OHLCV dataframe.

        symbol
            Trading symbol.

        Returns
        -------
        list[TradeDecision]
        """
        print("########## MY BACKTEST ENGINE IS RUNNING ##########")
        self._validate_dataframe(
            dataframe,
        )
        
        df = self._normalize(
        dataframe,
        )
        print("\nFIRST INDEX :", df.index[0])
        print("LAST INDEX  :", df.index[-1])
        print("\nLAST 10 INDEX VALUES")
        print(df.index[-10:])
        print(df.columns.tolist())
        self.trade_log.clear()

        minimum = self._minimum_bars()
        

        

        # -------------------------------------------------
        # Historical Replay
        # -------------------------------------------------

        for index in range(

            minimum,

            len(df),

        ):

            history = df.iloc[
                : index + 1
            ].copy()
            print(history.index[-1])
            
            if "timestamp" in history.columns:
                print("BACKTEST :", history.iloc[-1]["timestamp"])
            
            else:
                print("BACKTEST INDEX :", history.index[-1])



            decision = self.runner.process(

                dataframe=history,

                symbol=symbol,

            )

            if decision is None:

                continue
            
            
            

            # Store only completed trades
            if decision.status == TradeStatus.CLOSED:
               self.trade_log.append(decision)
               
            record = TradeRecord(
                    trade_id=decision.trade_id,
                    symbol=decision.symbol,

                    direction=decision.direction,

                    entry_time=decision.entry_time,

                    exit_time=decision.exit_time,

                    entry_price=decision.entry_price,

                    exit_price=decision.exit_price,

                    stop_loss=decision.stop_loss,

                    target=decision.target,

                    quantity=decision.quantity,

                    pnl=decision.pnl,

                    exit_reason=decision.exit_reason,

                    confidence=decision.confidence_score,

                    winner=decision.pnl > 0,
                )   

            self.journal.write_trade(record)

           

            

            

     

                

              

            closed = sum(
                1 for t in self.trade_log
                if t.status == TradeStatus.CLOSED
            )

            active = sum(
                1 for t in self.trade_log
                if t.status == TradeStatus.ACTIVE
            )

            pending = sum(
                1 for t in self.trade_log
                if t.status == TradeStatus.PENDING
            )

        print("\n========== SUMMARY ==========")
        print("Total   :", len(self.trade_log))
        print("Closed  :", closed)
        print("Active  :", active)
        print("Pending :", pending)
        print("=============================")

        # -------------------------------------------------
        # Performance Summary
        # -------------------------------------------------

        winners = [t for t in self.trade_log if t.pnl > 0]
        losers = [t for t in self.trade_log if t.pnl <= 0]

        print("\n========== PERFORMANCE ==========")
        print("Total Trades :", len(self.trade_log))
        print("Winners      :", len(winners))
        print("Losers       :", len(losers))

        if self.trade_log:
            print(
        "Win Rate     :",
        round(len(winners) * 100 / len(self.trade_log), 2),
        "%",
    )

        print("=================================")
        print("\n========== TRADE LIST ==========")

        for i, trade in enumerate(self.trade_log, start=1):

            print(
                i,
                trade.trade_id,
                trade.direction.name,
                trade.entry_time,
                trade.exit_time,
                trade.exit_reason.name,
                round(trade.pnl, 2),
            )

        print("================================")
        ids = [t.trade_id for t in self.trade_log]

        print("\nUnique IDs :", len(set(ids)))
        print("Total IDs  :", len(ids))
        targets = sum(
            1 for t in self.trade_log
            if t.exit_reason.name == "TARGET"
        )

        stops = sum(
        1 for t in self.trade_log
        if t.exit_reason.name == "STOPLOSS"
        )

        print("\nTargets :", targets)
        print("Stops   :", stops)
        print("\n========== PNL ==========")

        for trade in self.trade_log:

            print(
                trade.trade_id,
                trade.pnl,
            )
            self.runner.strategy_engine.analyzer.summary()
        return self.trade_log

            
        

            
            