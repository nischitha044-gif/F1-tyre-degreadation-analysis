# notebooks/01-exploration.py
# Quick exploratory script (can be run as a notebook or script)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Update this path if your processed CSV is elsewhere
CSV_PATH = "data/processed/lap_times.csv"

def load_data(path=CSV_PATH):
    df = pd.read_csv(path)
    return df

def overview(df, n=5):
    print("Head:")
    print(df.head(n))
    print("\nInfo:")
    print(df.info())
    print("\nMissing values per column:")
    print(df.isnull().sum())

def plot_lap_time_distribution(df):
    plt.figure(figsize=(8,4))
    plt.hist(df['lapTime_seconds'].dropna(), bins=40, color='C0', alpha=0.8)
    plt.xlabel('Lap time (s)')
    plt.ylabel('Count')
    plt.title('Lap Time Distribution')
    plt.grid(True)
    plt.show()

def plot_example_stint(df, race=None, driver=None, stint=1):
    if race is None:
        race = df['raceId'].iloc[0]
    if driver is None:
        driver = df['driverId'].iloc[0]

    st = df[(df.raceId == race) & (df.driverId == driver) & (df.stint == stint)].copy()
    if st.empty:
        print("No data for requested race/driver/stint")
        return
    st = st.sort_values('lap')
    plt.figure(figsize=(8,4))
    plt.plot(st['lap'], st['lapTime_seconds'], marker='o', label='lap time')
    plt.xlabel('Lap')
    plt.ylabel('Lap time (s)')
    plt.title(f'Ride {race} Driver {driver} Stint {stint}')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = load_data()
    overview(df)
    plot_lap_time_distribution(df)
    plot_example_stint(df)