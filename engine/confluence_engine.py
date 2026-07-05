from config.confluence_config import (
    CONFLUENCE_WEIGHTS,
    BUY_THRESHOLD,
    STRONG_BUY_THRESHOLD,
    MIN_ADX,
    MIN_RSI_BULL,
)

from models.confluence_result import ConfluenceResult


class ConfluenceEngine:

    def __init__(self):
        print("[ConfluenceEngine] Initialized")

    def evaluate(
        self,
        market_structure,
        market_context,
        swing_direction,
        liquidity,
        ema_bullish,
        adx,
        rsi,
        atr_high,
        fib_golden_zone,
    ):

        score = 0
        reasons = []

        # -----------------------------
        # Market Structure
        # -----------------------------
        if market_structure == "BULLISH":
            score += CONFLUENCE_WEIGHTS["market_structure"]
            reasons.append("Bullish market structure")

        # -----------------------------
        # Market Context
        # -----------------------------
        if market_context == "UPTREND":
            score += CONFLUENCE_WEIGHTS["market_context"]
            reasons.append("Uptrend confirmed")

        # -----------------------------
        # Swing Structure
        # -----------------------------
        if swing_direction == "HH_HL":
            score += CONFLUENCE_WEIGHTS["swing"]
            reasons.append("HH-HL swing sequence")

        # -----------------------------
        # Liquidity
        # -----------------------------
        if liquidity == "BUY_SIDE":
            score += CONFLUENCE_WEIGHTS["liquidity"]
            reasons.append("Buy-side liquidity")

        # -----------------------------
        # EMA Trend
        # -----------------------------
        if ema_bullish:
            score += CONFLUENCE_WEIGHTS["ema"]
            reasons.append("EMA bullish crossover")

        # -----------------------------
        # ADX
        # -----------------------------
        if adx >= MIN_ADX:
            score += CONFLUENCE_WEIGHTS["adx"]
            reasons.append(f"Strong Trend (ADX = {adx})")

        # -----------------------------
        # RSI
        # -----------------------------
        if rsi >= MIN_RSI_BULL:
            score += CONFLUENCE_WEIGHTS["rsi"]
            reasons.append(f"Bullish RSI ({rsi})")

        # -----------------------------
        # ATR
        # -----------------------------
        if atr_high:
            score += CONFLUENCE_WEIGHTS["atr"]
            reasons.append("High Volatility")

        # -----------------------------
        # Fibonacci
        # -----------------------------
        if fib_golden_zone:
            score += CONFLUENCE_WEIGHTS["fibonacci"]
            reasons.append("Inside Fibonacci Golden Zone")

        # -----------------------------
        # Confidence
        # -----------------------------
        confidence = round((score / 100) * 100)

        # -----------------------------
        # Trade Grade
        # -----------------------------
        if score >= 95:
            trade_grade = "A+"
        elif score >= 85:
            trade_grade = "A"
        elif score >= 70:
            trade_grade = "B"
        elif score >= 50:
            trade_grade = "C"
        else:
            trade_grade = "REJECT"

        # -----------------------------
        # Signal
        # -----------------------------
        if score >= STRONG_BUY_THRESHOLD:
            signal = "STRONG BUY"

        elif score >= BUY_THRESHOLD:
            signal = "BUY"

        elif score >= 50:
            signal = "WATCH"

        else:
            signal = "NO TRADE"

        return ConfluenceResult(
            score=score,
            signal=signal,
            confidence=f"{confidence}%",
            trade_grade=trade_grade,
            bullish_score=score,
            bearish_score=100 - score,
            reasons=reasons,
        )