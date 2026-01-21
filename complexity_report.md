# Complexity Report

The data loader reads the CSV file line by line making each row into a MarketDataPoint, which is stored in a list. Since one object is created and stored per row, the space complexity is O(n), where n is the number of rows in the dataset, in this case 100,000.

The NaiveMovingAverageStrategy recomputes the average price on every update by summing all historical prices seen so far, so each update has O(m) complexity, with m being the prices loaded up to that point. Over n total data points, this leads to a complexity of O(n²). The strategy stores all historical prices and one signal per tick, resulting in O(n) space complexity.

The WindowedMovingAverageStrategy maintains a fixed-size window of the last k prices and updates the average incrementally using a running sum. Each update performs only constant-time operations, giving O(1) time per update and O(n) total runtime over n ticks. This strategy also has O(n) space complexity.

The runtime graphs show that at small input sizes, the naive and windowed strategies perform similarly. As the input size increases to 10k and 100k ticks, the naive strategy’s runtime grows much faster. In contrast, the windowed strategy doesn't increase as much with the larger input sizes.

img width="640" height="480" alt="Runtime Plot" src="https://github.com/user-attachments/assets/6b46a845-44d6-4f26-bfe6-f902858f3c41" />


The memory usage graphs show increasing memory consumption for both strategies as input size grows. This is expected because both implementations store one signal per tick, which dominates memory usage at scale. While the windowed strategy has O(k) algorithmic memory for the moving average itself, the empirical measurements reflect total process memory, including auxiliary storage and profiling overhead. This highlights the difference between theoretical algorithmic complexity and observed system-level memory usage.

<img width="640" height="480" alt="Memory Usage Plot" src="https://github.com/user-attachments/assets/bac7f959-c188-4801-aa7a-360af7401006" />

The BetterMovingAverageStrategy calculates the same moving average as the naive strategy, but does so by saving a running sum and a count of observations. This avoids recomputing all prices every single time. As a result, we have O(n) total runtime. Compared to the naive approach, this strategy is more efficient in both time and space. 

Line Profilers:

Naive 1K
Timer unit: 1e-07 s

Total time: 0.0044687 s
File: strategies.py
Function: NaiveMovingAverageStrategy.update at line 13

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    13                                               def update(self, price):
    14      1000       3770.0      3.8      8.4          self.prices.append(price)
    15                                                   # Space grows by one element per call → O(n) total.
    16                                           
    17      1000      30882.0     30.9     69.1          avg_price = sum(self.prices) / len(self.prices)
    18                                                   # sum(self.prices) iterates over all stored prices.
    19                                                   # Time complexity per update: O(n).
    20                                                   # len(self.prices) and division are O(1).
    21                                           
    22      1000       3107.0      3.1      7.0          if price > avg_price:
    23        35        134.0      3.8      0.3              self.signals.append("BUY")
    24       965       3154.0      3.3      7.1          elif price < avg_price:
    25       964       3618.0      3.8      8.1              self.signals.append("SELL")
    26                                                   else:
    27         1         22.0     22.0      0.0              self.signals.append("HOLD")
    28                                           
    29                                                   # Overall per-update time complexity: O(n).
    30                                                   # Total time complexity over n ticks: O(n^2).


    Naive 10k
    Timer unit: 1e-07 s

Total time: 0.287758 s
File: strategies.py
Function: NaiveMovingAverageStrategy.update at line 13

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    13                                               def update(self, price):
    14     10000      38103.0      3.8      1.3          self.prices.append(price)
    15                                                   # Space grows by one element per call → O(n) total.
    16                                           
    17     10000    2724477.0    272.4     94.7          avg_price = sum(self.prices) / len(self.prices)
    18                                                   # sum(self.prices) iterates over all stored prices.
    19                                                   # Time complexity per update: O(n).
    20                                                   # len(self.prices) and division are O(1).
    21                                           
    22     10000      36449.0      3.6      1.3          if price > avg_price:
    23        35        157.0      4.5      0.0              self.signals.append("BUY")
    24      9965      35515.0      3.6      1.2          elif price < avg_price:
    25      9964      42856.0      4.3      1.5              self.signals.append("SELL")
    26                                                   else:
    27         1         24.0     24.0      0.0              self.signals.append("HOLD")
    28                                           
    29                                                   # Overall per-update time complexity: O(n).
    30                                                   # Total time complexity over n ticks: O(n^2).


    Naive 100k
    Timer unit: 1e-07 s

Total time: 24.376 s
File: strategies.py
Function: NaiveMovingAverageStrategy.update at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                               def update(self, price):
    10    100000     343302.0      3.4      0.1          self.prices.append(price)
    11                                           
    12                                                   # recompute average from scratch
    13    100000  242290397.0   2422.9     99.4          avg_price = sum(self.prices) / len(self.prices)
    14                                           
    15    100000     384839.0      3.8      0.2          if price > avg_price:
    16        35        128.0      3.7      0.0              self.signals.append("BUY")
    17     99965     324431.0      3.2      0.1          elif price < avg_price:
    18     99964     416387.0      4.2      0.2              self.signals.append("SELL")
    19                                                   else:
    20         1         21.0     21.0      0.0              self.signals.append("HOLD")



    Window 1k
    Timer unit: 1e-07 s

Total time: 0.0031716 s
File: strategies.py
Function: WindowedMovingAverageStrategy.update at line 60

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    60                                               def update(self, price):
    61      1000       3351.0      3.4     10.6          self.prices.append(price)
    62                                                   # deque append is O(1).
    63      1000       3542.0      3.5     11.2          self.running_sum += price
    64                                           
    65      1000       3496.0      3.5     11.0          if len(self.prices) > self.window:
    66                                                   # len(self.prices) is O(1).
    67       990       3948.0      4.0     12.4              removed = self.prices.popleft()
    68                                                       # deque popleft is O(1).
    69       990       3365.0      3.4     10.6              self.running_sum -= removed
    70                                           
    71      1000       3793.0      3.8     12.0          avg_price = self.running_sum / len(self.prices)
    72                                                   # Average computation uses running_sum and len(...) → O(1).
    73                                           
    74      1000       3382.0      3.4     10.7          if price > avg_price:
    75       104        441.0      4.2      1.4              self.signals.append("BUY")
    76                                                       # Append is O(1).
    77       896       2898.0      3.2      9.1          elif price < avg_price:
    78       153        584.0      3.8      1.8              self.signals.append("SELL")
    79                                                       # Append is O(1).
    80                                                   else:
    81       743       2916.0      3.9      9.2              self.signals.append("HOLD")
    82                                                       # Append is O(1).


    Window 10k
    Timer unit: 1e-07 s

Total time: 0.0326007 s
File: strategies.py
Function: WindowedMovingAverageStrategy.update at line 60

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    60                                               def update(self, price):
    61     10000      34516.0      3.5     10.6          self.prices.append(price)
    62                                                   # deque append is O(1).
    63     10000      33205.0      3.3     10.2          self.running_sum += price
    64                                           
    65     10000      34773.0      3.5     10.7          if len(self.prices) > self.window:
    66                                                   # len(self.prices) is O(1).
    67      9990      42811.0      4.3     13.1              removed = self.prices.popleft()
    68                                                       # deque popleft is O(1).
    69      9990      34160.0      3.4     10.5              self.running_sum -= removed
    70                                           
    71     10000      37173.0      3.7     11.4          avg_price = self.running_sum / len(self.prices)
    72                                                   # Average computation uses running_sum and len(...) → O(1).
    73                                           
    74     10000      34900.0      3.5     10.7          if price > avg_price:
    75       104        392.0      3.8      0.1              self.signals.append("BUY")
    76                                                       # Append is O(1).
    77      9896      32367.0      3.3      9.9          elif price < avg_price:
    78       153        659.0      4.3      0.2              self.signals.append("SELL")
    79                                                       # Append is O(1).
    80                                                   else:
    81      9743      41051.0      4.2     12.6              self.signals.append("HOLD")
    82                                                       # Append is O(1).



    Window 100k
    Timer unit: 1e-07 s

Total time: 0.30083 s
File: strategies.py
Function: WindowedMovingAverageStrategy.update at line 38

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    38                                               def update(self, price):
    39    100000     335183.0      3.4     11.1          self.prices.append(price)
    40    100000     317668.0      3.2     10.6          self.running_sum += price
    41                                           
    42    100000     328792.0      3.3     10.9          if len(self.prices) > self.window:
    43     99990     321134.0      3.2     10.7              removed = self.prices.popleft()
    44     99990     347457.0      3.5     11.5              self.running_sum -= removed
    45                                           
    46    100000     354486.0      3.5     11.8          avg_price = self.running_sum / len(self.prices)
    47                                           
    48    100000     309103.0      3.1     10.3          if price > avg_price:
    49       104        408.0      3.9      0.0              self.signals.append("BUY")
    50     99896     309814.0      3.1     10.3          elif price < avg_price:
    51       153        566.0      3.7      0.0              self.signals.append("SELL")
    52                                                   else:
    53     99743     383692.0      3.8     12.8              self.signals.append("HOLD")
