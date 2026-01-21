import timeit
import cProfile
import pstats
from memory_profiler import memory_usage
from line_profiler import LineProfiler
import sys

def run_strategy(strategy, data, n):
    """Runs update() for first n ticks."""
    for tick in data[:n]:
        strategy.update(tick.price)

def time_one(strategy_factory, data, n, repeats=3):
    """
    Measures execution time using timeit.
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

    mem_samples = memory_usage(target, interval=0.1, timeout=60)
    return max(mem_samples)

def cprofile_one(strategy_factory, data, n, prof_out_path, top_n=15):
    """
    Runs cProfile and saves results to a .prof file.

    """
    profiler = cProfile.Profile()
    profiler.enable()
    run_strategy(strategy_factory(), data, n)
    profiler.disable()

    profiler.dump_stats(prof_out_path)

    stats = pstats.Stats(profiler).sort_stats("tottime")
    stats.print_stats(top_n)

def line_profile_one(strategy_factory, data, n, out_path, method_name="update"):
    """
    """

    strategy = strategy_factory()

    method = getattr(strategy, method_name)

    profiler = LineProfiler()
    profiler.add_function(method)

    profiler.enable()

    for tick in data[:n]:
        strategy.update(tick.price)

    profiler.disable()

    with open(out_path, "w", encoding="utf-8") as f:
        old_stdout = sys.stdout
        sys.stdout = f
        profiler.print_stats()
        sys.stdout = old_stdout
