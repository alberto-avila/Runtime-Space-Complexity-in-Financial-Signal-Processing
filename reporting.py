import matplotlib.pyplot as plt

def plot_runtime_vs_input_size(sizes, naive_times, windowed_times):
    """
    """
    if not (len(sizes) == len(naive_times) == len(windowed_times)):
        raise ValueError("sizes, naive_times, and windowed_times must have the same length.")

    plt.figure()
    plt.plot(sizes, naive_times, marker="o", label="Naive Moving Average")
    plt.plot(sizes, windowed_times, marker="x", label="Windowed Moving Average")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size (ticks)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Input Size")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_memory_vs_input_size(sizes, naive_memory_mib, windowed_memory_mib):
    """
    """
    if not (len(sizes) == len(naive_memory_mib) == len(windowed_memory_mib)):
        raise ValueError("sizes, naive_memory_mib, and windowed_memory_mib must have the same length.")

    plt.figure()
    plt.plot(sizes, naive_memory_mib, marker="o", label="Naive Moving Average")
    plt.plot(sizes, windowed_memory_mib, marker="x", label="Windowed Moving Average")

    plt.xscale("log")
    plt.xlabel("Input size (ticks)")
    plt.ylabel("Peak memory (MiB)")
    plt.title("Peak Memory vs Input Size")
    plt.legend()
    plt.tight_layout()
    plt.show()
