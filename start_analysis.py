# start_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Minimal starter script that uses src/analysis.py functions if available
CSV_PATH = "data/processed/lap_times.csv"

def simple_stint_trend(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    # pick first (race,driver,stint) available
    group = df.groupby(['raceId','driverId','stint']).first().reset_index()
    race, driver, stint = group.loc[0, ['raceId','driverId','stint']]
    st = df[(df.raceId == race) & (df.driverId == driver) & (df.stint == stint)].sort_values('lap')
    if st.empty:
        print("No example stint found.")
        return
    x = st['lap'].to_numpy()
    y = st['lapTime_seconds'].to_numpy()
    slope, intercept, r_value, p_value, stderr = linregress(x, y)
    print(f"Slope: {slope:.4f} s/lap  R^2: {r_value**2:.3f}  p={p_value:.4g}")
    st['rolling'] = st['lapTime_seconds'].rolling(window=3, center=True).mean()
    plt.figure(figsize=(8,4))
    plt.plot(st['lap'], st['lapTime_seconds'], marker='o', label='lap time')
    plt.plot(st['lap'], st['rolling'], label='rolling mean', linewidth=2)
    plt.xlabel('lap')
    plt.ylabel('lap time (s)')
    plt.title(f'Race {race} Driver {driver} Stint {stint}')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    simple_stint_trend()