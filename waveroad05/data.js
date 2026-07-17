// =========================================================================
// Wavelength platform roadmap — data source
// =========================================================================
// This file is the source of truth for everything that appears on the
// roadmap page. Editing here, committing, and pushing to main is all that's
// needed to update apps.theapexos.com/waveroad05/.
//
// See CLAUDE.md (in this folder) for the schema reference and step-by-step
// examples for every common change.
// =========================================================================

window.ROADMAP_DATA = {

  // --- Page chrome ---------------------------------------------------------
  meta: {
    title: "Wavelength platform roadmap",
    pageTitle: "Wavelength Platform Roadmap — May–Dec 2026",
    eyebrow: "Internal · waveroad05",
    subtitle: "May 2026 → December 2026, organized into five workstream lanes (A360 Assessment, You View, Crew View, Launch View, Other) and gated by three milestones — EA Go-Live on 6/30, GA Go-Live on 9/30, and Polish + Future Planning on 12/31. Click any bar for workstream detail. Filter chips below scope the view by priority.",
    lastUpdated: "May 25, 2026",
    footerLeft: "May–Dec 2026 · 23 workstreams across 5 lanes · 3 milestone go-lives",
    footerRight: "theapexos.com"
  },

  // --- Timeline range ------------------------------------------------------
  // The roadmap spans these dates inclusive. Extend `end` to grow the timeline.
  timeline: {
    start: "2026-05-01",
    end:   "2026-12-31"
  },

  // --- Phases --------------------------------------------------------------
  // Background shading bands across the timeline.
  // id must be one of: ea | ga | po (these are styled in index.html CSS).
  // Adding a new phase id requires adding matching CSS rules.
  phases: [
    { id: "ea", label: "EA",             start: "2026-05-01", end: "2026-06-30" },
    { id: "ga", label: "GA",             start: "2026-07-01", end: "2026-09-30" },
    { id: "po", label: "Polish & plan",  start: "2026-10-01", end: "2026-12-31" }
  ],

  // --- Lanes (rows are grouped by lane) -----------------------------------
  // icon = any Tabler icon class. Browse at https://tabler.io/icons
  lanes: [
    { id: "a360",   name: "A360 assessment · foundation",          icon: "ti-clipboard-data", tag: "Lane 01" },
    { id: "you",    name: "You view · individual experience",      icon: "ti-user",           tag: "Lane 02" },
    { id: "crew",   name: "Crew view · team lead experience",      icon: "ti-users",          tag: "Lane 03" },
    { id: "launch", name: "Launch view · amplifiers & growth",     icon: "ti-rocket",         tag: "Lane 04" },
    { id: "other",  name: "Other · cross-cutting & future planning", icon: "ti-stack-2",      tag: "Lane 05" }
  ],

  // --- Items (the bars) ----------------------------------------------------
  // priority must be one of: crit | high | med
  // lane must match an id from the lanes array above.
  // Items appear in the order they're listed here, grouped by lane.
  items: [

    // --- A360 ASSESSMENT --------------------------------------------------
    {
      id: "a1",
      lane: "a360",
      title: "Cleanup, Roger wiring, Arbiter rename, prev. refiners",
      wavShort: "WAV-606 · 355–357 · misc",
      priority: "high",
      start: "2026-05-22",
      end:   "2026-06-30",
      detail: "Address open items: prompt cleanup and misaligned output, wire Roger into all assessment output fields (discussed several weeks ago), rename A5 (formerly C5) Calibrator to Arbiter (WAV-606) — the rationale being to reduce collision with the Calibrate activity in ARC-EQ. Complete previously scoped refiners WAV-355, 356, 357 (may be stale after sitting; first three already scored and wired in the Assessment Algorithms Live spreadsheet). The WAV-XXX placeholders for prompts and Roger output-wiring need real ticket numbers before they're trackable."
    },
    {
      id: "a2",
      lane: "a360",
      title: "New refiners: Z5 · D5 · E5+E5x",
      wavShort: "Social energy · drives · routing",
      priority: "crit",
      start: "2026-05-25",
      end:   "2026-06-30",
      detail: "Three refiners deferred to this window. Z5 is crucial — it's the first real read on Social Energy dynamics. D5 is helpful and provides a clearer Drives signal. E5+E5x is necessary for clear directional diagnostics — it covers Stimulus Routing and Emotional Gravity together. Done by 6/30 means each refiner is built, scored, wired, and producing output aligned with the cleanup work happening in parallel."
    },
    {
      id: "a3",
      lane: "a360",
      title: "Refiners: Q5 · V5 · H5",
      wavShort: "WAV-288 · 326 · 346 · 417 · 444 · 465 · 466",
      priority: "crit",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "Second batch of refiners. Q5 is the Calibration refiner and is necessary for App full functionality — without it the You View loop is incomplete. V5 brings Team/Crew specificity. H5 contributes additional directional diagnostics. Q5 ties into the ARC-EQ Calibrate activity, so this work has a real dependency on Response Field progress and on Z5/D5/E5 from the EA window."
    },
    {
      id: "a4",
      lane: "a360",
      title: "Assessment retake versioning",
      wavShort: "Master file + pinned preferred lens",
      priority: "high",
      start: "2026-05-25",
      end:   "2026-09-30",
      detail: "Up to five retakes per level (Check, Map, etc.). The system generates a master file averaging all takes. The user pins their preferred operating lens. All calculation happens on the master (average) file, but output is delivered through the preferred lens. Example: if pinned Prime Stance is Navigator but the real (averaged) Prime is Anchor, the output reads as 'As a Navigator with strong Anchor influences, you…' — leading with Nav and grounding in Anc."
    },
    {
      id: "a5",
      lane: "a360",
      title: "Editable categories + structural refinement",
      wavShort: "PM/Architect signoff workflow",
      priority: "med",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "Make all categories, codes, and formulae editable by Charlie. Push to production requires PM and/or Architect signoff (a real workflow, not just a label). A necessary but not quick lift. Pairs with assessment structural refinement, scoped after EA learnings come in."
    },

    // --- YOU VIEW ---------------------------------------------------------
    {
      id: "y1",
      lane: "you",
      title: "You View app — Base · Ops · Specs · Aims · Source",
      wavShort: "WAV-288 · 326 · 465 · 466",
      priority: "crit",
      start: "2026-05-25",
      end:   "2026-06-30",
      detail: "App foundation building on Casey's sketch. Base section: rate energy (depleted ↔ resourced) and rate activation (reserved ↔ expressed) as two separate sliders — they're different valences and not on the same axis. Confirm or define the task. Sync orientation without naming the stance — use colloquial framing (exploratory, social, get-stuff-done). Get advice from Roger on how to align. Ops, Specs, Aims, Source are expandable sections drawing from CoreCheck_AlfaNav_Bridge_Map."
    },
    {
      id: "y2",
      lane: "you",
      title: "Response Field (ARC-EQ) — NNARC + E5x + gating",
      wavShort: "WAV-416 · 417 · 444",
      priority: "high",
      start: "2026-07-01",
      end:   "2026-12-31",
      detail: "Rename from ARC-EQ to Response Field — echoes the EQ → NQ shift in the field (broader cognitive + emotional resources, not just emotion). Process: Notice-Name-Attune-Route-Calibrate, with Q5 doing the Calibration. Education: E5x Emotional Gravity (Sensemaking, Working, Social Standing, Boundaries, Significance — where attention is drawn) and E5 Stimulus Routing (Baseline-Sensitivity-Reactivity-Inertia — how stimuli get routed). Gating is primary: IMP-React-Respond-Restore mapped to System 1 / System 2 plus an Offramp."
    },
    {
      id: "y3",
      lane: "you",
      title: "My Wavelength: The Clear Signal",
      wavShort: "WAV-605 · Aims capstone",
      priority: "med",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "Folded into and made capstone of the Aims section in You View. Draws from existing data plus more developed content surfaced through this window."
    },
    {
      id: "y4",
      lane: "you",
      title: "You View desktop — enhanced insights",
      wavShort: "WAV-418 · 273 · 454 · 362",
      priority: "high",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "Desktop expansion of You View. WAV-418: depth and flexibility highlights, 'superpowers' with watchouts, all delivered through Use-Improve-Protect — concentration within Stance family especially with high deltas to other stances, low barriers between stances (dyad/triad/quadrat/pentad options), concentration within facet. WAV-273: Raw, Relative, and Potential scores in a rotating panel for individual and team lenses. WAV-454: 'Peak' added to cross-domain mapping as a Turbo icon alongside Energy (Fuel) and Drive (Horsepower) — what you can do in a sprint with prep + recovery. WAV-362: gauges on Energetic Stances and full range of all 25 with U-I-P per stance."
    },

    // --- CREW VIEW --------------------------------------------------------
    {
      id: "c1",
      lane: "crew",
      title: "Team member crew view (app)",
      wavShort: "Refines click-on-individual · WAV-412 tie-in",
      priority: "high",
      start: "2026-05-25",
      end:   "2026-06-30",
      detail: "Refinement of the current click-on-individual view wired into Crew View. Layout: avatar or uploaded photo plus name on the left. To the right: Roger chat field, team message board, Team icons + Team Pulse info (Stress Signals tie-in WAV-412), quick link to last-used Amplifier or Response Field training. Below avatar/name: Prime icon with Energetic Stance · Energetic Signature (e.g. Navigator · Discoverer), Shift slightly smaller, Pivot slightly smaller. Then horizontally: brief synthesis box (three lines visible, expandable, Roger icon for feedback). Then Response Field info row — current state, Shift Load (Work Signal:Shift Index, WAV-451), range, drift suggestions/watchouts, callout for ARC-EQ aspects to use. Then Execution Rhythm gauges. Then Social Energy gauges. Then top suggested + four Amplifiers / Response Field in-process (syncs with app and vice versa). Then all ten Operating Signals with Initiate / Integrate toggle."
    },
    {
      id: "c2",
      lane: "crew",
      title: "Crew desktop EA — team lead foundation",
      wavShort: "WAV-284 · 288 · 410 · 411 · 465 · 466",
      priority: "crit",
      start: "2026-05-01",
      end:   "2026-06-15",
      detail: "Team Lead edition for Early Access. Wire into live team member scores. Updated gauges (WAV-465/466). The big deal: the vast majority of this is pulling in existing data and gauges for individuals, providing simple averages for the group, and adding sorts. Execution Rhythm (WAV-410, 411): each person listed in the leftmost column with Initiate / Coordinate / Integrate / Modulate / Punctuate gauges left to right, hovers on each header explaining the phase, plus Aggregate / Expressed / Reserved for the team in each area at the top — focusing the Team Lead on team characteristics first. Sortable by person. Energetic Stance: keep the heat chart approach for coverage, add hovers with KB definitions for each Nav/Anc/Cat/Sen/Sag and each phase, add Prime/Shift/Pivot drill-in on individual initials, subsidiary heat charts for Shift and Pivot, aggregate heat chart with sized icons. Social Energy: rework to follow ETS / BPS / EBA (change S→C for charge) / EFS / EPS; keep bars for EBA hover only; lead with GAP; Glance gauges ideal. Operating Signals: sortable by person with gauges, keep Initiate / Integrate toggle, Aggregate / Expressed / Reserved on top."
    },
    {
      id: "c3",
      lane: "crew",
      title: "Team groupings + crew read",
      wavShort: "WAV-346 · 607",
      priority: "high",
      start: "2026-06-01",
      end:   "2026-06-30",
      detail: "Team Groupings Option (WAV-346) with clarified permissions — Charlie has full access to all for now; others can only view Wavelength. Each team config saved and comparable based on aggregates and averages across domains, including CrewArcs. Crew Read (WAV-607) placeholder pending Charlie completion: sortable by person with gauges, team Aggregate / Expressed / Reserved on top."
    },
    {
      id: "c4",
      lane: "crew",
      title: "CrewArcs (5): Clarity · Competence · Cohesion · Coordination · Candor",
      wavShort: "Team-level proto-Prismatics X5s",
      priority: "high",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "Crew Architecture — five team-level proto-Prismatics X5s. Clarity = Narrative Coherence + Compelling Direction. Competence = Capability Activation + Strong Structure. Cohesion = Practice Vitality + Supportive Context. Coordination = Strategic Pivot Velocity + Collective Cognition. Candor = Reality Recognition + Mutual Trust. Each comes with: overall selected crew gauge plus available individual view, composite and individual score (simple derivations), Development or TURBO gauge showing boost view for potential gains and actual progress. Most of this is simple linking or averaging of existing data from team members — same pie, different slicing."
    },
    {
      id: "c5",
      lane: "crew",
      title: "Crew desktop GA — full lead + CHRO + applicant",
      wavShort: "WAV-451 · Lou Adler ranking",
      priority: "high",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "Purpose Alignment extension of Clarity: measures whether the team's natural drives match the work asked of them and whether they have capacity to close the gap. Inputs: Team Lead's Shared Direction Statement translated into D5 language; Drive Epicenter (5) and Purpose Anchor (25) specificity at team aggregate top/second and individual drilldown; gauges and Social Energy-like output. Team Grouping Ratings: basic analysis of expected crew performance via Roger clarifying questions on team purpose and task structure. Drive alignment inference. Shift Load (WAV-451): Work Signal:Shift Index updates on individuals and team. CHRO / Job Applicant view using Lou Adler principles for resume ranking — both without A360 (speculative ranking plus translation engines for other assessments) and with A360 (core categories, then post-Stance-shift Prime→Shift and Shift→Pivot based on durability projections plus Amplifier development and deployment)."
    },
    {
      id: "c6",
      lane: "crew",
      title: "Plain language + own/dyad/small team pulses",
      wavShort: "Self-selectable crew",
      priority: "med",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "Own and dyad/small team views and pulses — the individual sets their cross-functional crew distinct from the formal team config. Cross-cutting collaborators often matter more than the formal team for day-to-day work, so this surfaces what's actually happening in the group people work with. Plus plain-language surfacing of stance / orienting / framing and Use-Improve-Protect in Crew View."
    },

    // --- LAUNCH VIEW ------------------------------------------------------
    {
      id: "l1",
      lane: "launch",
      title: "Amplifier module + UIP landing",
      wavShort: "WAV-365 · 603",
      priority: "high",
      start: "2026-05-25",
      end:   "2026-06-30",
      detail: "Launch View EA basics. Amplifier module illustration (WAV-365, 603) with scores wired into the actual assessment for individuals (pitching gauges). Provide base info on each amplifier from knowledge-base documents — at least enough that clicking shows what each is. Use-Improve-Protect landing so people see additional resources beyond the assessment output. Aim is a landing page for the links in UIP — not the full module, just enough to demonstrate that we're not just telling people what to do, we're giving them the resources."
    },
    {
      id: "l2",
      lane: "launch",
      title: "Five amplifier epicenters + training",
      wavShort: "WAV-603 · A360 Pro · 3 levels deep",
      priority: "high",
      start: "2026-07-01",
      end:   "2026-09-30",
      detail: "The five Amplifier Epicenters and training ship with A360 Pro up to three levels deep (WAV-603). Epicenter level (Framer, Tactician, Beacon, etc.) plus the module level beneath (TAC-1, BEA-4, etc.). Each amplifier ties into Use-Improve-Protect via specific connections: an associated Energetic Stance for Use (get your orientation right), the amplifier itself for Improve (skill development), and the Response Field for Protect (intentional evaluation and deployment). Scoring is already coded to support these links."
    },
    {
      id: "l3",
      lane: "launch",
      title: "UIP wiring + relativized scores",
      wavShort: "WAV-273 · every gauge linked",
      priority: "high",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "Use-Improve-Protect wired into every gauge — including the to-be-surfaced Stance gauges. Links in every one for supporting modules. Use: Stance Alignment plus Response Field. Improve: Dev plus Response Field. Protect: Range/Drift plus Response Field. Plus WAV-273 Raw, Relative, and Potential scores in the rotating panel for individual and team lenses."
    },

    // --- OTHER / FUTURE PLANNING ------------------------------------------
    {
      id: "o1",
      lane: "other",
      title: "Quick surveys for outreach + speaking",
      wavShort: "10-question briefs · v0.3 stance",
      priority: "med",
      start: "2026-07-01",
      end:   "2026-07-15",
      detail: "Quick surveys for outreach and speaking — 10-question briefs in the same format and iconography as the Drives refiners. Five questions on Stance, five on Phase, predicting all 25 plus Execution Rhythm. Consider current stance v0.3 draft for Stance and Work Shift; potentially augment v0.3 for Social Charge and Execution Rhythm."
    },
    {
      id: "o2",
      lane: "other",
      title: "Notifications system",
      wavShort: "Cadence + survey dropdowns",
      priority: "med",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "Standard cadence-based notifications on the app interface — set at whatever cadence works best. Alongside each notification, a + or prompt for a dropdown surfacing: Work Shift weekly survey questions (compares current work-slider input to baseline from the assessment, ideally averaged over five takes plus Roger calibrations), unfinished refiner questions (if the user just did QQs between tiers), and Amplifier questions at the epicenter level (Tactician, Beacon, etc. — not TAC-1, BEA-4, those live in Launch View)."
    },
    {
      id: "o3",
      lane: "other",
      title: "UWorks · AWorks · P360 basics",
      wavShort: "Initial tier builds",
      priority: "med",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "Initial tier builds for UWorks (Unicorn-themed), AWorks (Amplifier-themed), and P360 (Performance 360). Paired with Use-Improve-Protect wiring across every gauge."
    },
    {
      id: "o4",
      lane: "other",
      title: "Future planning — tiers scoped (Core · Unicorn · Amp · P360)",
      wavShort: "⊞ all tiers scoped by 9/30",
      priority: "med",
      start: "2026-08-01",
      end:   "2026-09-30",
      detail: "Scoping work for the next layer. A360 Core ⊞ all tiers scoped. Unicorn ⊞ all tiers scoped. Amp ⊞ all tiers scoped. P360 ⊞ all tiers scoped. Plus the Mission, Culture, Resonance, and Signal series at the same scoping level. 'Scoped' here means specs and structure are defined and ready for the planning push that follows in Q4."
    },
    {
      id: "o5",
      lane: "other",
      title: "Future planning — all tiers planned + Axis/Vector ↗",
      wavShort: "↓↑ planned · ↗ planned",
      priority: "med",
      start: "2026-10-01",
      end:   "2026-12-31",
      detail: "The Q4 planning push that sets up 2027. A360 Core, Unicorn, Amp, and P360 each get ↓↑ all-tiers planned. Plus A360 Axis ↗, UWorks Vector ↗, AWorks Amp ↗, P360 ↗ all planned. Mission, Culture, Resonance, Signal series at ↓↑ level. Impact, Apex, Cadence, Radar series at ↗ level. 'Planned' is deeper than 'scoped' — it includes sequencing, dependencies, and the rough resourcing required for the 2027 build window."
    }
  ],

  // --- Milestones (diamonds at the bottom) ---------------------------------
  // Each milestone is positioned at the end of its `date`.
  // Click opens a detail modal just like an item.
  milestones: [
    {
      id: "m1",
      label: "EA go-live",
      shortDate: "6/30",
      date: "2026-06-30",
      title: "EA go-live · 6/30",
      priority: "crit",
      dates: "June 30, 2026",
      wav: "Early Access launch",
      detail: "Early Access go-live. What needs to be ready: A360 cleanup including Roger output-wiring (the load-bearing dependency for every view), Z5/D5/E5+E5x refiners, You View app foundation, Team Member Crew View in app, Crew Desktop EA Team Lead foundation, Team Groupings + Crew Read placeholder, Launch View Amplifier module + UIP landing, and the previously scoped refiners (WAV-355/356/357). Most everything between 5/25 and 6/30 in the timeline ladders into this gate."
    },
    {
      id: "m2",
      label: "GA go-live",
      shortDate: "9/30",
      date: "2026-09-30",
      title: "GA go-live · 9/30",
      priority: "crit",
      dates: "September 30, 2026",
      wav: "General Access launch",
      detail: "General Access go-live. What needs to be ready: Q5 / V5 / H5 refiners (Q5 is the gate to App full functionality), assessment retake versioning, editable categories + structural refinement, CrewArcs (5), Crew Desktop GA including the CHRO and Job Applicant view, Plain Language + small team pulses, Five Amplifier Epicenters + training at A360 Pro three levels, Quick Surveys (ships ahead by 7/15), and tier scoping for Core / Unicorn / Amp / P360. The 9/30 gate is denser than 6/30 — more parallel workstreams, more dependencies between them."
    },
    {
      id: "m3",
      label: "Polish + plan",
      shortDate: "12/31",
      date: "2026-12-31",
      title: "Polish + plan · 12/31",
      priority: "crit",
      dates: "December 31, 2026",
      wav: "Polish complete · 2027 setup",
      detail: "Polish complete plus Future Planning foundation. What needs to be ready: Response Field (Notice-Name-Attune-Route-Calibrate complete with E5x and gating), My Wavelength Clear Signal, You View desktop with enhanced insights, UIP wiring across every gauge plus relativized scores, notifications system, UWorks / AWorks / P360 basics, and all tiers planned (↓↑) plus the Axis / Vector / Amp ↗ planning. The 12/31 push is less about new features and more about closing UIP loops, surfacing the right gauges in the right places, and lining up clean inputs for the 2027 build window."
    }
  ]
};
