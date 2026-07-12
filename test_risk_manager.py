from engine.risk_manager import RiskManager

engine = RiskManager()

result = engine.run(
    account_balance=500000,
    entry_price=100,
    STOPLOSS=95,
    target_price=115,
)

print("\n==============================")
print("FALCON RISK REPORT")
print("==============================")

print("Approved      :", result.approved)
print("Account       :", result.account_balance)
print("Risk %        :", result.risk_percent)
print("Risk Amount   :", result.risk_amount)
print("Quantity      :", result.quantity)
print("Risk Reward   :", result.risk_reward)
print("Message       :", result.message)