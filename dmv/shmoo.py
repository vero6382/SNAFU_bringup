import numpy as np

t_freqs = [20000000, 20000000, 20000000, 30000000, 30000000, 40000000, 40000000, 40000000, 50000000, 50000000, 60000000, 60000000, 60000000, 70000000, 70000000, 70000000, 80000000, 80000000]

MHz = 1000000

failed_configs = []

ind = 0
for i in np.arange(0.60, 0.96, 0.02):
    volt = round(i, 2)
    max_freq = t_freqs[ind] // MHz
    ind += 1
    
    for f in range(max_freq + 10, 150, 10):
        print((f, volt))
