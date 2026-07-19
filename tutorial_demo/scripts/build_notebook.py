"""Build the messy demo notebook.

The notebook opens with `pd.read_csv('ksea_2024.csv')` as if reading real
observations. The CSV is produced by prepare_data.py, which the audience
does not see. The seeded timezone bug lives in the notebook code (treating
UTC timestamps as if local), not in the data.
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

# ---- Cell 3: load (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Load the data"""))

# ---- Cell 4: read csv (code) ----
cells.append(nbf.v4.new_code_cell("""df = pd.read_csv('../data/ksea_2024.csv')
df.head()"""))

# ---- Cell 5: describe (code) ----
cells.append(nbf.v4.new_code_cell("""df.describe()"""))

# ---- Cell 6: cleaning (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Clean up

Convert the timestamp column and set as index."""))

# ---- Cell 7: parse and set index (code) ----
# NOTE: no timezone handling. This is where the bug lives — timestamps are
# UTC but nothing here says so, and downstream code treats them as local.
cells.append(nbf.v4.new_code_cell("""df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')
df.head()"""))

# ---- Cell 8: quick plot (code) ----
cells.append(nbf.v4.new_code_cell("""df['temp_c'].plot(figsize=(12, 3))
plt.ylabel('temperature (C)')
plt.title('Hourly temperature, 2024')
plt.show()"""))

# ---- Cell 9: daily agg (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Daily aggregation

Get daily mean/min/max."""))

# ---- Cell 10: resample (code) ----
cells.append(nbf.v4.new_code_cell("""daily = df['temp_c'].resample('D').agg(['mean', 'max', 'min'])
daily.head(10)"""))

# ---- Cell 11: daily plot (code) ----
cells.append(nbf.v4.new_code_cell("""daily[['max', 'mean', 'min']].plot(figsize=(12, 4))
plt.ylabel('temperature (C)')
plt.title('Daily temperature, 2024')
plt.show()"""))

# ---- Cell 12: diurnal (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Diurnal pattern

What does a typical day look like?"""))

# ---- Cell 13: hour of day (code) ----
# This is the plot that reveals the bug in Act 3.
cells.append(nbf.v4.new_code_cell("""df['hour'] = df.index.hour
by_hour = df.groupby('hour')['temp_c'].mean()
by_hour.plot(kind='bar', figsize=(10, 3))
plt.ylabel('mean temp (C)')
plt.xlabel('hour of day')
plt.title('Average temperature by hour of day')
plt.show()

print(f'peak hour: {by_hour.idxmax()}')
print(f'coldest hour: {by_hour.idxmin()}')"""))

# ---- Cell 14: forecast (markdown) ----
cells.append(nbf.v4.new_markdown_cell("""## Naive forecast

Predict tomorrow's max as the mean of the last 7 daily maxes."""))

# ---- Cell 15: forecast (code) ----
cells.append(nbf.v4.new_code_cell("""last_7 = daily['max'].iloc[-7:]
forecast = last_7.mean()
print(f'last 7 daily maxes:')
print(last_7)
print(f'\\nforecast for next day max: {forecast:.1f} C')"""))

nb['cells'] = cells

with open('ipynb/weather_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print(f'notebook written ({len(cells)} cells)')