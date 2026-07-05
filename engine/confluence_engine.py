from config.confluence_config import (
    CONFLUENCE_WEIGHTS,
    BUY_THRESHOLD,
    STRONG_BUY_THRESHOLD,
    SELL_THRESHOLD,
    STRONG_SELL_THRESHOLD,
    MIN_ADX,
    MIN_RSI_BULL,
    MAX_RSI_BEAR,
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
        # -----------------------------
        # Bullish Score
        # -----------------------------
        bullish_score = 0
        bull_reasons = []

        if market_structure == "BULLISH":
            bullish_score += CONFLUENCE_WEIGHTS["market_structure"]
            bull_reasons.append("Bullish market structure")

        if market_context == "UPTREND":
            bullish_score += CONFLUENCE_WEIGHTS["market_context"]
            bull_reasons.append("Uptrend confirmed")

        if swing_direction == "HH_HL":
            bullish_score += CONFLUENCE_WEIGHTS["swing"]
            bull_reasons.append("HH-HL swing sequence")

        if liquidity == "BUY_SIDE":
            bullish_score += CONFLUENCE_WEIGHTS["liquidity"]
            bull_reasons.append("Buy-side liquidity")

        if ema_bullish:
            bullish_score += CONFLUENCE_WEIGHTS["ema"]
            bull_reasons.append("EMA bullish crossover")

        if adx >= MIN_ADX:
            bullish_score += CONFLUENCE_WEIGHTS["adx"]
            bull_reasons.append(f"Strong Trend (ADX = {adx})")

        if rsi >= MIN_RSI_BULL:
            bullish_score += CONFLUENCE_WEIGHTS["rsi"]
            bull_reasons.append(f"Bullish RSI ({rsi})")

        if atr_high:
            bullish_score += CONFLUENCE_WEIGHTS["atr"]
            bull_reasons.append("High Volatility")

        if fib_golden_zone and market_context == "UPTREND":
            bullish_score += CONFLUENCE_WEIGHTS["fibonacci"]
            bull_reasons.append("Inside Fibonacci Golden Zone (Bullish)")

        # -----------------------------
        # Bearish Score
        # -----------------------------
        bearish_score = 0
        bear_reasons = []

        if market_structure == "BEARISH":
            bearish_score += CONFLUENCE_WEIGHTS["market_structure"]
            bear_reasons.append("Bearish market structure")

        if market_context == "DOWNTREND":
            bearish_score += CONFLUENCE_WEIGHTS["market_context"]
            bear_reasons.append("Downtrend confirmed")

        if swing_direction == "LH_LL":
            bearish_score += CONFLUENCE_WEIGHTS["swing"]
            bear_reasons.append("LH-LL swing sequence")

        if liquidity == "SELL_SIDE":
            bearish_score += CONFLUENCE_WEIGHTS["liquidity"]
            bear_reasons.append("Sell-side liquidity")

        if not ema_bullish:
            bearish_score += CONFLUENCE_WEIGHTS["ema"]
            bear_reasons.append("EMA bearish crossover")

        if adx >= MIN_ADX:
            bearish_score += CONFLUENCE_WEIGHTS["adx"]
            bear_reasons.append(f"Strong Trend (ADX = {adx})")

        if rsi <= MAX_RSI_BEAR:
            bearish_score += CONFLUENCE_WEIGHTS["rsi"]
            bear_reasons.append(f"Bearish RSI ({rsi})")

        if atr_high:
            bearish_score += CONFLUENCE_WEIGHTS["atr"]
            bear_reasons.append("High Volatility")

        if fib_golden_zone and market_context == "DOWNTREND":
            bearish_score += CONFLUENCE_WEIGHTS["fibonacci"]
            bear_reasons.append("Inside Fibonacci Golden Zone (Bearish)")

        # -----------------------------
        # Determine Direction
        # -----------------------------
        if bullish_score >= bearish_score:
            score = bullish_score
            reasons = bull_reasons
            confidence = round((bullish_score / 100) * 100)

            if score >= STRONG_BUY_THRESHOLD:
                signal = "STRONG BUY"
            elif score >= BUY_THRESHOLD:
                signal = "BUY"
            elif score >= 50:
                signal = "WATCH"
            else:
                signal = "NO TRADE"

            trade_grade = self._get_grade(score)
        else:
            score = bearish_score
            reasons = bear_reasons
            confidence = round((bearish_score / 100) * 100)

            if score >= STRONG_SELL_THRESHOLD:
                signal = "STRONG SELL"
            elif score >= SELL_THRESHOLD:
                signal = "SELL"
            elif score >= 50:
                signal = "WATCH"
            else:
                signal = "NO TRADE"

            trade_grade = self._get_grade(score)

        return ConfluenceResult(
            score=score,
            signal=signal,
            confidence=f"{confidence}%",
            trade_grade=trade_grade,
            bullish_score=bullish_score,
            bearish_score=bearish_score,
            reasons=reasons,
        )

    def _get_grade(self, score: int) -> str:
        if score >= 95:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 50:
            return "C"
        return "REJECT"