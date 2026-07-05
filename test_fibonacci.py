from engine.fibonacci_engine import FibonacciEngine

engine = FibonacciEngine()

levels = engine.calculate(
    high=120,
    low=100,
    trend="UPTREND"
)

print()

print("High :", levels.high)
print("Low  :", levels.low)

print()

print("0%    :", round(levels.fib_0, 2))
print("23.6% :", round(levels.fib_23_6, 2))
print("38.2% :", round(levels.fib_38_2, 2))
print("50%   :", round(levels.fib_50, 2))
print("61.8% :", round(levels.fib_61_8, 2))
print("78.6% :", round(levels.fib_78_6, 2))
print("100%  :", round(levels.fib_100, 2))

print()

print(
    "Golden Zone :",
    round(levels.golden_zone_top, 2),
    "to",
    round(levels.golden_zone_bottom, 2)
)