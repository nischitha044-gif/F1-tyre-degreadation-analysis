# src/data_processing.py
# Utilities for loading raw data and producing a cleaned lap_times.csv
import pandas as pd
import numpy as np
from pathlib import Path

def load_raw_csv(path):
    return pd.read_csv(path)

def standardize_columns(df):
    # Expected output columns: raceId, driverId, stint, lap, lapTime_seconds
    col_map = {}
    # Try common variants
    if 'lap_time' in df.columns:
        col_map['lap_time'] = 'lapTime_seconds'
    if 'lapTime' in df.columns:
        col_map['lapTime'] = 'lapTime_seconds'
    if 'lap_time_seconds' in df.columns:
        col_map['lap_time_seconds'] = 'lapTime_seconds'
    # apply mapping
    df = df.rename(columns=col_map)
    # Convert times to seconds if needed (handles mm:ss.xxx or pandas timedelta)
    if df['lapTime_seconds'].dtype == object:
        df['lapTime_seconds'] = df['lapTime_seconds'].apply(parse_time_to_seconds)
    return df

def parse_time_to_seconds(t):
    # Naive parser: accepts "m:ss.xxx" or "mm:ss.xxx" or seconds as float string
    if pd.isna(t):
        return np.nan
    if isinstance(t, (float, int)):
        return float(t)
    s = str(t)
    if ':' in s:
        try:
            parts = s.split(':')
            mins = float(parts[0])
            secs = float(parts[1])
            return mins*60 + secs
        except Exception:
            return np.nan
    try:
        return float(s)
    except Exception:
        return np.nan

def clean_and_save(df, out_path="data/processed/lap_times.csv"):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # Basic cleaning
    df = standardize_columns(df)
    # Ensure columns exist
    required = ['raceId', 'driverId', 'stint', 'lap', 'lapTime_seconds']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    # Drop fully empty rows
    df = df.dropna(subset=['raceId', 'driverId', 'lap', 'lapTime_seconds'])
    # cast types
    df['raceId'] = df['raceId'].astype(int)
    df['driverId'] = df['driverId'].astype(int)
    df['stint'] = df['stint'].astype(int)
    df['lap'] = df['lap'].astype(int)
    df['lapTime_seconds'] = df['lapTime_seconds'].astype(float)
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned data to {out_path}")
    return df
