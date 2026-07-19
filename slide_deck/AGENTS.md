# Slide Deck — Agent Context

This directory contains a presentation built with UW and NSF Cloud Bank branding.

## Repository layout

- `content/` — first-pass slide HTML files (text and structure only, no images)
- `content-with-visuals/` — second-pass slide HTML files (adds photos, diagrams, and icons)
- `assets/` — shared images and other media
- `shared/` — shared CSS and layout files
- `build/` — final output; `index.html` is the assembled presentation

## Key files

- **`SLIDES.md`** — the primary design brief. It defines the deck's content, slide order, speaker notes, and layout guidance. Start here when adding or revising slides.
- **`VISUALS.md`** — governs the second pass; specifies photographs, diagrams, and iconographic elements to add to existing slides after the first pass is complete.
- `build.sh` — stitches all HTML files in `content/` into `build/index.html`
- `build-visuals.sh` — does the same for `content-with-visuals/`

## Two-pass workflow

1. **First pass:** Use `SLIDES.md` to generate slides in `content/`. Typography, layout, color, and accent only — no images or decorative icons.
2. **Second pass:** Use `VISUALS.md` to generate enhanced versions in `content-with-visuals/`. This pass is additive; do not modify first-pass files.

## Design standards

All slides must follow the `uw-slides` plugin conventions in Claude Code. When in doubt about design decisions, consult that plugin for authoritative guidance on color tokens, typography, layout patterns, and logo usage.
