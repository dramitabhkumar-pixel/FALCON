"""
==========================================================
Project FALCON
Version : 1.0

Main Entry Point
==========================================================
"""

from engine.risk_manager import RiskManager
from engine.execution_engine import ExecutionEngine

from models.enums import Direction


def main():

    print("=" * 60)
    print("🦅 PROJECT FALCON V1.0")
    print("Financial AI Logic for Chart Observation & Navigation")
    print("=" * 60)

    print("\nInitializing Engines...")

    risk = RiskManager()
    execution = ExecutionEngine()

    print("✓ Risk Manager")
    print("✓ Execution Engine")

    print("\n----------------------------------------")
    print("SIMULATED TRADE")
    print("----------------------------------------")

    symbol = "BANKNIFTY"

    side = Direction.LONG

    entry = 51000

    stop_loss = 50950

    target = 51150

    order = execution.execute_trade(

        symbol=symbol,

        side=side,

        entry=entry,

        stop_loss=stop_loss,

        target=target,

        open_positions=0,

    )

    if order is None:

        print("\nTrade Rejected")

        return

    print("\nTrade Executed Successfully")

    print(f"Order ID     : {order.order_id}")
    print(f"Symbol       : {order.symbol}")
    print(f"Side         : {order.side.value}")
    print(f"Quantity     : {order.quantity}")
    print(f"Entry Price  : {order.entry_price}")
    print(f"Stop Loss    : {order.stop_loss}")
    print(f"Target       : {order.target}")
    print(f"Status       : {order.status.value}")

    print("\n----------------------------------------")
    print("MARKET MOVES TO TARGET")
    print("----------------------------------------")

    current_price = 51160

    execution.monitor_trade(
        order,
        current_price
    )

    print("\n----------------------------------------")
    print("ORDER BOOK SUMMARY")
    print("----------------------------------------")

    execution.orderbook.summary()

    print("\n========================================")
    print("FALCON V1 EXECUTION TEST COMPLETED")
    print("========================================")


if __name__ == "__main__":
    main()