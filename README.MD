# F1 Tyre Degradation Analysis

## Overview
This project analyzes tyre degradation patterns in Formula 1 races using historical lap time data.
This project is being built step by step as I learn GitHub and data analysis.

The goal is to understand how lap times increase as tyres wear and to identify potential pit stop windows.

## Objective
- Analyze lap time degradation across race stints
- Compare performance trends over laps
- Identify the lap where performance drop-off becomes significant

## Dataset
- Data source examples:
  - [Kaggle: Formula 1 Race Data 1950-2022](https://www.kaggle.com/datasets/ra5625/formula-1-race-data-1950-2022)
  - [FastF1 documentation & installation](https://theoehrly.github.io/Fast-F1/)
- Place processed CSV at `data/processed/lap_times.csv`
- Make sure any data you add follows the licensing terms of the source

## Project layout
- data/
  - raw/
  - processed/
- notebooks/
  - 01-exploration.ipynb (starter)
- src/
  - data_processing.py
  - analysis.py
  - plotting.py
- reports/
- README.MD

## How to run
1. Clone the repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Prepare data:
   - Place your processed lap times CSV at `data/processed/lap_times.csv`
   - Expected columns: `raceId, driverId, stint, lap, lapTime_seconds`
4. Run exploratory script or open notebooks:
   ```
   python notebooks/01-exploration.py
   ```
5. Run analysis:
   ```
   python start_analysis.py
   ```

## Success criteria examples
- Detect lap where lap time increases by >0.5s relative to local average
- Slope of lap time vs lap number > 0.15 s/lap
- Percentage of stints with positive, significant slope (p < 0.05)

## Status
Project in progress
