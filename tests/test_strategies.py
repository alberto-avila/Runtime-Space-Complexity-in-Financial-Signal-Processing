"""Tests for the data loader and the moving-average strategies. Run: python -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data_loader import load_market_data_csv
from models import MarketDataPoint
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, BetterMovingAverageStrategy


def run(strategy, prices):
    for p in prices:
        strategy.update(p)
    return strategy


class TestDataLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_market_data_csv(ROOT / "data" / "market_data.csv")

    def test_loads_all_rows(self):
        self.assertEqual(len(self.data), 100_000)
        self.assertIsInstance(self.data[0], MarketDataPoint)

    def test_first_rows(self):
        self.assertEqual(self.data[0].price, 186.5)
        self.assertEqual(self.data[1].symbol, "NVDA")


class TestStrategies(unittest.TestCase):
    PRICES = [10.0, 12.0, 11.0, 9.0, 13.0, 13.0, 8.0, 15.0, 14.0, 10.0, 11.0, 16.0]

    def test_better_matches_naive(self):
        """The running-mean strategy must produce exactly the same signals as the O(n^2) one."""
        data = load_market_data_csv(ROOT / "data" / "market_data.csv")[:5_000]
        prices = [t.price for t in data]
        naive = run(NaiveMovingAverageStrategy(), prices)
        better = run(BetterMovingAverageStrategy(), prices)
        self.assertEqual(naive.signals, better.signals)
        self.assertAlmostEqual(naive.total_return(), better.total_return())

    def test_windowed_matches_brute_force(self):
        window = 3
        strategy = run(WindowedMovingAverageStrategy(window=window), self.PRICES)
        expected = []
        for i, p in enumerate(self.PRICES):
            recent = self.PRICES[max(0, i - window + 1): i + 1]
            avg = sum(recent) / len(recent)
            expected.append("BUY" if p > avg else "SELL" if p < avg else "HOLD")
        self.assertEqual(strategy.signals, expected)
        self.assertLessEqual(len(strategy.prices), window)

    def test_total_return_uses_first_tick(self):
        expected = self.PRICES[-1] / self.PRICES[0] - 1.0
        for cls in (NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, BetterMovingAverageStrategy):
            with self.subTest(strategy=cls.__name__):
                self.assertAlmostEqual(run(cls(), self.PRICES).total_return(), expected)

    def test_total_return_needs_two_ticks(self):
        for cls in (NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, BetterMovingAverageStrategy):
            with self.subTest(strategy=cls.__name__):
                self.assertEqual(run(cls(), [100.0]).total_return(), 0.0)


if __name__ == "__main__":
    unittest.main()
