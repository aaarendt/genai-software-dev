"""Prepare the demo CSV for the coding-agent tutorial.

This script is NOT shown to the audience. Run it once before the tutorial to
produce ksea_2024.csv, which is what the demo notebook reads.

The generated data is designed to:
- Look like hourly weather observations for Seattle-Tacoma airport, 2024
- Have timestamps in UTC (no timezone metadata in the CSV)
- Have a diurnal signal that peaks around 22:00 UTC (~3 PM local, the real
  afternoon peak), so the seeded timezone bug in the notebook produces a
  visibly wrong "temperature by hour" plot that reads as ~11 PM peak
"""

import pandas as pd
import numpy as np

np.random.seed(42)

hours = pd.date_range('2024-01-01 00:00', '2024-12-31 23:00', freq='h', tz='UTC')

# seasonal signal: cold in Jan/Feb, warm in Jul/Aug
doy = hours.dayofyear.to_numpy()
seasonal = 9 + 11 * np.sin(2 * np.pi * (doy - 100) / 365.25)

# diurnal signal: peak at ~22:00 UTC = ~15:00 PST (3 PM, the real afternoon peak)
hod = hours.hour.to_numpy()
diurnal = 5 * np.sin(2 * np.pi * (hod - 16) / 24)

# noise
noise = np.random.normal(0, 1.8, len(hours))

temp = seasonal + diurnal + noise

df = pd.DataFrame({
    'timestamp': hours.tz_localize(None),  # strip tz — real weather CSVs usually don't carry it
    'temp_c': temp,
})

df.to_csv('ksea_2024.csv', index=False)
print(f'wrote ksea_2024.csv ({len(df)} rows)')