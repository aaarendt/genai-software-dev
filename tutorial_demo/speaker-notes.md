# Speaker Notes: Working With a Coding Agent

**Duration:** 60 minutes
**Format:** Lecture with one driven live demo woven through as a spine
**Tool anchor:** Claude Code (concepts portable to Cursor, Copilot, others)
**Demo vehicle:** `weather_analysis.ipynb` — hourly Seattle-Tacoma temperature data, 2024

---

## How to use this document

This is a narrative walkthrough of the full 60-minute session, keyed to the slide IDs in `SLIDES.md`. It's meant to be read cover-to-cover during rehearsal and skimmed on the day of. Timing anchors are targets, not deadlines — if a demo phase runs long, the flex points are called out at the transitions.

Everything in italics inside brackets is a stage direction — what's on screen, what to do physically, what to have already prepared. Everything else is roughly what to say, but delivered in your own words. Do not read this verbatim.

---

## Pre-session checklist

- [ ] `prepare_data.py` has been run; `ksea_2024.csv` exists in the demo directory
- [ ] `weather_analysis.ipynb` opens cleanly and runs top-to-bottom without error
- [ ] Terminal and editor visible, font size large enough for the back row
- [ ] Git repo initialized in the demo directory, one clean commit ("before agent")
- [ ] Coding agent authenticated, mode indicator visible on screen
- [ ] Handout printed or QR code prepared on the title slide
- [ ] Pre-recorded fallback video of each demo phase, in case live agent hangs
- [ ] `git config` has your name and email set — the agent's commits should attribute correctly
- [ ] The AGENTS.md phrasing you plan to write live is fresh in your head — you should be able to type it without pausing to think

---

## Act 1 — From chat to agent *(0:00–0:15)*

### Slide 01 — Title *(0:00–0:00:30)*

*[Walk to the front. Title slide up.]*

Set expectations for the tone: this is a change of pace from the rest of the week. The whole institute is about AI/ML as a research tool — models, methods, results. This one hour flips the frame: AI as a coworker inside the code you write to *do* the research. Different topic, same discipline.

Keep it to two sentences of framing. The demo is the show.

### Slide 02 — 'You have one of these on your laptop right now.' *(0:00:30–0:02)*

*[Bring up the messy notebook on screen next to the slide.]*

Ask the room directly: *who has one of these on their laptop somewhere?*

**Wait for hands.** Almost all go up. Small laugh in the room. That laugh is the sign the room is with you. If it doesn't come, either the notebook isn't visibly messy enough or the room needs another prompt — try naming a specific feature: "the six cells named 'test' and 'test2' at the bottom?" That usually gets it.

Say: *we're going to work on one together today.*

### Slide 03 — 'This is not "AI writes your code."' *(0:02–0:02:30)*

Quick expectation-setting, 30 seconds:

- This is not a demo where I say "build me a machine learning pipeline" and something perfect appears
- The three things you'll leave with: a mental model of how these tools actually work, a couple of concrete habits, and enough vocabulary to read the docs for whichever tool you end up using
- Coworker, not oracle

Do not linger. Move on.

### Slide 04 — 'Chat answers questions. An agent reads your files, runs your code, edits your project.' *(0:02:30–0:04:30)*

**This is the single distinction most non-agent users need to internalize. Do not rush it.**

Talk through the harness idea: same underlying language model, but an *agent* is that model wrapped in a piece of software that gives it access to your files, the ability to run code, and the ability to edit and save. "I'm using Claude" is under-specified — Claude in a browser and Claude Code and Claude in Cursor all behave differently because the harness is different. The harness, not the model, is what changed in the last two years.

Watch the room here. If people look confused about "harness," swap in "wrapper" or "runtime" — the specific word matters less than the concept landing.

### Slide 05 — 'Six pieces. Every tool has all of them.' *(0:04:30–0:07)*

The durable mental model for the whole hour. Take your time.

Point at each piece as you name it:

- **LLM backbone** — the language model itself; the thing generating text
- **Tool use** — the ability to read files, edit them, run commands
- **Agent loop** — the software that lets it decide whether to call another tool or finish
- **Project memory** — a file the agent reads on startup so it knows about your codebase
- **MCP servers** — a standard way to plug in external things like databases, calendars, APIs
- **Skills** — reusable procedures for specific kinds of tasks

The takeaway that has to stick: **every feature you see in every product maps to one of these six.** When you look at Cursor's docs, or Copilot's docs, or Claude Code's docs, and you get overwhelmed — stop and ask, which of the six is this? Suddenly it's much less scary. The tools are all doing roughly the same thing in slightly different clothes.

### Slide 06 — 'Trained in vs. in the prompt.' *(0:07–0:12)*

**Hold this slide for longer than feels comfortable.** This is the model that pays off every day for the rest of the audience's career.

The two-sided frame:

- **Trained in:** Python syntax, common libraries, general programming patterns, how to hold a conversation. Baked in months ago when the model was made. You cannot change it directly.
- **In the prompt:** the system message, your instructions, the files you give it, the project memory file you write. This side you control completely.

The line that has to land: **when you debug why an agent did something weird, ask yourself — was that a training problem or a prompt problem? Because you can only fix one of them.**

Everything in the next 45 minutes lives on the right-hand column. Say that out loud.

### Slide 07 — 'A messy notebook. Weather station data. We're going to refactor it.' *(0:12–0:15)*

*[Switch to the terminal/editor. Notebook is on screen.]*

Walk the room through the notebook briefly: loads a CSV of hourly temperature data for Seattle-Tacoma, cleans it, resamples to daily, looks at the diurnal pattern, produces a naive forecast. It works. It runs. It's a mess.

**Say the definition of refactor out loud even though it's obvious to you:**

> Quick side note in case that word isn't familiar — refactoring means reorganizing code without changing what it does. You take working-but-messy code and turn it into working-and-clean code. Same inputs, same outputs, better shape. It's one of the most common things you'd ask an agent to help with, and it's a good first task because you can check the answer: run the old version, run the new version, compare.

Then state what the demo will actually do: three phases. First, ask the agent to propose a plan — no code, just a plan. Second, extract cleaning and aggregation logic into a proper module. Third, something interesting will come up. Don't spoil it.

Tie back to the week: *some of you did time series methods on Tuesday. This is the engineering scaffolding those methods sit on. Before you can fit an LSTM to weather data, someone has to write this notebook first, and then someone has to clean it up. Today we're doing the cleaning-up part, together with an agent.*

---

## Act 2 — Shaping agent behavior *(0:15–0:35)*

### Slide 08 — 'The quality of AI output is the quality of the context you provide.' *(0:15–0:16:30)*

The thesis of the middle third. 90 seconds max.

The point: everything about how well an agent works comes down to context — the information you give it. Good context in, good work out. Vague or incomplete context in, plausible-sounding garbage out.

Then the reframe that lands with this audience: **you already know how to build context. That's what research methodology is.** Defining terms, stating assumptions, specifying inputs. All we're doing now is applying that same discipline to a piece of software. If you can write a methods section, you can write a good agent prompt. Same skill.

### Slide 09 — 'Read-only for planning. Agent mode for editing.' *(0:16:30–0:17:30)*

**This slide exists because half the room will try this in Copilot's default agent mode on Monday and get a mess.** 45 seconds well spent.

Every coding-agent tool has modes: ask, plan, edit, agent. Named differently in each tool.

*[Show your own mode indicator on screen while saying this.]*

Where to look:
- In Copilot inside VS Code — the dropdown at the bottom of the chat pane
- In Cursor — the mode selector next to the model name
- In Claude Code — the mode is shown in your prompt line
- In Windsurf — in the Cascade panel header

The line to leave the room with: **"Please propose a plan — don't write code yet" is a polite request that the agent may ignore if it has permission to edit.** Safer default: read-only mode when planning, upgrade to agent mode when ready to execute.

If you can't tell what mode you're in, don't send the prompt yet.

⚠️ **Verify before presenting:** these UIs change frequently. If Cursor or Windsurf has moved things recently, drop that bullet or hedge to "somewhere in the chat panel — find it in whichever tool you use."

### Slide 10 — Demo Phase 1: 'Ask for a plan. Not code.' *(0:17:30–0:24)*

*[Confirm you are in ask/plan mode. Show it on screen.]*

Frame the prompt before you send:

> When you start working with an agent on a real task — not "write me a one-liner," but a real task — the worst thing you can do is jump straight to "write the code." You will get code. It will look right. And you will spend the next hour figuring out that it isn't. Ask for a plan first.

*[Type the prompt into the agent:]*

> Please read `weather_analysis.ipynb` carefully. Then propose a plan for refactoring it into a clean Python module. Don't write any code yet — just the plan. What functions would you extract? What would you keep in the notebook?

Send. Agent starts working. **This will take 30–90 seconds. Use the pause to teach.**

Two things to say while it works:

**First — notice what it's doing.** It's reading the whole notebook. All the cells. This is what "an agent reads your files" means — it's actually loading the full content into what's called its context window before deciding what to say.

**Second — notice what it's not doing.** It's not asking clarifying questions. It's not saying "wait — do you want tests? do you want type hints? what Python version?" Most agents right now, on most tasks, will not ask. They will just proceed. **That's not a virtue. That's a failure mode.** Part of what you have to do as the researcher is fill in the questions the agent should have asked but didn't.

*[Agent finishes. Plan appears — probably lists 4–6 functions to extract, maybe with type hints added uninvited, possibly with a `tests/` directory proposed.]*

Read the plan out loud. Point at what's reasonable. **Then find the scope-creep and name it:**

> Notice something the agent did that I didn't ask for. See these little arrows here — `-> pd.DataFrame`, `-> None`? Those are called type hints. They're a Python feature that documents what kind of data a function takes and returns. Useful sometimes. But I didn't ask for them. It added them anyway. **This is a real thing that happens with agents — they often do slightly more than you asked. Sometimes that's helpful, sometimes it's not.** Today I'd rather not add them; I want the minimum change that makes this cleaner.

Push back on the agent visibly:

> Two revisions. Take out the type hints — keep the function signatures simple with just parameter names. Add a one-line docstring to each function. And skip the tests directory for now; we'll add tests separately. Also keep all plotting inline in the notebook — don't extract plot helpers.

Plan updates. Now it's what you want.

**The takeaway line:** *the plan is not something the agent hands you and you accept. The plan is a document you shape. That editing step you just watched — that's the moment when the human researcher puts their judgment into the process. If you let the agent's first plan be the plan, you're outsourcing your judgment to a language model. Which sometimes is fine. But if you're doing research, mostly it's not.*

### Slide 11 — 'Four places to shape agent behavior.' *(0:24–0:26)*

Everything you just did was shaping the agent through the prompt. That works, but it's the least durable version of what's possible.

Four surfaces, one gloss each — do not go deep on any of them:

- **Context documents (AGENTS.md)** — always loaded on startup; facts and conventions the agent should always have in hand
- **Skills** — task-triggered procedures; the agent picks them up when work matches. Good for "when analyzing time series, always check for missing values and irregular sampling"
- **Rules** — path-scoped constraints that fire based on which files are touched; hard limits rather than helpful suggestions. Good for "code in `analysis/` must have a test"
- **Custom agents** — distinct personas with their own tool access and voice; useful when you want a narrower, more focused agent for a specific job

**Taxonomy is portable across tools; file names differ.** In Claude Code, the context doc is `AGENTS.md`. In Copilot, `.github/copilot-instructions.md`. In Cursor, `.cursor/rules`. Same idea, different filenames.

*Today we're going to use the first one seriously and just name the others. If you take away one thing from this middle third of the hour, it's the AGENTS.md file. Everything else is a variation.*

### Slide 12 — 'AGENTS.md — ten lines that change how the agent behaves.' *(0:26–0:30)*

*[Switch to editor. Create AGENTS.md live. Type it in front of the room — do not paste from a prepared file. The audience should see you compose it.]*

Something like:

```markdown
# AGENTS.md

This is a small weather-analysis project working with hourly temperature data
from Seattle-Tacoma airport.

## Conventions

- All timestamps in raw data files are UTC unless explicitly noted otherwise.
- Prefer pandas over polars.
- Prefer matplotlib over seaborn or plotly.
- Functions should have one-line docstrings.

## What not to do

- Don't add type hints unless asked.
- Don't extract plotting into helper functions — keep plotting inline in notebooks.
```

Read it back to the room:

> Ten lines. Framing — what this project is. Conventions — my library preferences and code style. Constraints — things I want the agent *not* to do. Every one of these is something I would otherwise have to type in a prompt, over and over, every time I started a new session. AGENTS.md lets me say it once.

**Point specifically at the UTC line** — this is the seed for Act 3, and it needs to sit in the room's mind:

> This line — *all timestamps in raw data files are UTC unless explicitly noted otherwise* — that's the kind of thing you'd only think to write down after being bitten by a timezone bug once. Which I have been. Many times.

Also note the "no type hints" line — it lands harder because the room just saw the agent add them uninvited two minutes ago.

*[Commit:]*

```
git add AGENTS.md
git commit -m "add project conventions for agent"
```

The point: version-controlled, team asset, survives you leaving the project. Every collaborator gets the same context. Every session starts with these conventions in the agent's head.

### Slide 13 — Demo Phase 2: 'Now extract the cleaning logic.' *(0:30–0:35)*

*[Physically switch modes on screen — from ask/plan to agent mode. Do it slowly enough that the back row can see.]*

Say what you just did:

> See that? I just switched from ask mode into agent mode. Two minutes ago I was in a read-only conversation. Now the agent has permission to edit files. This is deliberate. **Think of mode as a physical gate — you cross it when you're ready for the agent to touch your files, and you cross back when you're not.** Don't leave it in agent mode all day. You will forget you're in it, ask what feels like a casual question, and come back to find seven files edited.

*[Send the prompt:]*

> Following the plan, extract the functions into a new module called `weather.py`. Update the notebook to call the module functions. Don't touch anything else — no tests, no plot helpers, no additional files.

Agent starts working. **This will take 60–90 seconds. Talk about git while you wait.**

The git-as-safety-net beat:

> Before we started this session, I made a git commit. Clean tree, everything checked in. That means right now — right this second, while the agent is editing multiple files — I have a one-command undo. If this goes sideways, `git restore .` puts me back. If it goes sideways in some subtle way I don't notice for ten minutes, the diff shows me every character that changed.

The line to leave the room with: **treat every commit like a save point in a video game.** Commit before you start a session. Commit at the end of each phase. Commit before anything risky. This is not just software hygiene — it's specifically an agent-safety practice, because agents can edit multiple files at once, silently, and produce a much larger diff than you expected.

**Optional beat if the agent takes longer than expected:**

> By the way — this pause you're watching me do right now? This is one of the underrated benefits of these tools. When the agent is thinking for a minute, that's a minute I have to actually consider what I asked for. Chat interfaces where the response comes back instantly don't give you that. The slower loop is not always the worse loop.

*[Agent finishes. `weather.py` exists. Notebook updated. Agent produces a summary.]*

Do not run anything yet. Move to the next slide.

---

## Interlude: reading the diff *(0:35–0:36)*

### Slide 14 — 'The chat is a claim. The diff is evidence.'

**This is a pause-and-repeat moment. Say the key message twice.**

Look at what the agent told you it did. That's a claim. It might be true. It's probably mostly true. But you don't know until you look.

*[Show the diff in whatever tool you actually use — VS Code's Source Control panel is fine, or `git diff` in a terminal, or the GitHub-style diff view in Cursor. Say it out loud that it doesn't matter which tool:]*

> Look at the diff, whatever you use to look at diffs. I'm going to use VS Code's Source Control panel because that's where my attention is anyway — green means added, red means removed. You could do the same thing with `git diff` at the command line — same information, different presentation. Use whichever matches how you work.

Read through:

- `weather.py` — read each function briefly. Confirm docstrings are there. Confirm no type hints. Confirm no test file, no plot helpers.
- Notebook — the exploratory cells still there. Actual work now happens through function calls instead of inline code.

Then run the code — either via `jupyter nbconvert --to notebook --execute` or by opening the notebook and running all cells. Whatever your setup supports live.

Compare against the original outputs: same annual mean (~9°C), same daily plot shape, same forecast value. Numbers match. Plots match.

Commit:

```
git add -A
git commit -m "extract cleaning and aggregation to weather.py"
```

**Two save points. If Act 3 goes off the rails, you can `git restore` back to right here.**

### Slide 15 — 'Nothing magical happened.' *(0:36–0:37)*

Take stock. Count off on fingers or gesture through the beats:

- I asked the agent to read a notebook
- It read it
- I asked for a plan; it gave me a plan; I edited the plan
- I wrote a small file that tells it about my project
- I switched modes
- I asked it to execute the plan; it executed it
- I read the diff
- I ran the code
- I committed

That's it. Nothing magical. No point where the agent took over and did something you couldn't follow. Every step was one you supervised. **This is the shape of every session you'll have with these tools for the rest of your career.** Ask, get proposal, shape proposal, get output, read output, verify output, commit.

Then the Act 3 setup:

> But — I want to check one more thing before I call this done. We ran the refactored code. We got the same numbers as before. Everything matches. So the refactor is correct, right?

**Wait. Let the question sit.**

> Well. The refactor preserved the behavior of the original notebook. That's not the same thing as saying the original notebook was correct.

*[Take a deliberate sip of water. The five-second silence here does more than any slide could. The room should be leaning in.]*

---

## Act 3 — Keeping it trustworthy *(0:37–0:55)*

### Slide 16 — Demo Phase 3: 'The bug was always there.' *(0:37–0:45)*

**This is the emotional peak of the hour. Do not rush any of it.**

*[Open the diurnal profile plot — the "temperature by hour" bar chart.]*

Point at the plot. **Then wait — three or four seconds of silence.** Give the room a chance to see it.

Ask: *what do you see?*

If someone speaks up, let them name it. If nobody does within about five seconds, name it yourself:

> The peak is at hour 23. The coldest hour is around 10. So according to this plot, Seattle-Tacoma is warmest at 11 PM and coldest at 10 AM.
>
> That's not a Seattle thing. That's a wrong thing.

**Beat. Let it land.**

Then the sentence the room needs to hear:

> The peak of the day should be mid-afternoon — 2, 3 PM. That's when temperature peaks basically everywhere on Earth that isn't near a pole. Something is off. And here's what I want you to sit with — **nothing about the summary statistics told us this.** The annual mean is fine. Daily min-max-mean is fine. The forecast number is fine. If we had shipped this analysis based on numeric outputs alone, we would have shipped a bug. It took looking at a plot — a specific plot, that we thought to make — to see it.

**Now the trace.** Do not fix it yourself. Hand the question back to the agent — this shows the audience how to use the tool for diagnosis, not just generation.

Frame the prompt aloud before you send:

> Notice how I'm framing this — I'm not saying "fix it." I'm saying "explain it." I want to understand before I let it change anything.

*[Type:]*

> The diurnal profile shows a peak at hour 23 and a trough around hour 10. That's inverted from what we'd expect for Seattle — the peak should be mid-afternoon local time. Before making any changes, can you look at the data and explain what's going on?

Send. Agent works. **Talk about diagnostic prompting while you wait:**

> Asking for explanation before action is a way to check whether the agent actually understands the problem. If it explains it well, I'll trust its fix. If the explanation is off, I'll know not to accept whatever code it proposes next.

*[Agent identifies the timezone issue — timestamps in CSV are UTC, code treats `df.index.hour` as if local, so UTC hour 23 (roughly 3 PM local Pacific) shows on the plot labeled as "hour 23" which reads as 11 PM.]*

Read the explanation. Then the callback that makes the whole hour connect:

> There it is. Timestamps are UTC. The code treats them as if they were local. **And remember what I wrote in AGENTS.md?** *All timestamps in raw data files are UTC unless explicitly noted otherwise.* This is exactly why that line exists. If I hadn't written it, the agent might have needed more prodding to catch this. But because that convention was already in front of it, it knew where to look. **That one line, that took me thirty seconds to write, is what makes this bug traceable instead of mysterious.**

*[Ask for the fix:]*

> Good — that matches what I expected. Please fix `load_and_clean` in `weather.py` to convert timestamps to America/Los_Angeles time before setting the index. Don't touch the notebook — the fix should be localized to the module.

Agent applies a one-line fix — `.dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')` after `pd.to_datetime`. Review the diff.

**The localization beat:**

> One line. That's the whole fix. And notice — because the bug was localized inside a single function during the refactor, the fix is also localized. This is a payoff for having done the refactor properly. If we were still working with the messy notebook where this logic was spread across three cells, we'd be editing in three places. **The refactor made the code fixable.**

Re-run the notebook. Diurnal plot now peaks at hour 15 (3 PM Pacific). That's Seattle. Commit.

### Slide 17 — 'The agent produces plausible code. Your job is to verify.' *(0:45–0:47)*

**Slow down. This is the sentence the room needs to remember.**

> The agent didn't introduce the bug. The bug was already there. The agent didn't cause it — but the agent *also* didn't catch it during the refactor. It faithfully reproduced code that was silently wrong. And every summary statistic we looked at said the code was fine.
>
> The agent produces *plausible* code. Not correct code. Plausible code. Code that looks like what a reasonable person would write. And a reasonable person's code passes casual review. It doesn't fail loudly. It fails quietly, in exactly the kind of way summary statistics don't catch.
>
> Your job — the human researcher's job — is to verify. Not because the agent is untrustworthy in general. It's actually pretty good. But because **it does not know what you know about your data.** It doesn't know Seattle should peak mid-afternoon. It doesn't know your instrument calibration was off between March and May. It doesn't know your genomic samples got mislabeled at the sequencing core. All the things you know about your work that make you the researcher — those never make it into the agent's context unless you put them there. And even then, only some of it lands.
>
> That's not a bug. That's the shape of the collaboration.

**Let the last sentence sit. Do not rush to the next slide.** In a real room this is where a couple of people start writing in their notebooks. Give them the pause to do it.

### Slide 18 — 'Five habits.' *(0:47–0:50)*

Generalize the practices you just demonstrated:

- **Read the diff, not the chat** — you just did this. It has a name now.
- **Test-first when it matters** — ask the agent to write the test before writing the code. The failing test becomes the specification.
- **The `[CITATION NEEDED]` pattern** — for high-hallucination-risk content (references, statistics, dates), have the agent explicitly flag what it's uncertain about. You look for the *absence* of the marker as the failure signal.
- **Evals as a distinct practice** — scored suites for agent behavior on your domain. Name-drop only; further reading in the handout.
- **Push back is allowed** — the agent is a coworker, not an oracle. Push back includes "no, you're in the wrong mode" and "no, you did more than I asked" — half of what looks like the agent going rogue is a permissions or scope problem you can just correct.

### Slide 19 — 'LLMs are stochastic. Science demands reproducibility.' *(0:50–0:51)*

One beat of honesty. Do not solve it yet — that's the next slide.

> This is a real tension, not a rhetorical one. "I used AI to help write my analysis" is not a reproducible methods description. And the resolution is not to give up on either side.

### Slide 20 — 'The process is not reproducible. The artifacts are.' *(0:51–0:54)*

This is the slide that answers the concern most attendees came in with. Deliver it slowly.

- The chat conversation is not the record. The **git repo** is the record.
- Docs committed alongside code become an audit trail — plans, review notes, validation outputs. `git log docs/` reads like a lab notebook.
- Log the model, version, and date in your methods section — the same way you'd cite any other tool.
- Pin your dependencies. AI-generated code often assumes packages or versions that aren't in your environment spec. CI catches this fast.

**The line that ties it together:** *the AI conversation is scaffolding. The committed artifact is the science. Treat them accordingly.*

### Slide 21 — 'Where to go next.' *(0:54–0:55)*

90 seconds. A map for the curious, not a sales pitch.

- **Skills** — turning your lab's repeated procedures into reusable modules the agent can pick up automatically. Institutional memory that survives personnel turnover.
- **Evals** — if you'll do a task more than three times, evals pay for themselves. The reproducible artifact that makes agent-assisted work defensible.
- **MCP** — connecting agents to your actual data sources: databases, calendars, internal APIs. Where the interesting integration work is happening right now.
- Full reading list on the handout.

---

## Close *(0:55–1:00)*

### Slide 22 — 'A checklist for Monday morning.' *(0:55–0:57)*

Show the handout. Walk the four sections briefly:

- **Before you start** — commit clean tree, write AGENTS.md, scope the task, ask for a plan
- **While you're working** — read the diff, re-run, push back, commit at phases
- **Before you trust the output** — compare summary stats, ask for a test, flag uncertainty, log model version
- **Warning signs** — confident specificity in your niche, files touched you didn't expect, "looks right" without articulation, you've stopped reading diffs

If QR code, place it large and center. Q&A begins after this slide.

### Slide 23 — 'The agent is a coworker. Read the diff.' *(0:57 → Q&A)*

Optional closing slide. Two sentences, nothing more. Leave it up during Q&A.

---

## Timing flex points

- **If Act 3 demo surfaces the bug faster than expected** → expand verification practices (slide 18), spend more time on each of the five habits
- **If Act 3 demo drags** → cut the evals name-drop, go straight to reproducibility
- **If Demo Phase 2 hangs live** → narrate what went wrong ("this is exactly why you don't leave agents unattended"), cut to pre-recorded fallback video
- **If you have 5 extra minutes** → between Acts 2 and 3, insert "what the agent can and cannot see" — where your data lives, what leaves your machine, consumer web vs. institutional gateway. This audience has real IRB and pre-publication data concerns that will surface in Q&A anyway.

---

## Q&A prep — anticipated questions

**"How does the agent know what a good plan looks like?"**
It's been trained on billions of lines of code, including many refactors. It has statistical intuitions about "what code like this usually looks like clean." That's a strength for common patterns and a weakness for your specific domain — which is why AGENTS.md and skills exist. Both push its intuitions toward your context.

**"What if I don't know what to ask for?"**
Ask the agent for options. "Here's the notebook — what are three different ways you could refactor this, and what are the tradeoffs?" You don't have to know the answer to ask a good question. This is one of the highest-value patterns for people who don't consider themselves strong developers.

**"How do I know when to trust it?"**
Wrong question. Never trust it. Verify it. The trust question doesn't need answering if the verification habit is in place. That's the whole point of Act 3.

**"Isn't this just going to make people worse at coding?"**
Maybe some people. But the frame here is not "AI replaces skill." It's "AI is a coworker whose output you review." Reading code critically is a first-class skill, and it becomes *more* important, not less, when agents write most of the code. If you can't read the diff, you can't do the work.

**"What about privacy? My data is under IRB / NDA / pre-publication."**
Depends on which tool and which tier. Consumer web interfaces often log and train on prompts. Enterprise tiers and institutional gateways usually don't. Local models don't send anything off your machine. If you can't tell what tier you're on, assume the worst until you can. And even for enterprise tiers: **redaction and synthetic samples work.** Send a schema, not the data. Send the shape of the problem, not the protected content.

**"What if the agent is confidently wrong about something in my niche?"**
This is exactly why AGENTS.md and skills exist. Any time you catch the agent making a wrong assumption about your domain, that's a candidate to add to your context document so it doesn't happen next time. Treat it as encoding institutional knowledge, not fixing a bug.

**"Is this ethical? Environmental cost, labor displacement, etc."**
The values are yours to draw. What I'll say factually: the tools are here, people around you are using them, and the choice you have is whether to engage with them thoughtfully or leave the norms to be set by people who aren't thinking carefully. Drawing your own lines and writing down your own personal use policy is legitimate work.

---

## Recovery notes

**If the agent produces a bad plan.** Perfect teachable moment. Do not try to fix it silently. Say aloud what's wrong with it, edit it in front of the room, explain the fix. The lesson is not "agents produce good plans"; the lesson is "the plan is a document you shape."

**If the agent refuses to write code in ask mode.** Ideal — that's the mode working as designed. Say so and move on.

**If the agent misses the bug in Act 3 even after being prompted.** Fine. Nudge more directly: "Look at the diurnal profile plot. Look at where the peak is. Look at the timestamps in the raw CSV." The lesson is that verification is on you either way; the agent as a diagnostic tool is nice-to-have, not essential.

**If you run out of time.** Cut slide 21 (where to go next) and slide 23 (closing). Land on slide 22 (handout) and let Q&A begin.

**If the room is completely silent during the bug reveal.** Good. Let them process. Do not fill the silence with more words.