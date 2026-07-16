"""Build the messy demo notebook with a seeded timezone bug.

Design intent:
- Feels like an exploratory notebook a researcher would actually write
- No functions, no docstrings, some hardcoded values, some reused variable names
- One coherent analysis story: load hourly weather -> clean -> aggregate to daily
  -> look at diurnal patterns -> naive forecast
- Seeded bug: timestamps are UTC, but the notebook treats them as if local time.
  Daily aggregations bucket at UTC midnight (which is 4-5 PM local for Seattle),
  and the "hour of day" analysis shows a peak at hour 22 UTC — which the
  researcher will initially misread as "10 PM peak" until the timezone is traced.

The bug survives an agent refactor faithfully because the refactor preserves
the pandas operations verbatim. Summary statistics (annual mean, min, max)
are unaffected. The bug becomes obvious only when the "temperature by hour"
plot is inspected in Act 3.
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# ---- Cell 1: title (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""# Seattle weather — quick look

Just poking at some hourly temperature data for SeaTac.
Want to see the seasonal + daily pattern and try a naive next-day forecast.
"""))

# ---- Cell 2: imports (code) ----
cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline"""))

# ---- Cell 3: generate synthetic data (code) ----
# Deliberately kept in the notebook so the demo is self-contained. In a real
# analysis this would be an external CSV; the presenter can explain that.
cells.append(nbf.v4.new_code_cell("""# generate a year of hourly data for SeaTac
# (in a real analysis this would be a CSV from NOAA, but this makes the
# notebook self-contained for the demo)

np.random.seed(42)

hours = pd.date_range('2024-01-01 00:00', '2024-12-31 23:00', freq='h', tz='UTC')

# seasonal signal: cold in Jan/Feb, warm in Jul/Aug
doy = hours.dayofyear.to_numpy()
seasonal = 9 + 11 * np.sin(2 * np.pi * (doy - 100) / 365.25)

# diurnal signal: peak at ~22:00 UTC = ~15:00 PST (3 PM, the realistic afternoon peak)
hod = hours.hour.to_numpy()
diurnal = 5 * np.sin(2 * np.pi * (hod - 16) / 24)

# noise
noise = np.random.normal(0, 1.8, len(hours))

temp = seasonal + diurnal + noise

df = pd.DataFrame({
    'timestamp': hours.tz_localize(None),  # strip tz — data files usually don't carry it
    'temp_c': temp,
})

df.to_csv('ksea_2024.csv', index=False)
print(f'wrote {len(df)} rows')"""))

# ---- Cell 4: load (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Load the data"""))

# ---- Cell 5: read csv (code) ----
cells.append(nbf.v4.new_code_cell("""df = pd.read_csv('ksea_2024.csv')
df.head()"""))

# ---- Cell 6: describe (code) ----
cells.append(nbf.v4.new_code_cell("""df.describe()"""))

# ---- Cell 7: cleaning (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Clean up

Convert the timestamp column and set as index."""))

# ---- Cell 8: parse and set index (code) ----
# NOTE: no timezone handling. This is where the bug lives — timestamps are
# UTC but nothing here says so, and downstream code treats them as local.
cells.append(nbf.v4.new_code_cell("""df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')
df.head()"""))

# ---- Cell 9: quick plot (code) ----
cells.append(nbf.v4.new_code_cell("""df['temp_c'].plot(figsize=(12, 3))
plt.ylabel('temperature (C)')
plt.title('Hourly temperature, 2024')
plt.show()"""))

# ---- Cell 10: daily agg (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Daily aggregation

Get daily mean/min/max."""))

# ---- Cell 11: resample (code) ----
# Bug propagates: .resample('D') buckets at UTC midnight. For SeaTac (PST/PDT)
# each "daily bucket" actually runs from ~4-5 PM local yesterday to ~4-5 PM local today.
cells.append(nbf.v4.new_code_cell("""daily = df['temp_c'].resample('D').agg(['mean', 'max', 'min'])
daily.head(10)"""))

# ---- Cell 12: daily plot (code) ----
cells.append(nbf.v4.new_code_cell("""daily[['max', 'mean', 'min']].plot(figsize=(12, 4))
plt.ylabel('temperature (C)')
plt.title('Daily temperature, 2024')
plt.show()"""))

# ---- Cell 13: diurnal (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Diurnal pattern

What does a typical day look like?"""))

# ---- Cell 14: hour of day (code) ----
# This is the plot that reveals the bug in Act 3. The peak appears at hour 22,
# which "looks wrong" for a temperature peak. The fix is to convert to local time
# before extracting the hour.
cells.append(nbf.v4.new_code_cell("""df['hour'] = df.index.hour
by_hour = df.groupby('hour')['temp_c'].mean()
by_hour.plot(kind='bar', figsize=(10, 3))
plt.ylabel('mean temp (C)')
plt.xlabel('hour of day')
plt.title('Average temperature by hour of day')
plt.show()

print(f'peak hour: {by_hour.idxmax()}')
print(f'coldest hour: {by_hour.idxmin()}')"""))

# ---- Cell 15: forecast (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Naive forecast

Predict tomorrow's max as the mean of the last 7 daily maxes."""))

# ---- Cell 16: forecast (code) ----
cells.append(nbf.v4.new_code_cell("""last_7 = daily['max'].iloc[-7:]
forecast = last_7.mean()
print(f'last 7 daily maxes:')
print(last_7)
print(f'\\nforecast for next day max: {forecast:.1f} C')"""))

nb['cells'] = cells

with open('/home/claude/demo/weather_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print('notebook written')
