from models import MarketDataPoint
from reporting import plot_runtime_vs_input_size, plot_memory_vs_input_size
from data_loader import load_market_data_csv
from profiler import time_one, peak_memory_one, cprofile_one, line_profile_one
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, BetterMovingAverageStrategy
from multiprocessing import freeze_support
from pathlib import Path

ROOT = Path(__file__).parent

if __name__ == "__main__":
    freeze_support()
    path = ROOT / "data" / "market_data.csv"
    data = load_market_data_csv(path)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)

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
        data=data,n=i, out_path=ROOT / "results" / f"lineprofile_naive{i}.txt")
        line_profile_one(strategy_factory=lambda: WindowedMovingAverageStrategy(),
        data=data, n=i, out_path=ROOT / "results" / f"lineprofile_window{i}.txt")

    print(f"{'ticks':>8} {'naive (s)':>10} {'windowed (s)':>13} {'naive (MiB)':>12} {'windowed (MiB)':>15}")
    for n, nt, wt, nm, wm in zip(sizes, naive_times, windowed_times, naive_memory, windowed_memory):
        print(f"{n:>8,} {nt:>10.4f} {wt:>13.4f} {nm:>12.2f} {wm:>15.2f}")

    better_time = time_one(lambda: BetterMovingAverageStrategy(), data, n=100_000, repeats=3)
    better_memory = peak_memory_one(lambda: BetterMovingAverageStrategy(), data, n=100_000)
    print(f"Better (running mean), 100,000 ticks: {better_time:.4f} s, {better_memory:.2f} MiB")

    plot_runtime_vs_input_size(sizes, naive_times, windowed_times, save_path=ROOT / "assets" / "runtime_plot.png")
    plot_memory_vs_input_size(sizes, naive_memory, windowed_memory, save_path=ROOT / "assets" / "memory_plot.png")
