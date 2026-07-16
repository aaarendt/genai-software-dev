# Demo notebook: `weather_analysis.ipynb`

The intentionally messy exploratory notebook used as the starting artifact for
the "Working With a Coding Agent" tutorial.

## What the notebook does

A researcher pokes at hourly temperature data for Seattle-Tacoma (2024).
Loads a CSV, cleans it, resamples to daily, looks at diurnal patterns, and
produces a naive next-day forecast. Written the way exploratory notebooks
actually get written: no functions, some copy-paste, hardcoded values,
minimal comments.

## The seeded bug

**Timestamps in the CSV are UTC, but the notebook treats them as if they were
local time.**

The bug is planted in two places:
1. Cell that parses the timestamp: no timezone information is attached, and no
   conversion to local time is done.
2. Cell that groups temperatures by "hour of day": uses `df.index.hour` on
   UTC-labeled timestamps, so the "hour" column is actually UTC hour.

### What the bug does and doesn't affect

| Quantity | Affected? |
|---|---|
| Annual mean temperature | No — averaging over a full year is timezone-invariant |
| Daily min/max/mean values | Barely — day boundaries are shifted, but values look plausible |
| Hourly diurnal pattern | **Yes — dramatically.** Peak shows at "hour 23", coldest at "hour 10" |
| Naive forecast output | Barely — value is plausible |

This is deliberate. Summary statistics give no signal that anything is wrong.
The bug only reveals itself when the "temperature by hour" plot is inspected,
and the peak lands at 23:00 (which reads as "11 PM" — obviously wrong for a
temperature peak, which should be mid-afternoon).

### The fix the agent will land on

Convert to local time before extracting the hour. One-line addition after
`pd.to_datetime`:

```python
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')
```

The AGENTS.md line the presenter writes live in Act 2 —
*"timestamps are UTC unless stated otherwise"* — is what makes this bug
traceable rather than mysterious in the demo.

## The intended demo arc

**Act 2 — Phase 1** (ask for a plan): agent reads the notebook and proposes a
refactor plan. Presenter edits the plan visibly.

**Act 2 — Phase 2** (extract functions): agent extracts the cleaning and
aggregation logic into a `.py` module. Bug is preserved faithfully because
the pandas operations are moved verbatim. Presenter commits, shows the diff.

**Act 3 — Phase 3** (the bug reveal): presenter runs the refactored code and
compares against the original notebook. Summary statistics match. Then
presenter surfaces the "temperature by hour" plot. Peak at hour 23. Trace it
together. Agent explains, proposes fix, presenter accepts.

## Files

- `weather_analysis.ipynb` — the clean starting artifact for the demo
- `weather_analysis_executed.ipynb` — same notebook with outputs, for the
  presenter to reference when rehearsing
- `ksea_2024.csv` — the synthetic dataset the notebook generates on first run.
  Included so the presenter can skip the generation cell if desired.
- `build_notebook.py` — the script that produced `weather_analysis.ipynb`.
  Edit and re-run this to change the notebook or bug behavior.

## Rehearsal checklist

- [ ] Run the notebook top-to-bottom on the demo machine to confirm it works
- [ ] Confirm the "by hour" plot shows the inverted pattern (peak at ~22-23)
- [ ] Confirm annual mean is ~9.0 C (the bug-invariant sanity number)
- [ ] Do one full agent refactor pass in rehearsal and record it as fallback video
- [ ] Verify AGENTS.md phrasing you plan to write live actually gets referenced
      by the agent when it proposes the fix in Act 3

## Notes on regenerating

`build_notebook.py` uses `nbformat` to construct the notebook programmatically.
This is more reliable than editing the `.ipynb` JSON directly.

If you want to tune the bug:
- The phase constant in the diurnal signal (`hod - 16`) controls where the
  UTC peak lands. Currently peaks at hour 22 UTC (~3 PM PST).
- Increase noise stddev (currently 1.8) to make the pattern less crisp.
- Change the seed (42) if you want different specific values but the same shape.
