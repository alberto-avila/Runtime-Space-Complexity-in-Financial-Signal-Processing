'''
Storing full data set in memory requires O(n), with n being the number of Market Data Points. 
'''

from typing import List
from models import MarketDataPoint
import csv

def load_market_data_csv(filepath: str) -> List[MarketDataPoint]:
    data: List[MarketDataPoint] = []

    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required = {"timestamp", "symbol", "price"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV must contain columns {required}. Found: {reader.fieldnames}")

        for row_num, row in enumerate(reader, start=2):
            try:
                ts = row["timestamp"].strip()
                sym = row["symbol"].strip()
                px = float(row["price"])
            except Exception as e:
                raise ValueError(f"Bad row at line {row_num}: {row}") from e

            data.append(MarketDataPoint(timestamp=ts, symbol=sym, price=px))

    print(f"Rows loaded: {len(data)}")
    return data
