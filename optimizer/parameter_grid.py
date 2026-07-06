from itertools import product

EMA_FAST = [5, 8, 10]
EMA_SLOW = [21, 29, 34]

ADX = [18, 20, 22, 25]

RSI = [55, 58, 60, 62]

RR = [1.5, 2.0, 2.5]

GRID = list(product(
    EMA_FAST,
    EMA_SLOW,
    ADX,
    RSI,
    RR
))