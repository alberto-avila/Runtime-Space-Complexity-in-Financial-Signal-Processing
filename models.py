from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: str
    symbol: str
    price: float

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass
