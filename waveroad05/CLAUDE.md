# Wavelength roadmap — maintainer guide

This is the live roadmap published at **apps.theapexos.com/waveroad05/**. The page reads from `data.js`. To update the roadmap, you edit `data.js`, commit, and push to `main`. GitHub Pages auto-deploys within about 60 seconds.

This file is written for Claude Code. If you are Claude Code reading this: the human will describe a change in plain English ("shift CrewArcs to start Aug 1", "add a new item under Crew View", "the timeline now goes to March 2027"). Map their request to one of the patterns in the **Common operations** section below. The patterns show exactly which file, which lines, and what the before/after looks like.

---

## File structure

```
waveroad05/
├── index.html      ← the renderer. Do not edit unless changing visual layout.
├── data.js         ← THE FILE YOU EDIT. All roadmap content lives here.
└── CLAUDE.md       ← this file.
```

---

## Deploy

After any edit to `data.js`:

```bash
cd waveroad05
git add data.js
git commit -m "Roadmap: <describe the change>"
git push origin main
```

GitHub Pages auto-deploys. Confirm at https://apps.theapexos.com/waveroad05/ after ~60 seconds.

Always update `meta.lastUpdated` in `data.js` as part of the same commit so viewers can see the page is current.

---

## Local preview before pushing

```bash
cd waveroad05
python3 -m http.server 8000
```

Open http://localhost:8000/ in a browser.

Do **not** just double-click `index.html` to open it — browsers block loading `data.js` over the `file://` protocol, so the page will appear blank. The local server step is required.

---

## Data schema

`data.js` defines one global object: `window.ROADMAP_DATA`. It has six top-level keys:

### `meta` — page chrome

```js
meta: {
  title:        "Wavelength platform roadmap",          // big header on page
  pageTitle:    "Wavelength Platform Roadmap — ...",    // browser tab title
  eyebrow:      "Internal · waveroad05",                // small text above title
  subtitle:     "...",                                  // descriptive paragraph
  lastUpdated:  "May 25, 2026",                         // shown under subtitle
  footerLeft:   "...",                                  // bottom-left footer text
  footerRight:  "theapexos.com"                         // bottom-right footer text
}
```

### `timeline` — date range of the roadmap

```js
timeline: {
  start: "2026-05-01",   // ISO date (YYYY-MM-DD)
  end:   "2026-12-31"
}
```

The page renders one column per month from `start` to `end` inclusive.

### `phases` — background shading bands

```js
phases: [
  { id: "ea", label: "EA",            start: "2026-05-01", end: "2026-06-30" },
  { id: "ga", label: "GA",            start: "2026-07-01", end: "2026-09-30" },
  { id: "po", label: "Polish & plan", start: "2026-10-01", end: "2026-12-31" }
]
```

`id` must be one of `ea`, `ga`, `po` — these are the only phase colors defined in `index.html`'s CSS. Adding a 4th phase id requires adding matching CSS rules (see **Anti-patterns** below).

### `lanes` — the row groups

```js
lanes: [
  { id: "a360",   name: "A360 assessment · foundation",        icon: "ti-clipboard-data", tag: "Lane 01" },
  { id: "you",    name: "You view · individual experience",    icon: "ti-user",           tag: "Lane 02" },
  // ...
]
```

| field  | type   | notes                                                   |
|--------|--------|---------------------------------------------------------|
| `id`   | string | Internal lane identifier. Items reference this.         |
| `name` | string | Display name. Convention: `"<short name> · <subtitle>"`.|
| `icon` | string | Tabler icon class. Browse at https://tabler.io/icons   |
| `tag`  | string | Right-aligned label, e.g. `"Lane 01"`.                 |

Lanes appear in the order they're listed in this array.

### `items` — the bars on the chart

```js
items: [
  {
    id:        "a1",                                   // unique across all items + milestones
    lane:      "a360",                                 // must match a lane id above
    title:     "Cleanup, Roger wiring, ...",           // shown in row label
    wavShort:  "WAV-606 · 355–357 · misc",             // shown below title in mono font
    priority:  "high",                                 // "crit" | "high" | "med"
    start:     "2026-05-22",                           // ISO date
    end:       "2026-06-30",                           // ISO date
    detail:    "..."                                   // shown in modal when bar is clicked
  }
]
```

| field      | type   | required | notes |
|------------|--------|----------|-------|
| `id`       | string | yes      | Must be unique across all items AND milestones. Convention: lane initial + number (`a1`, `c4`, `l3`). |
| `lane`     | string | yes      | Must match a lane `id`. |
| `title`    | string | yes      | The row label (left column). |
| `wavShort` | string | no       | Mono-font subtitle. WAV ticket refs or one-line description. Omit if not useful. |
| `priority` | string | yes      | One of `"crit"`, `"high"`, `"med"`. Controls bar color. |
| `start`    | string | yes      | ISO date (`YYYY-MM-DD`). |
| `end`      | string | yes      | ISO date. |
| `detail`   | string | yes      | Full description shown in the modal on click. Can be a long paragraph. |
| `barLabel` | string | no       | Override the auto-computed bar text (e.g. `"5/22 → 6/30"`). Set to `""` to suppress. Omit to auto-generate. |

Items are grouped by lane and rendered in the order they appear in this array (within each lane).

### `milestones` — the diamond markers at the bottom

```js
milestones: [
  {
    id:        "m1",
    label:     "EA go-live",            // bold line above date
    shortDate: "6/30",                  // shown under label
    date:      "2026-06-30",            // ISO date (positions the diamond)
    title:     "EA go-live · 6/30",     // modal title
    priority:  "crit",                  // modal badge color
    dates:     "June 30, 2026",         // modal date display
    wav:       "Early Access launch",   // modal mono subtitle
    detail:    "..."                    // modal body
  }
]
```

Milestones sit at the end of their `date`. Clicking opens a modal just like items.

---

## Common operations

Each pattern below shows: the kind of request, which fields to change, and a before/after snippet.

### Edit an item's start or end date

**Request:** "Push CrewArcs to start Aug 1 instead of Jul 1." / "Extend Response Field to run through Jan 31."

**Edit:** the item's `start` or `end` field. The bar position, bar label, and modal date display all auto-update.

```js
// Before
{ id: "c4", lane: "crew", title: "CrewArcs (5): ...", start: "2026-07-01", end: "2026-09-30", ... }

// After
{ id: "c4", lane: "crew", title: "CrewArcs (5): ...", start: "2026-08-01", end: "2026-09-30", ... }
```

If extending the `end` past the current `timeline.end`, also extend `timeline.end` (see **Extend the timeline** below).

### Change an item's priority

**Request:** "Bump UIP wiring to Critical." / "Drop Quick Surveys to Medium."

**Edit:** the item's `priority` field. Use exactly `"crit"`, `"high"`, or `"med"`.

```js
// Before
{ id: "l3", lane: "launch", title: "UIP wiring + relativized scores", priority: "high", ... }

// After
{ id: "l3", lane: "launch", title: "UIP wiring + relativized scores", priority: "crit", ... }
```

### Edit an item's title, subtitle, or detail text

**Request:** "Reword the CrewArcs title to remove the parenthetical." / "Tighten the Response Field modal text."

**Edit:** the `title`, `wavShort`, or `detail` field directly. Plain string replace.

### Add a new item

**Request:** "Add an item under Crew View called 'Crew analytics export' for Aug 15–Sep 30, High priority, no WAV tickets yet."

**Edit:** add a new object to the `items` array. Insert it in the order you want it to appear (items within a lane render in array order).

```js
// Add this object into the items array, ideally near the other crew items:
{
  id: "c7",                                            // pick the next unused id
  lane: "crew",                                        // existing lane id
  title: "Crew analytics export",
  wavShort: "",                                        // empty if none yet
  priority: "high",
  start: "2026-08-15",
  end: "2026-09-30",
  detail: "Description of what this workstream covers — what's included, what's not, what gates it."
}
```

Check that the new `id` doesn't collide with any existing item or milestone.

### Remove an item

**Request:** "Drop the Editable Categories item."

**Edit:** delete the entire item object from the `items` array (including the trailing comma if it had one, and the closing `}`).

If you're unsure whether the item might come back, comment it out instead by wrapping in `/* ... */` rather than deleting.

### Add a new lane

**Request:** "Add a sixth lane for Marketing & Ops work."

**Edit:** two places.

First, the `lanes` array:

```js
lanes: [
  // ... existing 5 lanes ...
  { id: "mktg", name: "Marketing & ops · go-to-market", icon: "ti-target-arrow", tag: "Lane 06" }
]
```

Then add items under that lane by setting `lane: "mktg"` on each new item.

### Add a new milestone

**Request:** "Add a milestone for 7/15 covering the Quick Surveys ship date."

**Edit:** add an object to the `milestones` array. Position is auto-computed from `date`.

```js
{
  id: "m4",                              // unique
  label: "Quick surveys ship",
  shortDate: "7/15",
  date: "2026-07-15",
  title: "Quick surveys ship · 7/15",
  priority: "high",
  dates: "July 15, 2026",
  wav: "Outreach + speaking",
  detail: "Description of what ships on this date and what depends on it."
}
```

### Edit or remove a milestone

Same pattern as items — edit the fields directly, or delete the whole object from the `milestones` array.

### Extend the timeline

**Request:** "The roadmap now runs through March 2027."

**Edit:** `timeline.end`.

```js
// Before
timeline: { start: "2026-05-01", end: "2026-12-31" }

// After
timeline: { start: "2026-05-01", end: "2027-03-31" }
```

You may also want to:
- Extend the last `phase.end` to match the new timeline end (otherwise the post-phase area renders without background shading).
- Update `meta.subtitle` if it mentions the date range.
- Add items with start dates in the new range.

### Update the "Last updated" date

**Request:** "Update the timestamp." (Or just do this whenever you push.)

**Edit:** `meta.lastUpdated`. Use the format "Month Day, Year".

```js
meta: {
  // ...
  lastUpdated: "June 8, 2026",
  // ...
}
```

### Change the title, subtitle, or eyebrow

**Edit:** the corresponding field in `meta`.

```js
meta: {
  title:    "Wavelength platform roadmap — Q3 push",   // changed
  eyebrow:  "Internal · waveroad06",                   // changed for a new version
  subtitle: "...",                                     // updated narrative
  // ...
}
```

### Override a bar's auto-generated date label

**Request:** "Show 'EA → GA' instead of dates on the Response Field bar." / "Hide the date label on this short bar."

**Edit:** add a `barLabel` field to the item.

```js
// Custom text:
{ id: "y2", title: "Response Field", barLabel: "EA → GA → Polish", ... }

// Suppress the label:
{ id: "o1", title: "Quick surveys", barLabel: "", ... }

// Auto-generate (default — just omit the field):
{ id: "a1", title: "Cleanup", ... }   // no barLabel field
```

---

## Anti-patterns and gotchas

**Do not invent new priority values.** Only `"crit"`, `"high"`, `"med"` have styling. A typo like `"critical"` or `"low"` will render as an unstyled bar.

**Do not invent new phase ids.** Only `ea`, `ga`, `po` have CSS rules in `index.html`. To add a new phase color, you'd need to add CSS rules — that's an `index.html` edit, not a `data.js` edit.

**Do not reuse `id` values.** Every item and milestone must have a unique `id`. Reusing one will break the modal lookup for whichever object comes second.

**Do not use ambiguous date formats.** Always use ISO format `YYYY-MM-DD`. `"5/22/2026"` will not parse correctly.

**Do not break the JSON-like syntax.** The file is JavaScript, but the data inside `window.ROADMAP_DATA = {...}` follows object/array syntax. Watch for:
- Missing commas between fields or array entries
- Unescaped quotes inside strings (use `\"` or wrap the string in different quotes)
- Trailing commas are fine in modern JS, but missing commas will break

**Do not edit `index.html` for content changes.** All content lives in `data.js`. If you find yourself wanting to edit `index.html`, you probably want to add a field to the data schema instead — flag it and we'll discuss.

**Do not commit without previewing locally** if the change is structural (new lane, new phase, timeline extension). Date edits and text edits are low-risk; structural edits should be verified at `localhost:8000` before pushing.

---

## When in doubt

If a request doesn't fit one of the patterns above, surface it before making the edit. Examples that warrant a check-in:

- "Make the bars interactive — let users drag to reschedule." (renderer change, not data)
- "Add a checkbox to mark items complete." (schema addition + renderer change)
- "Show two timelines side by side." (significant renderer rework)
- "Pull the data from Google Sheets instead." (architecture change)

For anything ambiguous, ask "is this a data change or a structure change?" — data changes go in `data.js`, structure changes go in `index.html` and need more scrutiny.
