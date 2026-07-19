# Run Sheet

**60 minutes • 16 slides • one live demo • toggling between slides and notebook**

Screen legend: **[S]** slides on screen • **[N]** notebook/agent on screen • **↔** switch

---

## Act 1 — Overview *(0:00–0:15)*

**0:00** **[S]** • **01 Title** — Welcome. Introduce Don: Principal RSE, SSEC at UW.

**0:00:30** **[S]** • **02 Opening** — Name tension: excitement + concerns. Landscape shifts fast, so we demo rather than lecture.

**0:02** **[S]** • **03 Frame** — Agent is a coworker. *We have the final say.* Preview: 10 min overview, then demo, then trust.

**0:02:30** **[S]** • **04 Chat vs. agent** — Same LLM, different harness. Don't rush this — it's the key distinction.

**0:04:30** **[S]** • **05 Six pieces** — LLM, tools, loop, memory, MCP, skills. Every tool has these; switching is config.

**0:07** **[S]** • **06 Trained vs. prompt** — You can only change one side. Everything next lives in the prompt side.

**0:12** **[S ↔ N]** • **07 Demo setup** — *Switch to notebook.* Walk the messy notebook briefly. Define "refactor." State the three phases: plan, extract, verify.

## Act 2 — Working with the agent *(0:15–0:35)*

**0:15** **[S]** • **08 Ask for a plan (flowchart)** — Walk the flowchart. Confirm ask/plan mode on screen. *Switch to N.* **Send Prompt 1.** While it works: agent reads the whole notebook; it didn't ask clarifying questions. When plan returns: **point at type hints**, name scope creep. **Send Prompt 2.**

**0:22** **[S]** • **09 Four surfaces** — Preamble: "Everything the agent does is shaped by context." Name all four, use AGENTS.md seriously today.

**0:24** **[S ↔ N]** • **10 AGENTS.md live** — *Switch to editor.* Type the file live (see page 2). Point at UTC line — domain knowledge you bring. Point at "no type hints" line — grounded in what just happened. Run `git add` and `git commit`.

**0:28** **[N]** • **Demo Phase 2** — *Switch modes on screen* (ask → agent). Explain: mode is a physical gate. **Send Prompt 3.** While it works: git as safety net, "save point in a video game." When done: **do not run yet.** Show diff first. Say: *the chat is a claim, the diff is evidence.* Then run cells. Same numbers as before. Commit.

**0:34** **[S]** • **11 Act 2 recap** — Consolidate. Let it breathe. Bridge: *the code runs, but is it correct?*

## Act 3 — The bug *(0:36–0:52)*

**0:36** **[N]** • **Demo Phase 3 — bug reveal** — *Switch to notebook.* Open the by-hour plot. **Wait.** Ask: *what do you see?* Name it if nobody does: peak at hour 23, trough at 10 — clearly wrong for Seattle. Summary stats didn't catch this. **Send Prompt 4** (explain, don't fix). Agent identifies UTC/local issue. Callback to AGENTS.md line. **Send Prompt 5** (apply fix). Review diff. Re-run — peak now at 15:00. Commit.

**0:44** **[S]** • **12 Bug consolidation** — *Advance after a beat, not instantly.* Walk the four bullets. Last bullet bridges to 13.

**0:46** **[S]** • **13 Plausible code** — Widen the lens: *"that wasn't a bug about weather data. It was a general pattern."* Verification is the researcher's responsibility. Let it sit.

**0:49** **[S]** • **14 Two habits** — Read the diff. Push back is allowed. Honest scope note: more advanced patterns on the handout.

**0:50:30** **[S]** • **15 Reproducibility** — Tension is real. Resolution: process isn't reproducible, artifacts are. `git log docs/` reads like a lab notebook. Land on: *conversation is scaffolding, artifact is the science.*

## Close *(0:53–1:00)*

**0:53** **[S]** • **16 Where to go next** — Write an AGENTS.md this week. One concrete assignment. Handout has more.

**0:56** • **Handout + Q&A**

---

# Demo Prompts

**Type these into the agent live. Numbered so you can find your place quickly.**

## Prompt 1 — Ask for a plan *(slide 08, ~0:16)*

*Confirm you are in ask/plan mode before sending.*

```
Please read weather_analysis.ipynb carefully. Then propose a plan for
refactoring it into a clean Python module. Don't write any code yet —
just the plan. What functions would you extract? What would you keep
in the notebook?
```

*Wait 30–90s. Agent will likely add type hints and possibly a tests directory. Point at those on screen when the plan comes back.*

## Prompt 2 — Revise the plan *(slide 08, ~0:20)*

```
Two revisions. Take out the type hints — keep the function signatures
simple with just parameter names. Add a one-line docstring to each
function. Skip the tests directory for now. And keep all plotting
inline in the notebook — don't extract plot helpers.
```

## AGENTS.md — type live into editor *(slide 10, ~0:24)*

*Type this in front of the room. Do not paste.*

```markdown
# AGENTS.md

This is a small weather-analysis project working with hourly temperature
data from Seattle-Tacoma airport.

## Conventions

- All timestamps in raw data files are UTC unless explicitly noted otherwise.
- Prefer pandas over polars.
- Prefer matplotlib over seaborn or plotly.
- Functions should have one-line docstrings.

## What not to do

- Don't add type hints unless asked.
- Don't extract plotting into helper functions — keep plotting inline in notebooks.
```

*Then in terminal:*

```
git add AGENTS.md
git commit -m "add project conventions for agent"
```

## Prompt 3 — Extract the module *(Demo Phase 2, ~0:28)*

*Switch modes: ask → agent. Show the toggle on screen.*

```
Following the plan, extract the functions into a new module called
weather.py. Update the notebook to call the module functions.
Don't touch anything else.
```

*Wait 60–90s. When done: show diff before running. Then run all cells. Then commit:*

```
git add -A
git commit -m "extract cleaning and aggregation to weather.py"
```

## Prompt 4 — Explain the bug *(Demo Phase 3, ~0:38)*

*Do not ask for a fix yet. Ask for explanation only.*

```
The diurnal profile shows a peak at hour 23 and a trough around hour 10.
That's inverted from what we'd expect for Seattle — the peak should be
mid-afternoon local time. Before making any changes, can you look at
the data and explain what's going on?
```

*Agent will identify UTC/local timezone issue. Read the explanation aloud. Callback to the AGENTS.md UTC line.*

## Prompt 5 — Apply the fix *(Demo Phase 3, ~0:42)*

```
Good — that matches what I expected. Please fix load_and_clean in
weather.py to convert timestamps to America/Los_Angeles time before
setting the index. Don't touch the notebook — the fix should be
localized to the module.
```

*Agent adds one line: `.dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')`. Review the diff. Re-run notebook. Peak now at hour 15. Commit and advance to slide 12 after a physical beat.*

---

## If something breaks

- **Agent hangs on any prompt** → narrate ("this is why you don't leave agents unattended"), switch to fallback video
- **Agent doesn't add type hints on Prompt 1** → point at whatever else it over-added (docstrings, defaults, imports) and use that as the scope-creep example
- **Agent misses the bug on Prompt 4** → nudge: *"look at the timestamps in the raw CSV, look at the peak hour"*
- **Running out of time** → cut slide 16 to one sentence; do not skip slide 15