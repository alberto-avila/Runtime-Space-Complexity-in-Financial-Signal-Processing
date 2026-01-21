from models import MarketDataPoint
from reporting import plot_runtime_vs_input_size, plot_memory_vs_input_size
from data_loader import load_market_data_csv
from profiler import time_one, peak_memory_one, cprofile_one, line_profile_one
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, BetterMovingAverageStrategy
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    path = "market_data.csv"
    data = load_market_data_csv(path)

    sizes = [1_000, 10_000, 100_000]
    naive_times = []
    windowed_times = []

    naive_memory = []
    windowed_memory = []

    for i in sizes:
        x = time_one(lambda: NaiveMovingAverageStrategy(), data, n=i, repeats=3)
        naive_times.append(x)
        x = time_one(lambda: WindowedMovingAverageStrategy(), data, n=i, repeats=3)
        windowed_times.append(x)
        x = peak_memory_one(lambda: NaiveMovingAverageStrategy(), data, n=i)
        naive_memory.append(x)
        x = peak_memory_one(lambda: WindowedMovingAverageStrategy(), data, n=i)
        windowed_memory.append(x)
        line_profile_one(strategy_factory=lambda: NaiveMovingAverageStrategy(),
        data=data,n=i, out_path=f"lineprofile_naive{i}.txt")
        line_profile_one(strategy_factory=lambda: WindowedMovingAverageStrategy(),
        data=data, n=i, out_path=f"lineprofile_window{i}.txt")

    plot_runtime_vs_input_size(sizes, naive_times, windowed_times)
    plot_memory_vs_input_size(sizes, naive_memory, windowed_memory)

    print(time_one(lambda: BetterMovingAverageStrategy(), data, n=100_000, repeats=3))
    print(peak_memory_one(lambda: BetterMovingAverageStrategy(), data, n=100_000))
