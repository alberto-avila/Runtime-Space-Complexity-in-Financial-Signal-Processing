class NaiveMovingAverageStrategy:
    def __init__(self):
        self.prices = []        
        self.signals = []       

    def update(self, price):
        self.prices.append(price)

        # recompute average from scratch
        avg_price = sum(self.prices) / len(self.prices)

        if price > avg_price:
            self.signals.append("BUY")
        elif price < avg_price:
            self.signals.append("SELL")
        else:
            self.signals.append("HOLD")

    def total_return(self):
        
        if len(self.prices) < 2:
            return 0.0
        return (self.prices[-1] / self.prices[0]) - 1.0


from collections import deque

class WindowedMovingAverageStrategy:
    def __init__(self, window=10):
        self.window = window
        self.prices = deque()
        self.running_sum = 0.0
        self.signals = []

    def update(self, price):
        self.prices.append(price)
        self.running_sum += price

        if len(self.prices) > self.window:
            removed = self.prices.popleft()
            self.running_sum -= removed

        avg_price = self.running_sum / len(self.prices)

        if price > avg_price:
            self.signals.append("BUY")
        elif price < avg_price:
            self.signals.append("SELL")
        else:
            self.signals.append("HOLD")

    def total_return(self):
        if len(self.prices) < 2:
            return 0.0
        return (self.prices[-1] / self.prices[0]) - 1.0
