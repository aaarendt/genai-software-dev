# Working With a Coding Agent

Target audience: Summer institute participants — researchers using AI/ML as a research tool, mixed coding fluency, diverse domains
Duration: 60 minutes

## How to render this deck (instructions for the slide generator)

**This document is a design brief, not slide copy.**

**Two-pass workflow.** This deck is built in two passes, and SLIDES.md governs only the first.

- **First pass (this file): content and structure only.** Build the deck to a publishable-looking, intentional state using only typography, layout, color palette, and accent following the specified design templates. Use no photographs and no decorative icons in this pass. The deck should look complete on its own — if it had to be presented tomorrow with no images, it should feel finished rather than naked.
- **Second pass (separate VISUALS.md): additive visual elements.** After the first pass is rendered and rehearsed, VISUALS.md specifies photographs, diagrammatic accents, and iconography to *add* to existing slides.
- **Do not anticipate the second pass during the first.** If a slide feels visually sparse, the correct response is stronger typography or layout, not a placeholder.

**General rules:**

- The **Key message** line is the main idea to convey in the slide. The title of the slide is usually extracted as a subset of the key message.
- **Bullets** are suggested layout of content and not necessarily menat to be verbatim on the slide.
- **Note to self** lines are for the speaker only. Never render them on the slide.
- Default to one anchoring element per slide: a phrase, a number, or a small structural composition. When in doubt, less text.
- Maintain visual continuity: consistent type scale, generous whitespace, and the gold accent from the title slide.
- Any other text is general context that should be used to thoughtfully craft the content of the slide. Be concise but don't be afraid to include some amount of text - just enough to get the key message across. I favor complete sentences over em-dashes. Avoid the short, pithy one-liners. Stay with more scientific writing and complete sentences.

## 01-title

Title slide with UW branding.

- Presenter names: Anthony Arendt, Landung (Don) Setiawan
- July 29, 2026
- Session title: Generative-AI for Software Development
- AI-in-Practice Summer Institute, University of Washington eScience Institute

## 02-opening-recognition

- Key message: Generative AI is being used increasingly for code development. One of the most useful ways to learn this is by starting with some existing code and seeing how gen-AI can be used to improve it. 
- I have many poorly formatted and incomplete notebooks on my laptop right now, and expect you do too!
- Today we are going to take one of those notebooks and apply some gen-AI methods to see what is possible in just a short amount of time. 
- Note to self: Show the messy notebook on the projector as this slide appears. 

## 03-what-this-hour-is-not

- Key message: The purpose of this session is not to show how AI will write code for you from scratch, rather it is to show you how we can work with an agent in a code base to improve and increase the reproducibility and robustness of the work that we're doing. 
- Bullets:
  - We're going to work with an agent in a codebase we care about
  - We will regard the agent as a coworker
  - Three acts: how it works, how you shape it, how you keep it trustworthy

## 04-chat-vs-agent

- Key message: The chat experience many of us have with LLMs is around answering questions. An agent is different because it reads your files, runs your code, and edits your project.
- Bullets:
  - Same LLM underneath, but different harness around it
  - Saying "I'm using Claude" is under-specified: browser Claude, Claude Code, and Claude in Cursor all behave differently
  - The harness, not the model, is what has changed in the last two years

## 05-six-pieces

Every tool has all of these six components:
- Bullets:
  - LLM backbone — the language model itself; the thing generating text
  - Tool use — the ability to read files, edit them, run commands
  - Agent loop — the software that lets it decide whether to call another tool or finish
  - Project memory — a file the agent reads on startup so it knows about your codebase
  - MCP servers — a standard way to plug in external things like databases, calendars, APIs
  - Skills — reusable procedures for specific kinds of tasks
  - Every feature in every product maps to one of these. Switching tools is a configuration exercise, not a re-learning exercise

## 06-trained-in-vs-prompt

- Key message: Trained in vs. in the prompt.
- Bullets:
  - Trained in: Python, common libraries, general patterns, dialogue format, when to stop
  - In the prompt: your data's quirks, your lab's conventions, your specific goal
  - You control one side of that line. Everything we do in the next 45 minutes will focus on things we can control in the prompt.
Render as two-column layout with the phrase as headline. This is the mental model 

## 07-demo-setup

- We will be refactoring a messy notebook that is processing weather station data. 
- Bullets:
  - What the notebook does: load, clean, resample, forecast, plot
  - Defining terms: refactor means reorganizing working code without changing what it does. 
  - What we're going to have the agent do: propose a plan, extract a module, and help us verify our code.
  - Ties to the time series methods you saw earlier in the week — this is the engineering scaffolding those methods sit on

## 08-demo-phase-1

- Bullets:
  - Confirm you're in ask/plan mode before typing anything — show the indicator on screen
  - Live prompt to agent: read the notebook, propose a refactor plan, no code yet
  - While it works: notice it reads the whole notebook. Notice whether it asked clarifying questions — most don't, and that's a failure mode, not a virtue
  - When plan returns: agent likely added things you didn't ask for — type hints, tests, extra structure. This is a live example of the scope-creep failure mode.
  - Push back visibly. Edit the plan. The plan is a document you shape, not a formality.
- Note to self: When the plan comes back, point at any scope-creep additions on screen and name them — "See these `-> pd.DataFrame` arrows? Those are type hints. I didn't ask for them." This is the "trained to be over-helpful" pattern surfacing live. Slide stays up during the demo pause; talk over it.

## 09-four-surfaces

- Key message: Four Durable Places to Shape Agent Behavior.
- Bullets:
  - Context documents (AGENTS.md) — always loaded on startup; the facts and conventions the agent should always have in hand when working in this project
  - Skills — task-triggered procedures; the agent picks them up when the work matches. Good for "when analyzing time series, always check for missing values and irregular sampling."
  - Rules — path-scoped constraints that fire based on which files are being touched; hard limits rather than helpful suggestions. Good for "code in `analysis/` must have a test."
  - Custom agents — distinct personas with their own tool access and voice; useful when you want a narrower, more focused agent for a specific job like schema review.
  - Taxonomy is portable across tools; file names differ
  - Today we'll use the first one seriously and name the others
- Note to self: Render as a 2x2 or four-column table with generous whitespace. The extra sentences per surface are speaker cues, not destined to be rendered on the slide; each row on screen should be terse. This is Section 3 of the wider curriculum compressed to a single slide — resist the urge to explain each one deeply beyond the one-example gloss.

## 10-agents-md-live

AGENTS.md typically has ten or so lines. This changes how the agent behaves.
- Bullets:
  - What this project is
  - Preferred libraries
  - Timestamps are UTC unless stated (seeds Act 3)
  - Don't add type hints unless asked (grounded in what just happened on slide 10)
  - Version-controlled — team asset, not personal preference
  - Cross-vendor convention — the file travels with the code
- Note to self: Write the file live in the editor after this slide appears. Commit it. The UTC line seeds the bug in Act 3 — do not skip it. The "no type hints" line will land harder because the room just saw the agent add them uninvited.

## 11-act2-recap

- Key message: The agent read your files, followed your plan, and edited your code. You supervised. That is the full shape of it.
- Bullets:
  - We switched to agent mode, prompted it to extract the cleaning logic into a module, and it did exactly that
  - The chat told us what the agent claims it changed, and the diff is where we confirmed it
  - The code looks right, but we should verify it to be sure
- Note to self: Recap slide — appears after the live demo, not during it. Let it breathe. The third bullet sets up Act 3 without telegraphing what's coming.

## 12-bug-in-code

Key message: The agent preserved the bug faithfully. It didn't introduce it, but it also didn't catch it.
Bullets:
- Bullets:
- The bug was in the original notebook. The refactor moved the pandas operations verbatim.
- Summary statistics were unaffected. Only the domain-informed look at the diurnal plot surfaced it.
- The AGENTS.md convention we wrote earlier (timestamps are UTC) made the fix traceable rather than mysterious.
This is the shape of the collaboration: the agent handles the code, you handle the domain.

## 13-plausible-code

- Key message: Why do we need to verify our code?
- Bullets:
  - This is not a question of whether the agent is trustworthy — it generally produces plausible, working code
  - The agent does not know the specifics of our data — its quirks, its edge cases, its domain context
  - It also lacks the scientific domain knowledge we bring as researchers — it cannot judge whether a result is physically reasonable or scientifically meaningful
  - Verification is not a safety check on a bad tool. It is the responsibility that stays with the human researcher.
- Note to self: The core teaching beat of the whole hour. Frame it as a genuine question the audience should be sitting with, not a verdict. Let the final point land in silence.

## 14-verification-practices

- Key message: There are multiple approaches. Today we used two.
- Bullets:
  - Read the diff, not the chat
  - Push back — the agent is a coworker, not an oracle. Push back includes "no, you're in the wrong mode" or "no, you did more than I asked" — half of what looks like the agent going rogue is a permissions or scope problem.
There are more advanced patterns — evals, test-first workflows, structured uncertainty flagging. The handout has starting points if you want to go deeper.

## 15-reproducibility

Key message: The conversation is scaffolding. The artifact is the science.
Bullets:
- LLMs are stochastic; science demands reproducibility. That tension is real. 
- The resolution: the process isn't reproducible, however the artifacts are.
- Your git repo, not your chat log, is the record.
- You can optionally commit plans, review notes, and validation outputs alongside code. git log docs/ reads like a lab notebook.
- it's good practice to log model, version, and date in your methods section, the way you'd cite any tool.
- Pin your dependencies, because AI-generated code often assumes packages it didn't declare.

## 16-where-to-go-next

Key message: Write an AGENTS.md for one of your own projects. This week.
Bullets (speaker cues):

Pick a project you're actively working on
Ten lines is enough — conventions, preferences, what not to do
Commit it to the repo so it travels with the code
Then use an agent on that project once, and notice what changed

---
