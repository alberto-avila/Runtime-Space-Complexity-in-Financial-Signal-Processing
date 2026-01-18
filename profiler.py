import json
import timeit
import cProfile
import pstats
from memory_profiler import memory_usage
from data_loader import load_market_data_csv
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy

def run_strategy(strategy, data, n):
    """Runs update() for first n ticks."""
    for tick in data[:n]:
        strategy.update(tick.price)

def time_one(strategy_factory, data, n, repeats=3):
    """
    Measures execution time using timeit.
    strategy_factory must return a NEW strategy each time.
    """
    stmt = lambda: run_strategy(strategy_factory(), data, n)
    times = timeit.repeat(stmt, repeat=repeats, number=1)
    return min(times)

def peak_memory_one(strategy_factory, data, n):
    """
    Measures peak memory (MiB) during strategy run.
    """
    def target():
        run_strategy(strategy_factory(), data, n)

    mem_samples = memory_usage(target, interval=0.01)
    return max(mem_samples)

def cprofile_one(strategy_factory, data, n, prof_out_path, top_n=15):
    """
    Runs cProfile and saves results to a .prof file.
    Also prints the top functions by total time.
    """
    profiler = cProfile.Profile()
    profiler.enable()
    run_strategy(strategy_factory(), data, n)
    profiler.disable()

    profiler.dump_stats(prof_out_path)

    stats = pstats.Stats(profiler).sort_stats("tottime")
    stats.print_stats(top_n)
