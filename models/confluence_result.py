from dataclasses import dataclass


@dataclass
class ConfluenceResult:

    score: int

    signal: str

    confidence: str

    trade_grade: str

    bullish_score: int

    bearish_score: int

    reasons: list[str]