import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
normal_files = [
    "data/raw/normal_1.txt",
    "data/raw/normal_2.txt",
]

anamoly_files = [
    "data/raw/mem_spike.txt",
    "data/raw/cpu_spike.txt",
    "data/raw/mem_leak.txt",
]

METRIC = "rss"   
THRESHOLD_STD = 3

os.makedirs("plots", exist_ok=True)
normal_values = []

for file in normal_files:
    df = pd.read_csv(file, sep="\t")
    normal_values.extend(df[METRIC].values)

normal_values = np.array(normal_values)

baseline_mean = normal_values.mean()
baseline_std = normal_values.std()

upper_threshold = baseline_mean + THRESHOLD_STD * baseline_std

print("Baseline mean:", baseline_mean)
print("Baseline std:", baseline_std)
print("Upper threshold:", upper_threshold)

for file in anamoly_files:

    df = pd.read_csv(file, sep="\t")
    series = df[METRIC]

    anomalies = series > upper_threshold

    plt.figure()
    plt.plot(series.values)
    plt.axhline(upper_threshold)
    plt.scatter(
        np.where(anomalies)[0],
        series[anomalies],
    )

    name = file.split("/")[-1].replace(".txt","")
    plt.title(f"{name} - Baseline Detection")
    plt.xlabel("Time")
    plt.ylabel(METRIC)

    plt.savefig(f"plots/{name}_baseline.png")
    plt.close()

    print(f"{name}: {anomalies.sum()} anomalies detected")