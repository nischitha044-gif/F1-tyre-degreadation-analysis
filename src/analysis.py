# src/analysis.py
# Per-stint degradation metrics and summary exports
import pandas as pd
import numpy as np
from scipy.stats import linregress

def compute_stint_metrics(df):
    """  
    For each raceId, driverId, stint compute:
      - slope (s/ lap)
      - intercept
      - r_value, p_value, stderr
      - mean_lap_time, std_lap_time
      - lap_of_max_delta (optional)
    Returns a DataFrame with one row per stint.
    """
    records = []
    grouped = df.groupby(['raceId','driverId','stint'])
    for (race, driver, stint), g in grouped:
        g = g.sort_values('lap')
        if g.shape[0] < 3:
            continue
        x = g['lap'].to_numpy()
        y = g['lapTime_seconds'].to_numpy()
        slope, intercept, r_value, p_value, stderr = linregress(x, y)
        mean_t = np.nanmean(y)
        std_t = np.nanstd(y)
        records.append({
            'raceId': int(race),
            'driverId': int(driver),
            'stint': int(stint),
            'n_laps': int(len(x)),
            'slope_s_per_lap': float(slope),
            'intercept': float(intercept),
            'r_value': float(r_value),
            'p_value': float(p_value),
            'stderr': float(stderr),
            'mean_lap_time': float(mean_t),
            'std_lap_time': float(std_t)
        })
    return pd.DataFrame.from_records(records)

def detect_drop_offs(df, window=3, threshold_sec=0.5):
    """
    For each stint compute rolling mean and detect first lap where lap time
    increases by more than threshold_sec relative to previous window mean.
    Returns a DataFrame of detected drop-offs (raceId, driverId, stint, lap, delta)
    """
    out_rows = []
    grouped = df.groupby(['raceId','driverId','stint'])
    for (race, driver, stint), g in grouped:
        g = g.sort_values('lap').reset_index(drop=True)
        if g.shape[0] < window+1:
            continue
        g['rolling'] = g['lapTime_seconds'].rolling(window=window, min_periods=1).mean()
        g['delta'] = g['lapTime_seconds'] - g['rolling'].shift(1)
        # find first lap where delta > threshold
        fail = g[g['delta'] > threshold_sec]
        if not fail.empty:
            first = fail.iloc[0]
            out_rows.append({
                'raceId': int(race),
                'driverId': int(driver),
                'stint': int(stint),
                'lap': int(first['lap']),
                'delta': float(first['delta'])
            })
    return pd.DataFrame.from_records(out_rows)
