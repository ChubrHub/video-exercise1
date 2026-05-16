# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A behavioral-economics browser game with two parallel editions, each shipped as a single self-contained HTML file. No build step, no dependencies, no package manager. Each file has inline `<style>` and `<script>` and runs by double-clicking it or hitting the deployed URL.

- `v1.html` — **Hemingway & Munger**, the adult edition. **Frozen.** Do not edit unless explicitly asked to ship a v1.1.
- `v2.html` — **Lightning & Doc**, the kid edition (ages 4–8, parent-read). Currently identical to `index.html`. Frozen the same way once it's "locked."
- `index.html` — the "current / latest" edition that GitHub Pages serves at the root of the custom domain. Right now `index.html === v2.html`. When iterating, edit `index.html`; when locking a new version, copy it to a numbered snapshot (`v3.html`, etc.) and commit both.

The published URL is **https://apps.theapexos.com** (GitHub Pages on `main`, custom domain via CNAME at GoDaddy).

## Run / develop

```sh
# Just open the file. No server needed.
start index.html              # Windows
```

The whole game is in one file. To make a change: edit the HTML, save, refresh the browser. There's no build, no transpile, no test suite. Verification is manual playthrough.

For the dev-loop in this harness, the Launch preview panel shows the current `index.html` automatically when it's edited.

## Architecture inside each edition

Both `v1.html` and `v2.html` share the same skeleton. The differences are content (scenarios, copy, personas) and palette (dark/jargony vs light/kid-friendly).

### Phases (state machine)

```
intro → scenario → feedback → (interstitial)? → scenario → ... → epilogue
                                     ↑
                                bonus scenarios insert here at specific turns
```

`state.phase` drives `render()`, which dispatches to one of `renderIntro`, `renderScenario`, `renderFeedback`, `renderInterstitial`, `renderEpilogue`.

### Data shape

- `SCENARIOS[]` — 10 regular turns, each with `obvious` (short-term/present-self choice) and `betterPath` (long-term/future-self choice).
- `BONUS_SCENARIOS[]` — 2 "teachable moment" rounds inserted via `insertAfterTurn`. Both options give positive effects; the `obvious` one is the *trap* (looks like a future-self pick, isn't).
- `ACHIEVEMENTS[]` — predicates over `state.history` and final stats; surface as badges in the epilogue.
- `BADGE_ICONS{}` — inline SVGs keyed by achievement name. Updating an achievement name requires updating both.

### Slot randomization

A/B button positions are randomized per scenario via `randomizeSlots()`. `state.slots = { a: 'obvious'|'betterPath', b: ... }`. All choice logic goes through `state.slots[slot]` → `choiceKey`. **Never assume A = obvious.** Achievements test by `scenarioId + choiceKey`, not by slot letter.

### Persona voice attribution

In **v1**, hints are abstract ("inner voice on A/B"). In **v2**, hints are attributed to characters: `obvious` is always **Lightning McQueen**'s voice, `betterPath` is always **Doc Hudson**'s voice. The voice cards in the feedback render are colored red/blue accordingly. This is hard-coded in `renderFeedback`'s `voiceRow` based on `choiceKey`.

### Compound mechanic

`compoundScore` starts at 100. Future-self picks apply a multiplier (`compoundMult`); short-term picks add a flat (`compoundFlat`). Three consecutive `betterPath` picks on regulars set `state.streakArmed`, which adds a one-shot ×1.25 on the next future-self multiplier. **Bonus rounds never break or consume the streak** — they're explicitly no-penalty.

### Delayed payoffs

Some `betterPath` choices schedule `payoffs: [{ atTurn, label, effects }]`. These fire as interstitial cards at the start of the named regular turn, before that scenario's choice is presented. This is how the magic-penny/sticker scenario "shows" compounding mid-run.

## Two-edition discipline

When the user asks for a new iteration:
1. Edit `index.html`. Don't touch `v1.html` or `v2.html` unless asked.
2. When the user says to "lock in" a version, copy `index.html` to a new numbered file (`v3.html`, etc.) and commit both in one go.
3. Old versioned files stay deployable at `apps.theapexos.com/vN.html`.

Both versioned files are functionally independent — they share no code. Changing one never affects the other.

## Deployment

- GitHub Pages serves the `main` branch root.
- Custom domain `apps.theapexos.com` via CNAME at GoDaddy → `chubrhub.github.io`.
- A `CNAME` file at the repo root holds the domain string; GitHub manages it automatically when the custom domain is set in repo Settings → Pages.
- Pushing to `main` redeploys in ~30–60 seconds. No CI/CD configuration in the repo.

## Conventions specific to this repo

- Single-file discipline. If a feature would push an edition's HTML past ~1500 lines, consider whether the user really wants the file to grow before splitting — they've explicitly chosen "no build" as a constraint.
- Verification is manual. There is no test suite. After a non-trivial change, do a static walkthrough of the state machine (intro → all-betterPath run → all-obvious run → at least one bonus round) and note expected outcomes in the response.
- The user prefers terse, decisive responses and concrete forward motion over option enumeration. End-of-turn summaries should be one or two sentences.
