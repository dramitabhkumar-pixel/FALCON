from engine.risk_manager import RiskManager


rm = RiskManager()

qty = rm.calculate_position_size(

    entry_price=51000,

    stop_loss=50950

)

print("Position Size :", qty)


print(

    "Trade Valid :",

    rm.validate_trade(

        entry=51000,

        stop_loss=50950,

        target=51150

    )

)


print(

    "Can Trade :",

    rm.can_trade(

        open_positions=1

    )

)


rm.increment_trade()

rm.update_daily_loss(500)


print("Trades Today :", rm.trades_today)

print("Daily Loss :", rm.daily_loss)