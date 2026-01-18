from dataclasses import dataclass

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: str
    symbol: str
    price: float
