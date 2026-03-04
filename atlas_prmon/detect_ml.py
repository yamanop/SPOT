import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
WINDOW = 10
THRESHOLD = 3
FILES = {
    "normal_1": "data/raw/normal_1.txt",
    "normal_2": "data/raw/normal_2.txt",
    "mem_spike": "data/raw/mem_spike.txt",
    "cpu_spike": "data/raw/cpu_spike.txt",
    "mem_leak" : "data/raw/mem_leak.txt",
}

METRIC = "rss"  

os.makedirs("plots", exist_ok=True)

for name, path in FILES.items():
    df = pd.read_csv(path, sep="\t")
    series = df[METRIC]
    rolling_mean = series.rolling(WINDOW).mean()
    rolling_std = series.rolling(WINDOW).std()
    z_score = (series - rolling_mean) / rolling_std
    anomalies = np.abs(z_score) > THRESHOLD

    plt.figure()
    plt.plot(series.values)
    plt.scatter(
        np.where(anomalies)[0],
        series[anomalies],
    )
    plt.title(f"{name} - {METRIC} Anomaly Detection")
    plt.xlabel("Time (seconds)")
    plt.ylabel(METRIC)

    plt.savefig(f"plots/{name}_{METRIC}.png")
    plt.close()

    print(f"{name}: {anomalies.sum()} anomalies detected")