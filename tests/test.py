assert len(data) == 100_000
assert isinstance(data[0], MarketDataPoint)
assert data[0].price == 186.5
assert data[1].symbol == "NVDA"
