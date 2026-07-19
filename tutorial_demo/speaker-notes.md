# Speaker Notes: Working With a Coding Agent

**Duration:** 60 minutes
**Format:** Lecture with one driven live demo woven through as a spine
**Tool anchor:** Claude Code (concepts portable to Cursor, Copilot, others)
**Demo vehicle:** `weather_analysis.ipynb` — hourly Seattle-Tacoma temperature data, 2024
**Slide count:** 16

---

## How to use this document

This is a narrative walkthrough of the full 60-minute session, keyed to the slide IDs in `SLIDES.md`. Read cover-to-cover during rehearsal, skim on the day of. Timing anchors are targets, not deadlines — flex points are called out at the transitions.

Bracketed italics are stage directions. Blockquotes are near-verbatim narration you can rehearse from, but deliver in your own words on the day.

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

Set expectations for tone. This is a change of pace from the rest of the week. The whole institute is about AI/ML as a research tool — models, methods, results. This one hour flips the frame: AI as a coworker inside the code you write to *do* the research. Different topic, same discipline.

Two sentences of framing, then move on. The demo is the show.

### Slide 02 — Opening recognition *(0:00:30–0:02)*

*[Bring up the messy notebook on screen next to the slide.]*

The recognition move — many researchers have poorly formatted, incomplete notebooks on their laptop. I have a lot of these myself, and will show you one today. You're going to work on it together with the room.

Wait for the acknowledgment in the room — nodding, small laughs. That signal is the point of this slide.

Say something like: *today we're going to take one of these and apply some gen-AI methods to see what's possible in a short amount of time.*

### Slide 03 — 'This is not "AI writes your code."' *(0:02–0:02:30)*

Quick expectation-setting, 30 seconds:

- This is not a demo where I say "build me a machine learning pipeline" and something perfect appears
- The three acts of the hour: how it works, how you shape it, how you keep it trustworthy
- Coworker, not oracle

Do not linger.

### Slide 04 — Chat vs. agent *(0:02:30–0:04:30)*

**This is the single distinction most non-agent users need to internalize. Do not rush it.**

Talk through the harness idea: same underlying language model, but an *agent* is that model wrapped in a piece of software that gives it access to your files, the ability to run code, and the ability to edit and save. "I'm using Claude" is under-specified — Claude in a browser and Claude Code and Claude in Cursor all behave differently because the harness is different. The harness, not the model, is what changed in the last two years.

Watch the room. If people look confused about "harness," swap in "wrapper" or "runtime" — the specific word matters less than the concept landing.

### Slide 05 — Six pieces *(0:04:30–0:07)*

The durable mental model for the whole hour. Take your time.

If the slide is rendered as a diagram, point at each piece as you name it:

- **LLM backbone** — the language model itself; the thing generating text
- **Tool use** — the ability to read files, edit them, run commands
- **Agent loop** — the software that lets it decide whether to call another tool or finish
- **Project memory** — a file the agent reads on startup so it knows about your codebase
- **MCP servers** — a standard way to plug in external things like databases, calendars, APIs
- **Skills** — reusable procedures for specific kinds of tasks

The takeaway that has to stick: **every feature in every product maps to one of these six.** When you look at Cursor's docs, or Copilot's docs, or Claude Code's docs, and get overwhelmed — stop and ask, which of the six is this? Suddenly it's much less scary. The tools are all doing roughly the same thing in slightly different clothes.

### Slide 06 — Trained-in vs. in the prompt *(0:07–0:12)*

The two-sided frame:

- **Trained in:** Python syntax, common libraries, general programming patterns, how to hold a conversation. Baked in months ago when the model was made. You cannot change it directly.
- **In the prompt:** the system message, your instructions, the files you give it, the project memory file you write. This side you control completely.

The line that has to land:

> When you debug why an agent did something weird, ask yourself — was that a training problem or a prompt problem? Because you can only fix one of them.

Everything in the next 45 minutes lives on the right-hand column. Say that out loud.

### Slide 07 — Demo setup *(0:12–0:15)*

*[Switch to the terminal/editor. Notebook is on screen.]*

Walk the room through the notebook briefly: loads a CSV of hourly temperature data for Seattle-Tacoma, cleans it, resamples to daily, looks at the diurnal pattern, produces a naive forecast. It works. It runs. It's a mess.

**Say the definition of refactor out loud even though it's obvious to you:**

> Quick side note in case that word isn't familiar — refactoring means reorganizing code without changing what it does. Same inputs, same outputs, better shape. It's one of the most common things you'd ask an agent to help with, and it's a good first task because you can check the answer: run the old version, run the new version, compare.

Then state what the demo will do — **honest framing, no theatrical setup:**

> We're going to have the agent do three things. Propose a plan. Extract a module. And help us verify our code.

Tie back to the week:

> Some of you did time series methods on Tuesday. This is the engineering scaffolding those methods sit on. Before you can fit an LSTM to weather data, someone has to write this notebook first, and someone has to clean it up. Today we're doing the cleaning-up part, together with an agent.

---

## Act 2 — Shaping agent behavior *(0:15–0:35)*

### Slide 08 — Demo phase 1: ask for a plan *(0:15–0:22)*

This slide is rendered as a flowchart with "check your mode" as the first node. When it comes up, walk through the flowchart briefly before typing:

> Every coding-agent tool has modes. Ask, plan, edit, agent — named differently in each tool. Before I send anything, I want to be sure I'm in ask or plan mode, not agent mode. Otherwise "please propose a plan — don't write code" is a polite request the agent may ignore because it has permission to edit anyway.

*[Show your own tool's mode indicator on screen. Confirm you're in ask/plan mode.]*

Frame the prompt before you send:

> When you start working with an agent on a real task — not "write me a one-liner," but a real task — the worst thing you can do is jump straight to "write the code." You will get code. It will look right. And you will spend the next hour figuring out that it isn't. Ask for a plan first.

*[Type the prompt:]*

> Please read `weather_analysis.ipynb` carefully. Then propose a plan for refactoring it into a clean Python module. Don't write any code yet — just the plan. What functions would you extract? What would you keep in the notebook?

Send. Agent starts working. **30–90 seconds. Use the pause to teach.**

Two things to say while it works:

**First — notice what it's doing.** It's reading the whole notebook. This is what "an agent reads your files" means — actually loading the full content into its context window before deciding what to say.

**Second — notice what it's not doing.** It's not asking clarifying questions. It's not saying "wait — do you want tests? do you want type hints? what Python version?" Most agents right now, on most tasks, will not ask. **That's not a virtue. That's a failure mode.** Part of what you have to do as the researcher is fill in the questions the agent should have asked but didn't.

*[Agent finishes. Plan appears — probably 4–6 functions to extract, likely with type hints added uninvited, possibly with a `tests/` directory proposed.]*

Read the plan out loud. Point at what's reasonable. **Then find the scope-creep and name it:**

> Notice something the agent did that I didn't ask for. See these little arrows here — `-> pd.DataFrame`, `-> None`? Those are called type hints. They're a Python feature that documents what kind of data a function takes and returns. Useful sometimes. But I didn't ask for them. It added them anyway. **This is a real thing that happens with agents — they often do slightly more than you asked.**

Push back on the agent visibly:

> Two revisions. Take out the type hints — keep the function signatures simple with just parameter names. Add a one-line docstring to each function. And skip the tests directory for now. Also keep all plotting inline in the notebook — don't extract plot helpers.

Plan updates.

**The takeaway line:**

> The plan is not something the agent hands you and you accept. The plan is a document you shape. That editing step you just watched — that's the moment when the human researcher puts their judgment into the process.

### Slide 09 — Four surfaces (context framing) *(0:22–0:24)*

**Say the framing aloud when the slide comes up** — the title carries the concept, but the audience needs to hear it once:

> Everything the agent does is shaped by the context you give it. Context lives in many places — every message you type, every file the agent opens, every tool output. But four of those places are worth designing deliberately, because they persist across sessions.

Then one gloss each — do not go deep on any of them:

- **Context documents (AGENTS.md)** — always loaded on startup; facts and conventions the agent should always have in hand
- **Skills** — task-triggered procedures; the agent picks them up when work matches. Good for "when analyzing time series, always check for missing values and irregular sampling"
- **Rules** — path-scoped constraints that fire based on which files are touched. Good for "code in `analysis/` must have a test"
- **Custom agents** — distinct personas with their own tool access and voice; useful for narrower, more focused agents

**Taxonomy is portable across tools; file names differ.** In Claude Code, `AGENTS.md`. In Copilot, `.github/copilot-instructions.md`. In Cursor, `.cursor/rules`. Same idea, different filenames.

> Today we're going to use the first one seriously and just name the others. If you take away one thing from this middle third of the hour, it's the AGENTS.md file. Everything else is a variation.

### Slide 10 — AGENTS.md live *(0:24–0:28)*

*[Switch to editor. Create AGENTS.md live. Type it in front of the room — do not paste from a prepared file.]*

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

Read it back:

> Ten lines. Framing — what this project is. Conventions — my library preferences and code style. Constraints — things I want the agent *not* to do. Every one of these is something I would otherwise have to type in a prompt, over and over. AGENTS.md lets me say it once.

**Point specifically at the UTC line** — this is the seed for Act 3 and needs to sit in the room's mind:

> This line — *all timestamps in raw data files are UTC unless explicitly noted otherwise* — that's the kind of thing you'd only think to write down after being bitten by a timezone bug once. Which I have been. Many times.

Also note the "no type hints" line — lands harder because the room just saw the agent add them uninvited.

*[Commit:]*

```
git add AGENTS.md
git commit -m "add project conventions for agent"
```

Version-controlled, team asset, survives you leaving the project. Every collaborator gets the same context.

### Demo phase 2 — extract the module *(0:28–0:34)*

*This block runs without a slide. Slide 10 stays up while you set up, then the notebook/terminal takes over.*

*[Physically switch modes on screen — from ask/plan to agent mode. Do it slowly enough that the back row can see.]*

Say what you just did:

> See that? I just switched from ask mode into agent mode. Two minutes ago I was in a read-only conversation. Now the agent has permission to edit files. **Think of mode as a physical gate — you cross it when you're ready for the agent to touch your files.** Don't leave it in agent mode all day. You will forget you're in it, ask what feels like a casual question, and come back to find seven files edited.

*[Send the prompt:]*

> Following the plan, extract the functions into a new module called `weather.py`. Update the notebook to call the module functions. Don't touch anything else.

Agent works. **60–90 seconds. Talk about git while you wait.**

The git-as-safety-net beat:

> Before we started, I made a git commit. Clean tree, everything checked in. Right now — while the agent is editing multiple files — I have a one-command undo. If this goes sideways, `git restore .` puts me back. If it goes sideways in some subtle way I don't notice for ten minutes, the diff shows me every character that changed.

The line to leave the room with: **treat every commit like a save point in a video game.** Commit before you start a session. Commit at the end of each phase. This is not just software hygiene — it's specifically an agent-safety practice, because agents can edit multiple files at once, silently, and produce a much larger diff than you expected.

*[Agent finishes. `weather.py` exists. Notebook updated. Agent produces a summary.]*

**Do not run the code yet. Do not celebrate.** Show the diff first.

*[Show the diff in whatever tool you actually use — VS Code's Source Control panel, `git diff` in a terminal, whatever matches your workflow. Say aloud that the tool doesn't matter:]*

> Look at the diff, whatever you use to look at diffs. I'm using VS Code's Source Control panel because that's where my attention is anyway — green means added, red means removed. Same information as `git diff` at the command line. Use whichever matches how you work.

Read through:

- `weather.py` — read each function briefly. Confirm docstrings are there. Confirm no type hints. Confirm no test file, no plot helpers.
- Notebook — exploratory cells still there. Actual work now happens through function calls.

**Say the phrase, and say it twice:**

> The chat is a claim. The diff is evidence.

Then run the code — via `jupyter nbconvert --to notebook --execute` or by opening the notebook and running all cells. Same annual mean (~9°C), same daily plot shape, same forecast value.

Commit:

```
git add -A
git commit -m "extract cleaning and aggregation to weather.py"
```

Two save points.

### Slide 11 — Act 2 recap *(0:34–0:36)*

*[Advance to the recap slide as you're finishing the commit.]*

Consolidate. Do not narrate through — let the slide breathe.

- The agent read your files, followed your plan, and edited your code. You supervised.
- The chat told us what the agent claims it changed. The diff is where we confirmed it.
- The code looks right, and it runs. The next question is whether the code is *correct* — which is different from whether it runs.

**That third bullet is the bridge to Act 3.** Deliver it without theatrics — verification was named as a phase in slide 07, so it should feel like the natural next step, not a mysterious foreshadowing.

---

## Act 3 — The bug, and what it teaches *(0:36–0:52)*

### Demo phase 3 — the bug reveal *(0:36–0:44)*

*This block runs without a slide. Slide 11 stays up while you transition, then you go back to the notebook.*

**This is the emotional peak of the hour. Do not rush any of it.**

*[Return to the notebook. Open the diurnal profile plot — the "temperature by hour" bar chart.]*

Point at the plot. **Wait — three or four seconds of silence.** Give the room a chance to see it.

Ask:

> What do you see?

If someone speaks up, let them name it. If nobody does within about five seconds, name it yourself:

> The peak is at hour 23. The coldest hour is around 10. So according to this plot, Seattle-Tacoma is warmest at 11 PM and coldest at 10 AM.
>
> That's not a Seattle thing. That's a wrong thing.

**Beat. Let it land.**

Then the observation the room needs to hear:

> The peak of the day should be mid-afternoon — 2, 3 PM. That's when temperature peaks basically everywhere on Earth that isn't near a pole. Something is off. And here's what I want you to sit with — **nothing about the summary statistics told us this.** The annual mean is fine. Daily min-max-mean is fine. The forecast number is fine. If we had shipped this analysis based on numeric outputs alone, we would have shipped a bug.

**Now the trace.** Do not fix it yourself. Hand the question back to the agent.

Frame the prompt aloud:

> Notice how I'm framing this — I'm not saying "fix it." I'm saying "explain it." I want to understand before I let it change anything.

*[Type:]*

> The diurnal profile shows a peak at hour 23 and a trough around hour 10. That's inverted from what we'd expect for Seattle — the peak should be mid-afternoon local time. Before making any changes, can you look at the data and explain what's going on?

Send. Agent works. **Talk about diagnostic prompting while you wait:**

> Asking for explanation before action is a way to check whether the agent actually understands the problem. If it explains it well, I'll trust its fix. If the explanation is off, I'll know not to accept whatever code it proposes next.

*[Agent identifies the timezone issue — timestamps in CSV are UTC, code treats `df.index.hour` as if local, so UTC hour 23 (roughly 3 PM local Pacific) shows on the plot labeled as "hour 23" which reads as 11 PM.]*

Read the explanation. **Then the callback that makes the whole hour connect:**

> There it is. Timestamps are UTC. The code treats them as if local. **And remember what I wrote in AGENTS.md?** *All timestamps in raw data files are UTC unless explicitly noted otherwise.* This is exactly why that line exists. Because the convention was already in front of it, the agent knew where to look. That one line, that took me thirty seconds to write, is what makes this bug traceable instead of mysterious.

*[Ask for the fix:]*

> Good — that matches what I expected. Please fix `load_and_clean` in `weather.py` to convert timestamps to America/Los_Angeles time before setting the index. Don't touch the notebook — the fix should be localized to the module.

Agent applies a one-line fix — `.dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')` after `pd.to_datetime`. Review the diff.

**The localization beat:**

> One line. That's the whole fix. And notice — because the bug was localized inside a single function during the refactor, the fix is also localized. This is a payoff for having done the refactor properly. **The refactor made the code fixable.**

Re-run the notebook. Diurnal plot now peaks at hour 15. That's Seattle. Commit.

*[Look at the corrected plot for a second. Then advance to slide 12.]*

### Slide 12 — The bug and what it teaches *(0:44–0:46)*

*[The transition wants a physical beat — commit the fix, look at the corrected plot, then advance the slide as you start to speak. Do not snap to the slide the instant the fix commits.]*

This slide consolidates the specific case. Tight and grounded — do not generalize yet; slide 13 does that.

Walk the bullets:

- The bug was in the original notebook. The refactor moved the pandas operations verbatim.
- Summary statistics were unaffected. Only the domain-informed look at the diurnal plot surfaced it.
- The AGENTS.md convention we wrote earlier — timestamps are UTC — made the fix traceable rather than mysterious.
- This is the shape of the collaboration: the agent handles the code, you handle the domain.

**The last bullet is the bridge to slide 13.** Deliver it as an observation the demo just proved, not a general claim yet.

### Slide 13 — Plausible code *(0:46–0:49)*

**Slow down. Frame it as a genuine question the audience should sit with, not a verdict.**

Open by naming the widening explicitly:

> That wasn't a bug about weather data. It was an instance of a general pattern. Let me widen the lens.

Then:

> This is not a question of whether the agent is trustworthy — it generally produces plausible, working code. The agent produces *plausible* code. Not correct code. Plausible code. Code that looks like what a reasonable person would write. And a reasonable person's code passes casual review.
>
> The agent does not know the specifics of our data — its quirks, its edge cases, its domain context. It also lacks the scientific domain knowledge we bring as researchers — it cannot judge whether a result is physically reasonable or scientifically meaningful.
>
> Verification is not a safety check on a bad tool. **It is the responsibility that stays with the human researcher.**

**Let the last sentence sit. Do not rush.** In a real room this is where a couple of people start writing in their notebooks. Give them the pause to do it.

### Slide 14 — Verification practices *(0:49–0:50:30)*

Two habits from this demo — the ones you actually demonstrated live:

- **Read the diff, not the chat.** You just did this. It has a name now.
- **Push back is allowed.** The agent is a coworker, not an oracle. Push back includes "no, you're in the wrong mode" and "no, you did more than I asked" — half of what looks like the agent going rogue is a permissions or scope problem you can just correct.

**Then the honest scope-naming, which strengthens rather than weakens the session:**

> There are more advanced patterns — evals, test-first workflows, structured uncertainty flagging. The handout has starting points if you want to go deeper. I'm not going to walk through them because I'd rather teach two habits well than name five badly.

That kind of honesty about scope earns credibility with a research audience.

### Slide 15 — Reproducibility *(0:50:30–0:53)*

*This is the slide that answers the concern most attendees came in with. Deliver it slowly.*

Open with the tension — honestly, not rhetorically:

> LLMs are stochastic. Science demands reproducibility. That tension is real, and I don't want to wave it away. "I used AI to help write my analysis" is not a reproducible methods description.

Then the resolution:

> The process isn't reproducible. The artifacts are. Your git repo — not your chat log — is the record.

Walk the remaining bullets:

- You can optionally commit plans, review notes, and validation outputs alongside code. **`git log docs/` reads like a lab notebook** — dated, attributed, chronological. If you've been committing your reasoning artifacts alongside your code, the log of that folder becomes a durable record of the project's thinking, not just its output.
- Log the model, version, and date in your methods section, the way you'd cite any tool.
- Pin your dependencies, because AI-generated code often assumes packages it didn't declare.

**The line that ties it together:**

> The AI conversation is scaffolding. The committed artifact is the science. Treat them accordingly.

---

## Close *(0:53–1:00)*

### Slide 16 — Where to go next *(0:53–0:56)*

**The concrete action, delivered with matching concreteness.**

> If you leave with one action item, this is it. Pick a project you're already working on. Not a new one. Something you have open right now. Write ten lines that tell an agent what it needs to know about that project — your conventions, what libraries you prefer, things you don't want it to do. Commit it. Then use an agent on that project once this week and notice what changed. That's the whole assignment.

Then briefly point at the handout for anyone who wants more:

> If you're already comfortable with that, the handout has pointers to the next set of practices — skills, evals, MCP — and starting points to explore them.

### Handout walkthrough and Q&A *(0:56–1:00)*

Show the handout on screen. Quick tour of the four sections:

- **Before you start** — commit clean tree, write AGENTS.md, scope the task, ask for a plan
- **While you're working** — read the diff, re-run, push back, commit at phases
- **Before you trust the output** — compare summary stats, log model version, further practices to grow into
- **Warning signs** — confident specificity in your niche, files touched you didn't expect, "looks right" without articulation, you've stopped reading diffs

Q&A begins.

---

## Timing flex points

- **If Demo Phase 1 runs long** → cut the "trained-in vs. in the prompt" restatement on slide 09; the concept has already landed
- **If Demo Phase 2 hangs live** → narrate what went wrong ("this is exactly why you don't leave agents unattended"), cut to pre-recorded fallback video
- **If Demo Phase 3 surfaces the bug faster than expected** → expand the reproducibility slide, dwell longer on `git log docs/`
- **If Demo Phase 3 drags** → keep slide 12 and 13 crisp; verification practices can be trimmed to just "read the diff"
- **If you have 5 extra minutes anywhere** → between slides 11 and 12, insert "what the agent can and cannot see" — where your data lives, what leaves your machine, consumer web vs. institutional gateway. This audience has real IRB and pre-publication data concerns that will surface in Q&A anyway.

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

**"You only showed us Claude Code — what about Copilot / Cursor / Windsurf?"**
The concepts are the same. The six pieces from slide 05 are in every tool. The four surfaces from slide 09 exist in every tool with different filenames. The mode-picker discipline works the same everywhere. If you're already using another tool, everything I showed you today translates — the filename for AGENTS.md changes, the location of the mode indicator changes, but nothing else does.

---

## Recovery notes

**If the agent produces a bad plan.** Perfect teachable moment. Do not try to fix it silently. Say aloud what's wrong with it, edit it in front of the room, explain the fix. The lesson is not "agents produce good plans"; the lesson is "the plan is a document you shape."

**If the agent refuses to write code in ask mode.** Ideal — that's the mode working as designed. Say so and move on.

**If the agent doesn't add type hints uninvited during Phase 1.** Adapt on the fly — point at whatever it *did* add without being asked (docstring style, argument defaults, imports, error handling), and use that as the scope-creep example instead. The lesson doesn't depend on the specific over-add.

**If the agent misses the bug in Act 3 even after being prompted.** Fine. Nudge more directly: "Look at the diurnal profile plot. Look at where the peak is. Look at the timestamps in the raw CSV." The lesson is that verification is on you either way; the agent as a diagnostic tool is nice-to-have, not essential.

**If you run out of time.** Cut slide 16 to just "write an AGENTS.md this week" — one sentence — and land on the handout. Do not skip slide 15 (reproducibility); it's the slide most attendees came for.

**If the room is completely silent during the bug reveal.** Good. Let them process. Do not fill the silence with more words.