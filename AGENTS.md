# Plan: Refactor weather_analysis.ipynb into a Python module

## Overview
Extract reusable logic from the notebook into `scripts/weather.py` (a new module alongside the existing `scripts/build_notebook.py`). The notebook becomes a thin orchestration layer: import, call, display.

## Functions to extract

### `generate_synthetic_data(seed, output_path)`
- Docstring: "Generate a year of synthetic hourly SeaTac temperatures and save to CSV."
- Source: cell lines 16–43
- No type hints; parameters: `seed` (default 42), `output_path` (default `../data/ksea_2024.csv`)

### `load_and_clean(path)`
- Docstring: "Load the CSV at path, parse the timestamp column, and set it as the index."
- Source: cell lines 49–50 and 61–63

### `compute_daily_stats(df)`
- Docstring: "Resample hourly DataFrame to daily mean, max, and min temperature."
- Source: cell lines 77–78

### `compute_diurnal_pattern(df)`
- Docstring: "Return mean temperature grouped by hour of day across the full dataset."
- Source: cell lines 92–101

### `forecast_next_day_max(daily, window=7)`
- Docstring: "Forecast tomorrow's max temperature as the mean of the last `window` daily maxes."
- Source: cell lines 109–113

## What stays in the notebook
- Imports + `%matplotlib inline`
- Calls to module functions
- Exploratory display calls: `df.head()`, `df.describe()`
- All `plt.show()` plot calls (visual/interactive by nature)
- All markdown narrative cells (unchanged)

## Module location
`scripts/weather.py` — consistent with existing `scripts/build_notebook.py`

## Verification
1. `import scripts.weather` in a Python shell — no import errors
2. Re-run notebook top-to-bottom — all outputs match `weather_analysis_executed.ipynb`
3. `forecast_next_day_max` result matches the printed value in the executed notebook

## Decisions
- Keep plot rendering in the notebook (not in the module) — matplotlib calls are side-effectful and context-dependent
- `generate_synthetic_data` stays extractable even though it's demo scaffolding — makes the module independently runnable
- No new subdirectory (`src/`) needed given existing `scripts/` convention