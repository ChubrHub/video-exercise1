// =========================================================================
// Wavelength platform roadmap — data source
// =========================================================================
// Generated 2026-08-11. Restructured to a GA-minimum scope with a separate
// stretch layer for deferred work (see notes below).
// This restructures the roadmap around a GA-minimum scope: each lane shows
// a reduced near-term slice needed for GA, plus a separate "stretch" bar
// for work that continues past GA rather than gating it.
//
// METHODOLOGY, DOCUMENTED (read before trusting any specific date):
// - No Linear ticket carries a real time Estimate. Hours below are a rough
//   proxy: High priority ~8h, Medium ~5h, Low ~3h, No-priority ~4h, with
//   manual overrides for tickets known (from the seam-wiring review) to be
//   P1 unlocks or already near-complete, regardless of their Linear priority.
// - Capacity assumed: 15 hrs/week per developer (Rick + Trenton), 30
//   combined, minus a continuous background draw for Platform/Admin's
//   GA-minimum slice and for Enterprise Account/Team (kept running per
//   this roadmap). Net ~25 effective hrs/week for phase-specific work.
// - One week of buffer has been added ahead of the GA-minimum milestone.
// - Mobile App has NO Linear tickets today. Its GA-minimum bar (40h) and
//   stretch bar (16h) are a placeholder assumption — a working prototype
//   (S&A Marketing) needs a gap-assessment plus wiring to the same A360
//   output You/Base consumes. Treat as provisional until scoped for real.
// - Launch View has essentially no dev-sized tickets yet (WAV-795 is a
//   still-childless umbrella). Its bar is a placeholder for "get scoped,"
//   not a real estimate.
// - This whole file should be treated as a first-pass draft, not final
//   until Charlie, Rick, and Trenton have reviewed the underlying estimates.
//
// See CLAUDE.md (in this folder) for the schema reference.
// =========================================================================

window.ROADMAP_DATA = {

  // --- Page chrome ---------------------------------------------------------
  meta: {
    title: "Wavelength platform roadmap",
    pageTitle: "Wavelength Platform Roadmap — May 2026 – Jan 2027 (DRAFT)",
    eyebrow: "Internal · waveroad05",
    subtitle: "May 2026 → January 2027, organized into eight lanes (Assessment, Crew View, UIP, You/Base View, Mobile App, Stance Alignment, Launch View, Platform/Admin) plus a separate Enterprise Account/Team track. GA-minimum scope targets 11/7. Bars marked 'stretch' are deferred work that continues past GA rather than gating it. Every date here is a first-pass estimate built from ticket-count proxies, not confirmed developer LOE — see the notes at the top of data.js before treating any date as committed.",
    lastUpdated: "August 11, 2026",
    footerLeft: "May 2026–Jan 2027 · 8 lanes + 1 concurrent track · GA-minimum target 11/7",
    footerRight: "theapexos.com"
  },

  // --- Timeline range ------------------------------------------------------
  timeline: {
    start: "2026-05-01",
    end:   "2027-01-31"
  },

  // --- Phases --------------------------------------------------------------
  phases: [
    { id: "ea", label: "EA",             start: "2026-05-01", end: "2026-06-30" },
    { id: "ga", label: "GA (minimum)",   start: "2026-07-01", end: "2026-11-07" },
    { id: "po", label: "Polish & Launch View", start: "2026-11-08", end: "2027-01-31" }
  ],

  // --- Lanes ----------------------------------------------------------------
  lanes: [
    { id: "a360",       name: "A360 assessment · refiners & scoring",         icon: "ti-clipboard-data", tag: "Lane 01" },
    { id: "crew",       name: "Crew view · team lead experience",             icon: "ti-users",          tag: "Lane 02" },
    { id: "uip",        name: "Use / Improve / Protect · copy & link layer", icon: "ti-link",           tag: "Lane 03" },
    { id: "you",        name: "You / Base view · individual experience",     icon: "ti-user",           tag: "Lane 04" },
    { id: "mobile",     name: "Mobile app · prototype wiring",               icon: "ti-device-mobile",  tag: "Lane 05" },
    { id: "stance",     name: "Stance alignment · live scoring engine",      icon: "ti-compass",        tag: "Lane 06" },
    { id: "launch",     name: "Launch view · amplifiers & growth",           icon: "ti-rocket",         tag: "Lane 07" },
    { id: "platform",   name: "Platform / admin · cross-cutting infra",      icon: "ti-stack-2",        tag: "Lane 08" },
    { id: "enterprise", name: "Enterprise account/team · concurrent track",  icon: "ti-building",       tag: "Concurrent" }
  ],

  // --- Items (the bars) ----------------------------------------------------
  items: [

    // --- A360 ASSESSMENT ----------------------------------------------------
    {
      id: "a1", lane: "a360",
      title: "Z5s Social Energy refiner — do next (Charlie-reprioritized 8/11)",
      wavShort: "WAV-837",
      priority: "crit",
      start: "2026-08-11", end: "2026-08-21",
      detail: "GA-minimum, immediate. Carved out of WAV-355 on 8/11 and reprioritized High relative to all other refiners, per Charlie. First Assessment item on the schedule. ~8 hrs at the priority-heuristic rate."
    },
    {
      id: "a1b", lane: "a360",
      title: "Post-assessment landing/credibility page",
      wavShort: "WAV-696",
      priority: "crit",
      start: "2026-08-11", end: "2026-10-17",
      detail: "GA-minimum. Already In Progress. Landing page between assessment completion and results, using canonical copy from wavelength_positioning.md. ~8 hrs at the priority-heuristic rate."
    },
    {
      id: "a2", lane: "a360",
      title: "D5 / E5 / E5x / Q5 / V5 refiners — deprioritized 8/11, plus remaining backlog",
      wavShort: "WAV-355 · 356 · 357 · 34 other WS: Assessment tickets",
      priority: "med",
      start: "2026-08-11", end: "2027-01-31",
      detail: "Stretch. WAV-355/356/357 were deprioritized to Low on 8/11 to concentrate resources on Z5s (WAV-837) — Charlie's direction. Worth a direct flag: D5 was previously identified as feeding the Clarity CrewArc composite (WAV-767/Seam S-2), and Q5 was called out on the prior roadmap as the gate to full App functionality. Deprioritizing this group may have downstream effects on those dependencies that are worth confirming were considered. Also includes the remaining ~34 open WS: Assessment tickets not required to gate GA-minimum. ~143 hrs total, not sequenced against a specific date."
    },

    // --- CREW VIEW -----------------------------------------------------------
    {
      id: "c1", lane: "crew",
      title: "Wire Crew View to real A360 output — the P1 unlock",
      wavShort: "WAV-663·664·767·809-812·814",
      priority: "crit",
      start: "2026-08-11", end: "2026-10-17",
      detail: "GA-minimum. Seams S-1 (WAV-809), S-2 (WAV-767), S-3 (WAV-810), S-6/S-7 (WAV-811), S-8 (WAV-812), plus already-shipped-or-in-flight S-4/S-9 wiring (WAV-663, 664, 665). 'Everything reads off real scores' — the brief's own framing. ~94 hrs."
    },
    {
      id: "c2", lane: "crew",
      title: "Remaining Crew View seams — S-10, S-11, The Bar, Coach pathway",
      wavShort: "WAV-813 · 814 · 815",
      priority: "high",
      start: "2026-10-17", end: "2027-01-31",
      detail: "Stretch. Leader designation, Roger production-endpoint composition read, and the Bar leader-verdict rule. The Coach pathway (Demo 2 scope) was deliberately not drafted — still pending reconciliation against WAV-769. ~31 hrs."
    },

    // --- UIP -------------------------------------------------------------
    {
      id: "u1", lane: "uip",
      title: "UIP mechanical wiring — link columns, RAG fix, KB grounding",
      wavShort: "WAV-796 · 801 · 802 (WAV-799 shipped 8/11)",
      priority: "crit",
      start: "2026-08-11", end: "2026-10-17",
      detail: "GA-minimum. Migration + populate + render (WAV-796), the gauge-specific RAG query fix now unblocked (WAV-801), and the KB_U5/KB_T5 sync (WAV-802). The per-gauge Use/Improve/Protect rollout (WAV-799) shipped 8/11 and is no longer part of the remaining estimate. ~84 hrs, down from ~92 — the ~8-hour reduction is banked as minor schedule margin rather than reflected in an earlier end date. Nearly all of UIP's open work is GA-critical; almost nothing here is stretch."
    },
    {
      id: "u2", lane: "uip",
      title: "Open rulings, KB_UIP v0.7, destination-brief content",
      wavShort: "Charlie's own queue — untracked as dev tickets",
      priority: "med",
      start: "2026-08-11", end: "2027-01-31",
      detail: "Charlie's own workflow — the four open rulings, two Part 8 defects, and KB_UIP version bump, plus incremental landing of destination-brief content. Not tracked as Linear tickets per standing practice; shown here only so the roadmap doesn't imply UIP is 100% dev-driven."
    },

    // --- YOU / BASE VIEW -----------------------------------------------------
    {
      id: "y1", lane: "you",
      title: "Wire You/Base to real A360 output — the P1 unlock",
      wavShort: "WAV-819 (B-5) + 663·667·665·664·814",
      priority: "crit",
      start: "2026-10-17", end: "2026-11-07",
      detail: "GA-minimum. B-5 (WAV-819) is the brief's own 'single biggest unlock,' sharing a scoring seam with Crew View's S-1/S-7. B-1/B-3/B-6/B-7/B-8 are already covered by existing tickets. ~37 hrs."
    },
    {
      id: "y2", lane: "you",
      title: "Remaining seams — B-2, B-4, B-9, Daily Roger Loop",
      wavShort: "WAV-817 · 818 · 820",
      priority: "high",
      start: "2026-11-07", end: "2027-01-31",
      detail: "Stretch. Today's Edge, the Baseline/Now toggle, band tier-gating, and the two-prompt daily loop (still missing its source 'loop spec' document). ~17 hrs."
    },

    // --- MOBILE APP (assumption-based, no tickets exist) ---------------------
    {
      id: "mb1", lane: "mobile",
      title: "Prototype gap-assessment + core wiring (ASSUMPTION — no tickets exist)",
      wavShort: "S&A Marketing prototype · no WAV tickets yet",
      priority: "crit",
      start: "2026-10-17", end: "2026-11-07",
      detail: "GA-minimum, entirely provisional. No Linear tickets exist for this. Assumes ~7 tickets, ~40 hrs, wiring the existing prototype to the same A360 output You/Base's B-5 consumes. Charlie's framing: a value item, run in parallel with You/Base. Needs real scoping before this bar means anything firm."
    },
    {
      id: "mb2", lane: "mobile",
      title: "Adjustments & polish beyond MVP wiring",
      wavShort: "Assumption — ~16 hrs",
      priority: "med",
      start: "2026-11-07", end: "2027-01-31",
      detail: "Stretch, provisional. Whatever the prototype needs beyond core wiring once real scoping happens."
    },

    // --- STANCE ALIGNMENT ------------------------------------------------
    {
      id: "s1", lane: "stance",
      title: "SA-9 unlock + SA-1, SA-2, SA-2b quick fixes",
      wavShort: "WAV-824 · 823 · 825 · 826",
      priority: "crit",
      start: "2026-11-07", end: "2026-11-16",
      detail: "GA-minimum. SA-9 (WAV-824) exposes the ordered 25-signature ranking — no blockers, unlocks SA-1/SA-5/SA-10. SA-2/SA-2b are minutes-scale string fixes. ~32 hrs."
    },
    {
      id: "s2", lane: "stance",
      title: "Remaining Stance seams — SA-4, 5, 6, 8, 10, 11, 12; SA-7 legal tracking",
      wavShort: "WAV-827 · 830 · 831 · 834 · 835 · 836 · 832",
      priority: "high",
      start: "2026-11-16", end: "2027-01-31",
      detail: "Stretch. Includes SA-4 (unresolved — its relationship to WAV-364 needs Trenton's confirmation before this is even fully scoped), gate/zone gating of recommendations, feedback-control wiring, and the SA-7 fair-use legal review tracking item (not dev work). ~29 hrs."
    },

    // --- LAUNCH VIEW -----------------------------------------------------
    {
      id: "l1", lane: "launch",
      title: "Scope Launch View into dev-sized tickets (UNSCOPED)",
      wavShort: "WAV-795 · still childless",
      priority: "med",
      start: "2026-11-17", end: "2027-01-31",
      detail: "Not a real estimate — placeholder only. Launch View has no dev-committed sub-tickets today; WAV-634 (the Charlie-side master) hasn't been handed off the way Crew View's and You/Base's masters were. Real Amplifier/AmpArc content and the wavelength-launch-unified JSX exist, but nothing has been broken into execution-sized pieces yet. Assume this begins once Stance Alignment's GA-minimum lands and runs open-ended."
    },

    // --- PLATFORM / ADMIN (cross-cutting) ---------------------------------
    {
      id: "p1", lane: "platform",
      title: "Launch-blocking: tier entitlement security + Roger trust grounding",
      wavShort: "WAV-168 · 169 · 652 · 655",
      priority: "crit",
      start: "2026-08-11", end: "2026-11-07",
      detail: "GA-minimum, running continuously in the background across the whole GA window rather than as its own phase. Tier entitlement enforcement (WAV-168/169) and Roger's two most trust-critical behavioral grounding items: never confabulate against real A360 data (WAV-652), and anti-sycophancy / honesty-first (WAV-655). ~32 hrs, spread as background tax on every other lane's schedule."
    },
    {
      id: "p2", lane: "platform",
      title: "Remaining Platform/Admin — Roger identity depth, analytics, infra chores, test-failure cleanup",
      wavShort: "37 tickets — WAV-650·651·656·658·577·578·263·792·782-790 and others",
      priority: "med",
      start: "2026-08-11", end: "2027-01-31",
      detail: "Stretch. Includes the deeper Roger identity/character-stability grounding, behavioral analytics infrastructure, the frontend/backend/roger monorepo CI/CD migration (deliberately deferred — too disruptive to run during the crunch), the Claude Code harness commit, and the 60-pre-existing-test-failure cleanup (WAV-782's children). ~235 hrs, deprioritized relative to the GA-minimum cut."
    },

    // --- ENTERPRISE ACCOUNT/TEAM (concurrent, not part of GA path) --------
    {
      id: "e1", lane: "enterprise",
      title: "Enterprise Account/Team Management — active, expected complete end of August",
      wavShort: "WAV-805 · 806 · 807 · 808 (all Rick)",
      priority: "high",
      start: "2026-08-11", end: "2026-08-31",
      detail: "Real, active work — Make Team a first-class citizen of the platform, org units, roles/permissions, an enterprise management skeleton. Not derived from any operationalization brief and not required for A360 GA itself. Draws from Rick's hours in parallel with early Crew View / UIP work, expected complete by end of August. ~32 hrs is likely a floor, not a full estimate, since these read as epic-level titles not yet broken into execution-sized pieces the way Crew View's and You/Base's were."
    }
  ],

  // --- Milestones ------------------------------------------------------
  milestones: [
    {
      id: "m1", label: "EA go-live", shortDate: "6/30", date: "2026-06-30",
      title: "EA go-live · 6/30", priority: "crit", dates: "June 30, 2026",
      wav: "Early Access launch",
      detail: "Historical — Early Access went live on schedule, per Rick's WAV-633 ship note confirming v1.50.0-mvp on 2026-07-15 (post-EA stabilization)."
    },
    {
      id: "m2", label: "GA go-live (minimum)", shortDate: "11/7", date: "2026-11-07",
      title: "GA go-live · GA-minimum scope · 11/7", priority: "crit", dates: "November 7, 2026",
      wav: "General Availability launch — reduced scope",
      detail: "This is a GA-MINIMUM milestone, not full completion: it reflects only the crit-priority bars on this roadmap (Crew View's P1 wiring, UIP's mechanical wiring, You/Base's B-5, Mobile App's core wiring — assumption-based, and Platform/Admin's launch-blocking security/trust items). Stance Alignment and Launch View are explicitly sequenced after this date. Every stretch-priority bar continues past 11/7 by design — a deliberately reduced slice now, with full scope shown as a separate visible layer rather than implied as done."
    },
    {
      id: "m3", label: "Polish + Launch View", shortDate: "1/31", date: "2027-01-31",
      title: "Polish + Launch View + Future Planning · 1/31 (open-ended)", priority: "crit", dates: "January 31, 2027 (provisional)",
      wav: "Stretch work + Launch View scoping",
      detail: "Open-ended placeholder, not a hard deadline. Covers all stretch-priority work across every lane, plus Launch View's entire buildout, which cannot be dated with any confidence until it gets broken into dev-sized tickets the way Crew View and You/Base already have been. Treat this date as 'not before,' not 'by.'"
    }
  ]
};
