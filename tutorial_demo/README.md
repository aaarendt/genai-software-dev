# Demo notebook: `weather_analysis.ipynb`

The intentionally messy exploratory notebook used as the starting artifact for
the "Working With a Coding Agent" tutorial.

## What the audience sees

A notebook that opens with `df = pd.read_csv('ksea_2024.csv')` and works with
hourly temperature data for Seattle-Tacoma, 2024. Loads a CSV, cleans it,
resamples to daily, looks at diurnal patterns, and produces a naive next-day
forecast. Written the way exploratory notebooks actually get written — no
functions, some copy-paste, hardcoded values, minimal comments.

## What the presenter uses

Three files in the demo directory:

- `prepare_data.py` — generates `ksea_2024.csv`. Run once before the tutorial.
  Not shown to the audience; not part of the demo.
- `weather_analysis.ipynb` — the starting artifact of the demo.
- `ksea_2024.csv` — the "observed" data the notebook reads.

## The seeded bug

**Timestamps in the CSV are UTC, but the notebook treats them as if they were
local time.**

The bug lives in the notebook code, not the data. NOAA-style weather data
comes in UTC as a matter of convention; the CSV mirrors this. The notebook
never converts to local time, so:

- `df.index.hour` extracts UTC hours
- `groupby('hour')` produces a "temperature by hour" plot that peaks at
  hour 23 (which reads as "11 PM") and troughs at hour 10 ("10 AM")
- Annual mean and daily min/max/mean are unaffected

Summary statistics give no signal. The bug reveals itself only when the
diurnal profile plot is inspected.

## The intended demo arc

**Act 2 — Phase 1** (ask for a plan): agent reads the notebook and proposes a
refactor plan into a `weather.py` module. Presenter edits the plan visibly —
removing type hints the agent added uninvited, adding docstrings.

**Act 2 — Phase 2** (extract functions): after a live AGENTS.md write that
includes "timestamps are UTC unless stated otherwise", agent extracts cleaning
and aggregation into `weather.py`. Bug is preserved faithfully because the
pandas operations are moved verbatim. The refactor also *localizes* the bug
inside `load_and_clean`, which pays off in Act 3. Presenter commits, reviews
the diff.

**Act 3 — Phase 3** (the bug reveal): presenter runs the refactored code and
compares against the original notebook — summary statistics match. Then
surfaces the diurnal profile plot. Peak at hour 23. Trace with the agent;
identify the timezone issue; apply a one-line fix inside `load_and_clean`
(add `.dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')` after the
`pd.to_datetime` call). Re-run — peak now lands at hour 15, correctly.

## Rehearsal checklist

- [ ] Run `prepare_data.py` on the demo machine, confirm `ksea_2024.csv` exists
- [ ] Run the notebook top-to-bottom to confirm it works
- [ ] Confirm the "by hour" plot peaks at hour 23 and troughs at hour 10
- [ ] Confirm annual mean is ~9.0 C (bug-invariant sanity number)
- [ ] Do one full agent refactor pass in rehearsal; record it as fallback video
- [ ] Verify the AGENTS.md phrasing you plan to write live actually gets
      referenced by the agent when it proposes the fix in Act 3

## Notes on regenerating

`build_notebook.py` uses `nbformat` to construct the notebook programmatically.
Edit it and re-run to change the notebook. `prepare_data.py` produces the CSV;
edit it if you want to tune the bug amplitude:

- Change the phase in the diurnal signal (`hod - 16`) to shift where the UTC
  peak lands. Current phase peaks at hour 22-23 UTC (~3 PM local).
- Increase noise stddev (currently 1.8) to make the pattern less crisp.
- Change the seed (42) for different specific values, same shape.