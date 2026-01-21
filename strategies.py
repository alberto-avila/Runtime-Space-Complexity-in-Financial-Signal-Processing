from models import Strategy, MarketDataPoint


class NaiveMovingAverageStrategy(Strategy):
    def __init__(self):
        self.prices = []
        # prices stores all historical prices seen so far.
        # Space complexity: O(n), where n is the number of ticks processed.
        self.signals = []
        # signals stores one signal per tick.
        # Space complexity: O(n).

    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

    def update(self, price):
        self.prices.append(price)
        # Space grows by one element per call → O(n) total.

        avg_price = sum(self.prices) / len(self.prices)
        # sum(self.prices) iterates over all stored prices.
        # Time complexity per update: O(n).
        # len(self.prices) and division are O(1).

        if price > avg_price:
            self.signals.append("BUY")
        elif price < avg_price:
            self.signals.append("SELL")
        else:
            self.signals.append("HOLD")

        # Overall per-update time complexity: O(n).
        # Total time complexity over n ticks: O(n^2).


    def total_return(self):
        if len(self.prices) < 2:
            # len(...) and indexing are O(1)
            return 0.0

        # Constant-time arithmetic and indexing.
        # Time complexity: O(1).
        return (self.prices[-1] / self.prices[0]) - 1.0


from collections import deque

class WindowedMovingAverageStrategy(Strategy):
    def __init__(self, window=10):
        self.window = window
        # window is a fixed constant (k).
        # Space complexity: O(1).
        self.prices = deque()
        # prices stores at most k recent prices using a deque.
        # Space complexity: O(k).
        self.running_sum = 0.0
        # running_sum stores a single float.
        # Space complexity: O(1).
        self.signals = []
        # signals stores one signal per tick.
        # Space complexity: O(n).

    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

    def update(self, price):
        self.prices.append(price)
        # deque append is O(1).
        self.running_sum += price

        if len(self.prices) > self.window:
        # len(self.prices) is O(1).
            removed = self.prices.popleft()
            # deque popleft is O(1).
            self.running_sum -= removed

        avg_price = self.running_sum / len(self.prices)
        # Average computation uses running_sum and len(...) → O(1).

        if price > avg_price:
            self.signals.append("BUY")
            # Append is O(1).
        elif price < avg_price:
            self.signals.append("SELL")
            # Append is O(1).
        else:
            self.signals.append("HOLD")
            # Append is O(1).

    # Overall per-update time complexity: O(1).
    # Total time complexity over n ticks: O(n).

    def total_return(self):
        if len(self.prices) < 2:
        # len(...) and indexing are O(1).
            return 0.0

        # Constant-time arithmetic and indexing.
        # Time complexity: O(1).
        return (self.prices[-1] / self.prices[0]) - 1.0

class BetterMovingAverageStrategy(Strategy):
    def __init__(self):
        self.running_sum = 0.0
        self.count = 0
        self.first_price = None
        self.last_price = None
        self.signals = []

    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

    def update(self, price):
        if self.first_price is None:
            self.first_price = price
        self.last_price = price

        self.running_sum += price
        self.count += 1

        avg_price = self.running_sum / self.count

        if price > avg_price:
            self.signals.append("BUY")
        elif price < avg_price:
            self.signals.append("SELL")
        else:
            self.signals.append("HOLD")

    def total_return(self):
        if self.count < 2:
            return 0.0
        return (self.last_price / self.first_price) - 1.0
