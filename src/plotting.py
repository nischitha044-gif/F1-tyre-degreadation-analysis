# src/plotting.py
# Plotting utilities for per-stint visualizations
import matplotlib.pyplot as plt
import numpy as np

def plot_stint_with_rolling(st_df, window=3, highlight_dropoff=None):
    st_df = st_df.sort_values('lap')
    laps = st_df['lap']
    times = st_df['lapTime_seconds']
    rolling = times.rolling(window=window, center=True, min_periods=1).mean()

    plt.figure(figsize=(9,4))
    plt.plot(laps, times, marker='o', label='lap time', color='C0')
    plt.plot(laps, rolling, label=f'rolling mean (w={window})', color='C1', linewidth=2)
    if highlight_dropoff is not None:
        plt.axvline(highlight_dropoff, color='C3', linestyle='--', label='detected drop-off')
    plt.xlabel('Lap')
    plt.ylabel('Lap time (s)')
    plt.grid(True)
    plt.legend()
    plt.title(f'Stint {st_df["stint"].iloc[0]} (race {st_df["raceId"].iloc[0]} driver {st_df["driverId"].iloc[0]})')
    plt.show()