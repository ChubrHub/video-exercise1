#!/usr/bin/env python3
"""
=============================================================================
 SESSION CLOSE - the derivable half, done for you   (a dev tool, not shipped)

   python tools/close.py               what moved, and how far behind we are
   python tools/close.py --dated       build ONE combined dated document
   python tools/close.py --row         append the skeleton row to SLOT_LOG.md
   python tools/close.py --drop URL    write the drop file the board reads
   python tools/close.py --all URL     dated + row + drop, in one command

   python <house>/close.py --install <repo>    give a repo its own copy

   tools/close.project   ONE LINE: the project this repo files under on the
                         board, when that is not the folder name (see below)
   tools/close.slots     `<Slot> <path>` per line, when the slot documents are
                         not docs/STATUS_<repo>.md and its siblings
   tools/close.own       ONE LINE: the tool this repo already closes with.
                         Present, and close.py reports and writes nothing

 WHY THIS EXISTS
 -------------------------------------------------------------------------
 HIS WORDS, 2026-09-12: *"The slots thing we worked out about ten sessions ago
 and was supposed to be a permanent protocol. Now I find not only is it not
 being done, it's malformed."* And then the requirement, verbatim:

     "No touches by me. None. Automatic. Every repo"

 WHAT HAD HAPPENED. The protocol lives in `~/.claude/CLAUDE.md` and was skipped
 at every close for 108 builds: `SLOT_LOG.md`'s newest row said `clarity-207`
 on 2026-08-24 while the program was at `clarity-315`, and `SESSION_HANDOFF.md`
 - the file a session reads FIRST - described that same dead build. HE found
 that. Not a tool, not a session.

 AND THE ARCHIVE WAS RECORDING NOTHING. Measured on his own board: Clarity's
 Status slot held `...d3cffbc33481` with `...d3cffbc33481` filed behind it
 TWICE. The slot address is PERMANENT by design, so archiving it files the
 identical string on top of itself. What the standard asks for is a permanent
 address in the slot PLUS a dated copy at its own URL - and the dated copies
 had stopped being made.

 WHAT IS AUTOMATED HERE, AND WHAT DELIBERATELY IS NOT
 -------------------------------------------------------------------------
 AUTOMATED: which slots moved (git knows), the combined dated document, the
 log row's skeleton, and the drop file the board reads. Five of the six steps.

 NOT AUTOMATED, and neither can be:
   * THE PUBLISH. Only a session can mint an artifact URL. What this does is
     make it ONE publish rather than five - the S44 ruling, in his words
     "it costs one Share click a round instead of five".
   * THE CONTENT of the "what moved" column. Every sentence there is a claim
     about what happened, and only somebody who was there can make one. This
     writes a SKELETON carrying the facts that ARE derivable - the build range
     and the commit subjects - and marks the prose TODO, which the gate in
     `make_release` then refuses to ship.

 THE PROJECT IS NOT ALWAYS THE REPO - found by the Admin session before it
 installed this, 2026-09-12, read from the source. `wavelength-suite` files
 under the board's `admin` project (his words, 8 Sep: "this should go to the
 Admin project") and `quickwave` under `stance-read`. Keyed on the folder name,
 `--all` filed a close under a project holding none of that repo's slots. So a
 repo whose board name differs DECLARES it in `tools/close.project`, and with
 nothing declared the folder name is used and the output SAYS so.

 AND IT IS NEVER A SECOND WRITER. A repo may already produce
 `<repo>.sessions.clarity.json` with its own script (wavelength-suite's
 `clarity-drop.mjs` writes its three newest reports there). Overwriting that
 would silently drop rows from his AI Sessions feed - the exact conflict the
 drop road forbids, arriving through the tool built to enforce it. So the file
 carries `"writer": "close.py"`, and a file that is not close.py's is REFUSED,
 never replaced.

 AND A REPO IS NOT LAID OUT LIKE CLARITY - the same session, installing it
 for real. Three more facts close.py had assumed:
   * WHERE THE SLOTS ARE. wavelength-suite's five are hand-written HTML at
     docs/published/{status,spec,map,inventory,handoff}.html (his ruling: slot
     pages there are hand-written, never generated). By convention close.py
     found an old MAP_wavelength-suite.md and called it the Map. A repo like
     that declares its slots in tools/close.slots, and a declared list is the
     WHOLE list - a slot it does not name is absent, never guessed at.
   * WHAT A LOG ROW LOOKS LIKE. Its table is `Date | Session | Re-derived |
     Moved | Bound / to bind | Note`, with no build column, so a reader keyed on
     close.py's own row called eighteen rows "NONE LOGGED" and its first close.
     A close is now any table row whose first cell is a date; the build is read
     only from a column the header names Build.
   * WHO WRITES THE ROW. `--row` into that table would have put a nine-column
     row into a six-column table. It writes only into the shape it created and
     refuses any other with the columns named.
 And a repo that already closes correctly with its own tooling says so in
 tools/close.own; the standard's "every repo" is met by the repo, not by this
 file.

 REPO-AGNOSTIC ON PURPOSE. Nothing here names Clarity. The slot markdown is
 found by convention, the build stamp is optional, and a repo with no stamp
 falls back to its short sha - so this file is copied into a repo and works.
=============================================================================
"""

import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.basename(ROOT)
PROJECT_FILE = os.path.join(ROOT, "tools", "close.project")
SLOTS_FILE = os.path.join(ROOT, "tools", "close.slots")
OWN_FILE = os.path.join(ROOT, "tools", "close.own")
WRITER = "close.py"
DOCS = os.path.join(ROOT, "docs")
LOG = os.path.join(DOCS, "SLOT_LOG.md")


def say(*bits):
    """RULE 58: A `print` IS NOT A SAFE OPERATION ON WINDOWS. This tool puts
       paths, commit subjects and its own marks on a cp1252 console, and the
       first run of it died on a pencil glyph - UnicodeEncodeError, mid-report,
       after two thirds of the answer had already been printed. A helper that
       reports may never be the thing that takes the run down."""
    line = " ".join(str(b) for b in bits)
    try:
        sys.stdout.write(line + "\n")
    except Exception:                                          # noqa: BLE001
        try:
            enc = getattr(sys.stdout, "encoding", None) or "ascii"
            sys.stdout.write(line.encode(enc, "replace").decode(enc) + "\n")
        except Exception:                                      # noqa: BLE001
            pass


# THE FIVE, BY CONVENTION AND NOT BY A SECOND LIST. A per-repo table here would
# be a second place the paths live and it would drift from SLOT_LOG's own
# "the markdown behind each one" (rule 55's corollary).
SLOTS = [
    # WHERE_WE_ARE.md is circles' Status, and the house standard itself names
    # it as that repo's Status document - so it is a convention, not a guess.
    ("Status", ("STATUS_%s.md" % REPO, "STATUS.md", "WHERE_WE_ARE.md")),
    ("Spec", ("SPEC_%s.md" % REPO, "SPEC.md")),
    ("Map", ("MAP_%s.md" % REPO, "MAP.md")),
    ("Inventory", ("INVENTORY_%s.md" % REPO, "INVENTORY.md")),
    # THE ONE NAME THAT DOES NOT FOLLOW THE CONVENTION, deliberately: it is
    # named by the starter prompt and by every session's opening instruction,
    # and renaming it to satisfy a convention would break the one file a
    # session reads first.
    ("Handoff", ("SESSION_HANDOFF.md", "HANDOFF_%s.md" % REPO)),
]

MOVED, SAME, ABSENT = "moved", "same", "-"


def declared_lines(path):
    """The non-blank, non-comment lines of a one-fact-per-line file, or None
       when the file is not there. None and [] are different answers: absent
       means "use the convention", present-and-empty means "declared nothing"."""
    try:
        with io.open(path, encoding="utf-8-sig") as fh:
            raw = fh.read().splitlines()
    except OSError:
        return None
    return [l.strip() for l in raw if l.strip() and not l.strip().startswith("#")]


def declared_slots():
    """{label: absolute path} from tools/close.slots, or None when undeclared.

       A DECLARED LIST IS THE WHOLE LIST. Falling back to the convention for a
       label it leaves out is exactly how an old MAP_<repo>.md got called the
       Map in a repo whose Map is somewhere else."""
    lines = declared_lines(SLOTS_FILE)
    if lines is None:
        return None
    names = dict((l.lower(), l) for l, _ in SLOTS)
    out = {}
    for line in lines:
        parts = line.split(None, 1)
        if len(parts) != 2 or parts[0].lower() not in names:
            continue
        out[names[parts[0].lower()]] = os.path.normpath(
            os.path.join(ROOT, parts[1].strip()))
    return out


def own_tool():
    """The tool this repo already closes with, or "" (tools/close.own)."""
    lines = declared_lines(OWN_FILE)
    return lines[0] if lines else ""


def slot_file(label, names):
    """The document behind one slot: declared, else by convention, else ""."""
    decl = declared_slots()
    if decl is not None:
        p = decl.get(label, "")
        return p if p and os.path.isfile(p) else ""
    return slot_path(names)


# THE CANONICAL COPY, and the reason this file can install itself.
#
# TWO HOUSE RULES POINT OPPOSITE WAYS HERE AND BOTH ARE RIGHT.
# `00_House_Standards/README.md` says these are NOT copied into each repo -
# "a copy forks the moment two repos disagree". `~/.claude/CLAUDE.md` says
# "copy them into a repo rather than running them from OneDrive - a tool run
# from a synced folder against the wrong working directory is a bad
# afternoon." The first is about the PRACTICE documents, which must not fork.
# The second is about a TOOL, and this tool is the sharp case: it derives the
# repo from its own `__file__`, so run out of the standards folder it would
# treat that folder as the repo and write a close log into OneDrive.
#
# ⇒ The canonical copy lives in the standards folder and REFUSES to operate
# there. `--install` is how a repo gets its copy: one command, run by a
# session, never by him - which is the whole of "No touches by me. None.
# Automatic. Every repo". A copy that drifts is re-installed by the same
# command, because it overwrites.
HOUSE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents",
                     "Business", "Apps", "00_House_Standards")


def in_house():
    """Is this file the canonical copy, sitting in the synced folder?"""
    try:
        return os.path.normcase(os.path.dirname(os.path.abspath(__file__))) \
            == os.path.normcase(HOUSE)
    except Exception:                                          # noqa: BLE001
        return False


def cmd_install(dest):
    """Copy this file into <repo>/tools/close.py and say what happened.

       It overwrites deliberately: the standards folder is the source and a
       repo never edits its own copy, so a divergent copy is a stale copy."""
    dest = os.path.abspath(os.path.expanduser(dest))
    if not os.path.isdir(dest):
        say("  REFUSING: %s is not a folder" % dest)
        return 2
    if not os.path.isdir(os.path.join(dest, ".git")):
        say("  REFUSING: %s has no .git - name the repo's top folder" % dest)
        return 2
    tools = os.path.join(dest, "tools")
    if not os.path.isdir(tools):
        os.makedirs(tools)
        say("  created %s" % tools)
    me = os.path.abspath(__file__)
    out = os.path.join(tools, "close.py")
    if os.path.normcase(me) == os.path.normcase(out):
        say("  already installed here - nothing to do")
        return 0
    blob = io.open(me, "rb").read()
    was = io.open(out, "rb").read() if os.path.isfile(out) else b""
    # ENCODE FIRST, TEMP, REPLACE (rule 153) - and this one is a byte copy, so
    # there is nothing to encode and nothing that can fail after a truncate.
    tmp = out + ".tmp"
    io.open(tmp, "wb").write(blob)
    os.replace(tmp, out)
    say("  %s %s (%d bytes)"
        % ("installed" if not was else
           ("refreshed" if was != blob else "re-wrote (identical)"),
           os.path.relpath(out, dest).replace("\\", "/"), len(blob)))
    say("  Run it there: python tools/close.py")
    return 0


def git(*args):
    try:
        r = subprocess.run(["git"] + list(args), cwd=ROOT, text=True,
                           capture_output=True, timeout=30)
        return r.stdout.strip()
    except Exception:                                          # noqa: BLE001
        return ""


def slot_path(names):
    for n in names:
        p = os.path.join(DOCS, n)
        if os.path.isfile(p):
            return p
    return ""


def build_stamp():
    """This repo's build string, or its short sha. Optional by design - most
       repos carry no build number and a close still owes a row."""
    for name in ("clarity_admin.py",):
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            with io.open(p, encoding="utf-8", errors="replace") as fh:
                m = re.search(r'CLARITY_BUILD\s*=\s*"([^"]+)"', fh.read())
            if m:
                return m.group(1)
    return git("rev-parse", "--short", "HEAD") or "(no build stamp)"


def last_close():
    """(build, date) of the newest logged close, or ("", "")."""
    build, date, _session = last_close_row()
    return build, date


def last_close_row():
    """(build, date, session) of the newest logged close, or ("", "", "")."""
    if not os.path.isfile(LOG):
        return "", "", ""
    with io.open(LOG, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    # A CLOSE IS A ROW WITH A DATE IN THE COLUMN ITS TABLE CALLS Date, under
    # whatever columns the log has and in whatever order. circles puts Session
    # first (`| Session | Date | Trigger | ...`), and a reader that wanted the
    # date in the first cell found no close there at all. The build comes only
    # from a column headed Build, the session only from one headed Session -
    # a backtick in a notes cell is a file name, not a build.
    # A table whose header has no Date column contributes nothing; a table
    # with no header at all falls back to a date in the first cell.
    lines = src.splitlines()
    date_col, build_col, ses_col = 0, -1, -1
    rows = []
    sep = re.compile(r"^\|\s*:?-{3,}")
    for n, line in enumerate(lines):
        if not line.startswith("|"):
            date_col, build_col, ses_col = 0, -1, -1
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if sep.match(line):
            continue
        if n + 1 < len(lines) and sep.match(lines[n + 1]):
            low = [re.sub(r"[*_`]", "", c).strip().lower() for c in cells]
            date_col = low.index("date") if "date" in low else -1
            build_col = low.index("build") if "build" in low else -1
            ses_col = low.index("session") if "session" in low else -1
            continue
        if date_col < 0 or date_col >= len(cells):
            continue
        if not re.match(r"^\d{4}-\d\d-\d\d$", cells[date_col]):
            continue
        build = ""
        if 0 <= build_col < len(cells):
            m = re.search(r"`([^`]+)`", cells[build_col])
            build = m.group(1) if m else ""
        session = ""
        if 0 <= ses_col < len(cells):
            m = re.match(r"^[\s*_`]*([A-Za-z]+\d+[a-z]?)\b", cells[ses_col])
            session = m.group(1) if m else ""
        rows.append((cells[date_col], build, session))
    if not rows:
        return "", "", ""
    # NEWEST BY DATE, not by position - rows are written newest-first by hand,
    # and a correction row appended later must not read as a regression. On a
    # tie the FIRST row in the file wins, because newest-first is how both
    # shapes of log are written.
    # ⚠️ EXCEPT A LOG WRITTEN OLDEST-FIRST (wavelength-app's appends at the
    # bottom), where the newest of a day's rows is the LAST. Measured 2026-10-02:
    # a second close the same day kept reading the morning's row, so its count
    # never reset and its own gate refused the close. The direction is read off
    # the log itself (first dated row older than the last), so a newest-first
    # log is exactly as before.
    newest = max(r[0] for r in rows)
    ascending = rows[0][0] < rows[-1][0]
    tied = [r for r in rows if r[0] == newest]
    date, build, session = tied[-1] if ascending else tied[0]
    return build, date, session


def boundary():
    """The commit the last logged close was cut at, as git range arguments.

       A BARE DATE IS NOT MIDNIGHT, AND THAT IS WHY THIS IS NOT A DATE.
       Measured here on 2026-09-12 at 11:15, with nine commits already made
       that morning: `--since=2026-09-12` returned ZERO and
       `--since='2026-09-12 00:00:00'` returned NINE. Git's approxidate reads a
       bare date as that date AT THE CURRENT TIME OF DAY, so a close run on the
       day it happens would list none of its own work - silently, and with an
       empty "what moved" column that reads as "nothing happened".

       The log row names a BUILD, and a build has a release commit. That is
       exact, it is same-day safe, and it is already recorded. The date is the
       fallback for a repo with no build stamps, and it is spelled with a
       time."""
    last, date, session = last_close_row()
    if last:
        sha = build_commit(last)
        if sha:
            return [sha + "..HEAD"], last, date
    if date:
        # THE DAY IS TOO COARSE WHEN A SESSION WORKS ALL DAY. wavelength-suite,
        # 2026-09-12: the log names S29 and no build, and counting from the
        # start of the day gave 17 commits where 7 follow "S29 closed" - ten of
        # them S29's own work. Against a trigger of a dozen, that read as
        # overdue when it was not. So the commit whose subject names the
        # logged session is the boundary, and the day is the fallback.
        sha = session_commit(session, date) or close_commit_on(date)
        if sha:
            return [sha + "..HEAD"], last, date
        return ["--since=%s 00:00:00" % date], last, date
    return [], last, date


def session_commit(session, date):
    """The commit a dated close was cut at, found by the session it names, or "".

       On or after the close's day, the newest subject naming the session as a
       whole token ("S29", never the "S2" inside it) - and among those, one
       that says it CLOSED wins, so a later session's commit that merely
       mentions S29 cannot move the boundary past the close."""
    if not session or not date:
        return ""
    raw = git("log", "--since=%s 00:00:00" % date, "-n", "400",
              "--format=%H\x1f%s", "HEAD")
    token = re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(session))
    named, closed = [], []
    for line in raw.split("\n"):
        if "\x1f" not in line:
            continue
        sha, subject = line.split("\x1f", 1)
        if token.search(subject):
            named.append(sha)
            if re.search(r"(?i)\bclos(e|ed|ing)\b", subject):
                closed.append(sha)
    return (closed or named or [""])[0]


def close_commit_on(date):
    """The commit that wrote the close, on or after its day, or "".

       THE ROW IS THE CLOSE, SO THE COMMIT THAT CHANGED THE LOG IS ITS
       BOUNDARY. This used to be the newest commit whose SUBJECT said "close",
       and commits use that word for other things. Measured 3 Oct 2026:
       signal-read resolved to "W-427: close literal control bytes as a class"
       and counted 5 commits where 48 had passed; quickwave resolved to "SEN's
       row is closed" and counted 3 where 17 had. A repo whose work mentions
       closing anything read as current while a month behind, the one
       condition this tool exists to catch. Found by signal-read's session.
       circles' close commit ("docs: the close notes on the commit count"),
       the case this was first written for, changes the log, so it still
       resolves."""
    if not date:
        return ""
    rel = os.path.relpath(LOG, ROOT).replace(os.sep, "/")
    return git("log", "--since=%s 00:00:00" % date, "-n", "1",
               "--format=%H", "HEAD", "--", rel)


def build_commit(build):
    """The newest commit whose SUBJECT names this build, or "".

       ⚠️ THE SUBJECT, NOT THE MESSAGE, AND THAT IS THE WHOLE FUNCTION.
       `git log --grep` searches the entire commit message. The commit that
       introduced this tool quotes `clarity-315` in its body while describing
       the gap it was written for - so `--grep` resolved the boundary to THAT
       commit, and the very next run reported "0 commits, nothing moved" over
       work committed ninety seconds earlier. A release commit announces itself
       in its SUBJECT; a commit that merely discusses a build does not.

       Bounded by `-n`, because this walks subjects rather than asking git to
       filter, and an unbounded walk of a long history on every invocation is a
       cost nobody asked for."""
    if not build:
        return ""
    raw = git("log", "-n", "400", "--format=%H\x1f%s", "HEAD")
    for line in raw.split("\n"):
        if "\x1f" not in line:
            continue
        sha, subject = line.split("\x1f", 1)
        if build in subject:
            return sha
    # ⚠️ A LOG WHOSE BUILD COLUMN IS THE COMMIT ITSELF (wavelength-app writes
    # `cut from 76299b7`) names no release commit, so no subject carries it,
    # and the fallback below found the PREVIOUS close's commit instead: a
    # second close the same day could not reset its own count until it had
    # already committed, which its gate refused (2026-10-02). A build that is a
    # commit hash resolves to that commit. A release name like clarity-315 is
    # not a hash and never reaches this line.
    if re.match(r"^[0-9a-f]{7,40}$", build):
        full = git("rev-parse", "--verify", "--quiet", build + "^{commit}")
        if full:
            return full.strip()
    return ""


def moved_since():
    """Which slot documents have commits in the range. Three states, never two:
       a document that does not exist here is not the same fact as one that did
       not move (rule 16)."""
    rng, last, date = boundary()
    out = []
    for label, names in SLOTS:
        p = slot_file(label, names)
        if not p:
            out.append((label, ABSENT, ""))
            continue
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if not rng:
            out.append((label, MOVED, rel))       # no prior close: all of it
            continue
        n = git("rev-list", "--count", *(rng + ["--", rel]))
        moved = (n or "0") != "0"
        # ⚠️ THE WORKING TREE COUNTS, AND LEAVING IT OUT UNDERSTATED THE FIRST
        # REAL CLOSE THIS TOOL RAN. The handoff and the status had been rewritten
        # minutes earlier and were not yet committed, so the row said `same`
        # across all five - a close describing itself as having changed nothing
        # while the documents sat edited on disk.
        # `guide_sync.touched()` had already settled this for the guide gate and
        # says why in its own comment: "a gate that can only see committed work
        # is a gate you walk around by not committing yet." Same question, so
        # the same answer.
        if not moved and git("status", "--porcelain", "--", rel).strip():
            moved = True
        out.append((label, MOVED if moved else SAME, rel))
    return out


# A FIRST CLOSE STILL HAS WORK TO NAME. Nothing was capped here at first and
# a repo with four thousand commits would have put all of them in one table
# cell; the row says how many were withheld rather than dropping them silently
# (rule 28 - a cap that DISCARDS is not a cap).
FIRST_CLOSE_MAX = 40


def subjects():
    """The commit subjects this close covers.

       ⚠️ AN EMPTY RANGE IS "EVERYTHING", NOT "NOTHING", AND THE FIRST DRAFT
       HAD IT BACKWARDS. With no prior close `boundary()` returns no range, and
       returning [] there made a repo's FIRST close report `0 commit(s) since
       the beginning` beside a moved column saying every slot had moved. The
       two halves of one row contradicting each other, on the one close that
       has the most to say. Found by driving it in a fresh repo (rule 138)."""
    rng, last, _ = boundary()
    # A LOG ROW WITH A DATE AND NO BUILD still gives a range: `boundary()`
    # falls back to the date, spelled with a time. So "logged, but no range"
    # only happens with no row at all, and that is the first close.
    args = list(rng) if rng else ["HEAD"]
    raw = git("log", "--format=%s", "--no-merges",
              "-n", str(FIRST_CLOSE_MAX), *args)
    return [l for l in raw.split("\n") if l.strip()]


def subject_total():
    """How many commits this close really covers - asked separately, because
       the listing is capped and a capped list cannot count what it did not
       fetch. `rev-list --count` is one number and no output to truncate."""
    rng, _, _ = boundary()
    n = git("rev-list", "--count", *(list(rng) if rng else ["HEAD"]))
    try:
        return int(n)
    except (TypeError, ValueError):
        return -1


def subjects_capped():
    """(shown, withheld) - and `withheld` is measured against the REAL total,
       never against the length of a list that was capped before it arrived."""
    subs = subjects()
    total = subject_total()
    if total < 0:
        return subs, 0                 # unknown: claim nothing (rule 16)
    return subs, max(0, total - len(subs))


def cmd_check():
    build = build_stamp()
    last, date = last_close()
    rng, _, _ = boundary()
    say("  repo            %s" % REPO)
    _key, _declared = project_key()
    say("  board project   %s%s" % (_key, "" if _declared else
        "   (the folder name - nothing in tools/close.project)"))
    say("  build           %s" % build)
    if declared_slots() is not None:
        say("  slot documents  declared in tools/close.slots")
    tool = own_tool()
    if tool:
        say("  closes with     %s   (tools/close.own - close.py writes nothing here)"
            % tool)
    if not date:
        say("  last close      NONE LOGGED - docs/SLOT_LOG.md has no row")
    elif not last:
        _b, _d, ses = last_close_row()
        at = session_commit(ses, date)
        near = "" if at else close_commit_on(date)
        if at:
            say("  last close      %s, %s (measured from %s, the commit that "
                "names it)" % (date, ses, at[:7]))
        elif near:
            say("  last close      %s%s (measured from %s, the commit that "
                "wrote the close row)" % (date, (", " + ses) if ses else "",
                                          near[:7]))
        else:
            say("  last close      %s (the log names no build%s; measured from "
                "that whole day)" % (date, (" and no commit names " + ses)
                                     if ses else ""))
    else:
        say("  last close      %s on %s" % (last, date))
    say("  measured from   %s" % (rng[0] if rng else "the beginning"))
    say("")
    say("  what has moved since then:")
    for label, mark, rel in moved_since():
        say("    %-10s %-6s %s" % (label, mark, rel or "(no such document)"))
    subs, more = subjects_capped()
    say("")
    if not date:
        say("  %d commit(s) in this repo's history%s - this is its FIRST close"
            % (len(subs), (" (+%d not listed)" % more) if more else ""))
    else:
        say("  %d commit(s) since the last close%s"
            % (len(subs), (" (+%d not listed)" % more) if more else ""))
    for s in subs[:8]:
        say("      %s" % s[:96])
    if len(subs) > 8:
        say("      ... and %d more" % (len(subs) - 8))
    return 0


def cmd_dated(quiet=False):
    """ONE combined dated document - the S44 ruling, in his words: "it costs
       one Share click a round instead of five". Five separate publishes was
       five Share clicks and five pinned versions to move by hand."""
    build = build_stamp()
    day = datetime.date.today().isoformat()
    # THE NAME IS THE ONE THE REPO ALREADY USES, AND THAT IS NOT COSMETIC.
    # `.gitignore` carries `docs/SLOT_All_*.html` with a measured reason:
    # this file is the five sources concatenated, so every close committed
    # ~1,200 lines that already live in the .md beside it - four closes in
    # one day added 4,755 lines and not one said anything the sources did
    # not. The first draft of this tool invented `SLOT_dated_...`, which
    # slipped past that rule and committed 1,410 lines on its first run.
    # A new name is how an existing rule gets defeated without anyone
    # deciding to defeat it (rule 55's corollary).
    out = os.path.join(DOCS, "SLOT_All_%s_%s.html" % (REPO, day))
    state = fragment_state()
    stale = [l for l, f, m, behind in state if behind]
    frags = [(l, f) for l, f, m, behind in state if f]
    # 🔴 A SLOT WITH A SOURCE AND NO RENDERED PAGE IS A FACT THE ARCHIVE HAS TO
    # CARRY, NOT A CONSOLE LINE THAT SCROLLS AWAY. `circles` binds its Handoff
    # as a FILE, which the house standard allows for that slot alone because it
    # is read by whoever picks the work up rather than sent onward - so it has
    # no page by design. A dated copy that simply leaves it out reads as four
    # slots and no reason, and the reader cannot tell "bound as a file" from
    # "nobody rendered it". Named inside the document instead, with its path.
    unrendered = [(l, os.path.relpath(m, ROOT).replace(os.sep, "/"))
                  for l, f, m, b in state if m and not f]
    blob = b""
    if len(frags) >= 2:
        html = []
        for label, f in frags:
            with io.open(f, encoding="utf-8", errors="replace") as fh:
                html.append((label, fh.read()))
        out_html = (stitch(html, day, build, stale, unrendered)
                    or framed(html, day, build))
        if out_html:
            blob = out_html.encode("utf-8")
            if not quiet:
                say("  stitched %d rendered fragment(s)%s"
                    % (len(frags),
                       (" - BEHIND their source: " + ", ".join(stale))
                       if stale else ""))
                if unrendered:
                    say("  no rendered page for: %s - carried in the document "
                        "as a bound file, not silently dropped"
                        % ", ".join(l for l, _ in unrendered))
    parts = []
    for label, names in SLOTS:
        p = slot_file(label, names)
        if not p:
            continue
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            parts.append((label, fh.read()))
    if not blob and not parts:
        say("  REFUSING: none of the five slot documents exist under docs/")
        return ""
    # THE FALLBACK, for a repo with no renderer. It is deliberately plain and
    # deliberately second: a `<pre>` wrap of the markdown is not what the
    # permanent slots look like, and a dated copy that does not resemble them
    # is a different document wearing their name.
    body = [
        "<!doctype html><meta charset='utf-8'>",
        "<title>%s - session close %s</title>" % (REPO, day),
        "<style>body{max-width:52rem;margin:2rem auto;padding:0 1rem;"
        "font:16px/1.6 system-ui,sans-serif;color:#1b1b1b;background:#fff}"
        "h1{font-size:1.5rem}h2{margin-top:2.5rem;border-top:1px solid #ccc;"
        "padding-top:1rem}pre{white-space:pre-wrap;font:13px/1.55 "
        "ui-monospace,monospace}</style>",
        "<h1>%s - session close %s</h1>" % (REPO, day),
        "<p><b>Build:</b> %s. A dated copy of all five slots, combined. The "
        "five permanent slot addresses are unchanged; this is the copy that "
        "keeps its own date.</p>" % build,
    ]
    for label, text in parts:
        body.append("<h2>%s</h2>" % label)
        body.append("<pre>%s</pre>" % text.replace("&", "&amp;")
                                          .replace("<", "&lt;"))
    if not blob:
        blob = "\n".join(body).encode("utf-8")
    # ENCODE FIRST, TEMP, REPLACE (rule 153). A "w" open truncates before an
    # encode can fail, and that is how a 151 KB source file became 0 bytes.
    tmp = out + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(blob)
    os.replace(tmp, out)
    if not quiet:
        say("  wrote %s (%d bytes)" % (os.path.relpath(out, ROOT), len(blob)))
        say("  PUBLISH THIS ONE FILE, then pass its URL to --row / --drop.")
    return out


def fragment(label):
    """The already-rendered HTML for one slot, or "". Convention only, to stay
       repo-agnostic: `docs/SLOT_<Label>_<repo>.html`, which is what this
       repo's own `slot_doc.py` already writes.

       🔴 AND THE SECOND AND THIRD NAMES ARE NOT TIDINESS. MEASURED IN
       `circles` 2026-10-03: this looked only for `SLOT_Spec_circles.html`,
       found nothing, and built a dated copy of FOUR slots while printing
       "no rendered copy for: Spec". That repo's Spec page is real, is
       published, and is 224 KB - it is `docs/SPEC_circles.html`, written by
       `npm run spec` from a field register rather than by `slot_doc.py`. So
       the slot the house standard calls the rarest and most expensive to move
       was the one silently missing from its own archive, and the console line
       that said so read as a gap in the repo rather than a gap in this
       lookup. A slot whose page is generated by the product's own tool is the
       normal case, not the exception.

       ⚠️ THE DECLARED PATH STILL WINS AND STILL ANSWERS ALONE. A declared
       list is the whole list (see `declared_slots`), so a repo that names its
       pages gets exactly what it named and none of these guesses."""
    decl = declared_slots()
    if decl is not None:
        p = decl.get(label, "")
        return p if p.lower().endswith(".html") and os.path.isfile(p) else ""
    for name in ("SLOT_%s_%s.html" % (label, REPO),
                 "%s_%s.html" % (label.upper(), REPO),
                 "%s.html" % label.upper()):
        p = os.path.join(DOCS, name)
        if os.path.isfile(p):
            return p
    return ""


def fragment_state():
    """(label, fragment path, markdown path, is the fragment BEHIND its source).

       ⚠️ THE STALENESS IS REPORTED, NEVER REPAIRED HERE. A dated copy that
       silently stitches a fragment older than the markdown it claims to show
       is the archive fault again: a record that records the wrong thing. It is
       named instead, on the console and in the document, because re-rendering
       is `slot_doc.py`'s job and it is not always affordable - MAP_clarity.md
       at 158 KB did not finish rendering in 120 seconds."""
    out = []
    for label, names in SLOTS:
        md, frag = slot_file(label, names), fragment(label)
        behind = bool(md and frag
                      and os.path.getmtime(frag) < os.path.getmtime(md))
        out.append((label, frag, md, behind))
    return out


def framed(parts_html, day, build):
    """One document from whole HTML pages that are not this tool's fragments -
       each kept intact in its own frame, so every page keeps its own styling
       and none of them can restyle another. A `<pre>` wrap of their markup
       would be a different document wearing their name."""
    if not parts_html:
        return ""
    frames = []
    for label, html in parts_html:
        esc = (html.replace("&", "&amp;").replace('"', "&quot;")
                   .replace("<", "&lt;").replace(">", "&gt;"))
        frames.append('<h2 id="slot-%s">%s</h2>\n<iframe title="%s" '
                      'srcdoc="%s"></iframe>' % (label.lower(), label, label, esc))
    return ("<!doctype html><meta charset='utf-8'><title>%s - session close %s"
            "</title><style>body{max-width:60rem;margin:2rem auto;padding:0 1rem;"
            "font:16px/1.5 system-ui,sans-serif}iframe{width:100%%;border:1px "
            "solid #ccc;min-height:60vh}</style><h1>%s - session close %s</h1>"
            "<p><b>Build:</b> %s. The five slot pages as they stood today, each "
            "in its own frame.</p>%s<script>for(const f of document.querySelectorAll"
            "('iframe'))f.addEventListener('load',()=>{try{f.style.height="
            "f.contentDocument.documentElement.scrollHeight+'px'}catch(e){}});"
            "</script>" % (REPO, day, REPO, day, build, "\n".join(frames)))


def stitch(parts_html, day, build, stale, unrendered=()):
    """One document from the five rendered fragments, keeping the first one's
       head and stylesheet whole so all five are typeset identically.

       🔴 EXCEPT FOR A PAGE THAT IS NOT THE SLOT RENDERER'S, WHICH GETS ITS OWN
       FRAME. MEASURED IN `circles` 2026-10-03: once the Spec was found (see
       `fragment`), inlining it dropped its stylesheet and **11 of the 14
       classes its markup uses went undefined** - every one of them defined in
       the stylesheet this function had just thrown away. That is 220 KB of a
       field register rendered as structureless text: the archive would have
       carried the Spec's words with none of its shape, and the console would
       have said "stitched 4 fragments" either way.

       ⚠️ THE MECHANISM IS ALREADY HERE, which is why this is six lines rather
       than a CSS scoper: `framed()` puts each page in an `iframe srcdoc` so
       none can restyle another. A fragment carrying the kept STYLESHEET is
       inlined and typesets identically; one carrying a different sheet is
       framed and keeps its own. **Neither case loses anything, and the
       document says which happened to which**, because "it looked fine" is
       not a thing a session can check about a 440 KB archive.

       ⚠️ AND THE TEST IS THE STYLESHEET, NOT THE WHOLE HEAD. The first version
       compared heads, and framed the Map and the Inventory as well - two pages
       written by the slot renderer itself, carrying the identical sheet, whose
       heads differ in nothing but their own `<title>`. Measured rather than
       assumed: 11,104 and 11,110 characters of head against Status's 11,115,
       same stylesheet byte for byte. A test that over-frames does not lose
       anything either, which is exactly why nothing would have reported it."""
    head = None
    sheet = None
    parts = []
    outside = []
    css = lambda h: (re.search(r"<style>(.*?)</style>", h, re.S) or [None, None])[1]
    for label, html in parts_html:
        m = re.search(r"^(.*?)<div class=\"wrap\">", html, re.S)
        if head is None:
            if not m:
                return ""                 # not the shape we know: fall back
            head, sheet = m.group(1), css(m.group(1))
        body = re.search(r"<div class=\"wrap\">(.*)</div>\s*$", html, re.S)
        if m and sheet is not None and css(m.group(1)) == sheet and body:
            inner = body.group(1)
        else:
            inner = ('<iframe class="slotframe" title="%s" srcdoc="%s">'
                     '</iframe>'
                     % (label,
                        html.replace("&", "&amp;").replace('"', "&quot;")
                            .replace("<", "&lt;").replace(">", "&gt;")))
            outside.append(label)
        parts.append(
            '<section class="slotpart" id="slot-%s">\n<hr class="divider">\n'
            '<p class="slotnote"><strong>%s</strong> &mdash; %s, %s</p>\n'
            '%s\n</section>'
            % (label.lower(), label, day, build, inner))
    if not parts:
        return ""
    warn = ""
    if stale:
        warn = ('<p class="slotnote"><strong>Behind its source:</strong> %s. '
                'Those sections show the last rendered copy, not the markdown '
                'as it stands today.</p>\n' % ", ".join(stale))
    if unrendered:
        warn += ('<p class="slotnote"><strong>Carried as a file, not a page:'
                 '</strong> %s. That slot is bound to a document in the repo '
                 'rather than to a published address, which the house standard '
                 'allows for the Handoff, so there is no rendered page to '
                 'stitch here and nothing was dropped.</p>\n'
                 % ", ".join("%s (%s)" % (l, p) for l, p in unrendered))
    frame_css = ""
    if outside:
        warn += ('<p class="slotnote"><strong>In its own frame:</strong> %s. '
                 'That page is generated by the product rather than by the '
                 'slot renderer and carries its own stylesheet, so it keeps '
                 'it here instead of being flattened into this one.</p>\n'
                 % ", ".join(outside))
        # The height script is the same one `framed()` uses. It is inert when
        # no section was framed, so it is only emitted when one was.
        frame_css = ('<style>.slotframe{width:100%;border:0;min-height:60vh}'
                     '</style>\n<script>for(const f of document.'
                     'querySelectorAll(".slotframe"))f.addEventListener('
                     '"load",()=>{try{f.style.height=f.contentDocument.'
                     'documentElement.scrollHeight+"px"}catch(e){}});'
                     '</script>\n')
    out = (head + frame_css + '<div class="wrap">\n<header class="masthead">\n'
           '<p class="eyebrow"><span>%s</span><span>&middot;</span>'
           '<span>All five slots</span><span>&middot;</span><span>%s</span>'
           '</p>\n<h1>%s &mdash; the five slots</h1>\n'
           '<p class="standfirst">One dated handover carrying all five slots as '
           'they stood at the close of <strong>%s</strong>, %s. The five '
           'permanent slot addresses are republished in place; this copy is '
           'dated and is never overwritten.</p>\n%s</header>\n<main>\n'
           % (REPO, day, REPO, build, day, warn)
           + "\n".join(parts) + '\n</main>\n</div>\n')
    # THE TITLE IS WHAT HE SEES IN A GALLERY OF DOZENS, so it is a NAME: the
    # repo capitalised, and the date, because a dated copy has to be tellable
    # from the one before it at a glance.
    name = REPO[:1].upper() + REPO[1:]
    return re.sub(r"<title>[^<]*</title>",
                  "<title>%s &mdash; Five Slots, %s</title>" % (name, day),
                  out, count=1)


HEADER = (
    "# Slot log - %s\n\n**One row per close, appended, never rewritten.**\n\n"
    "`moved` written this session | `same` re-derived, unchanged | `-` no "
    "such slot here\n\n| Date | Session | Build | Status | Spec | Map | Inv | "
    "Handoff | What moved, and why |\n|---|---|---|---|---|---|---|---|---|\n")


def cmd_row(url=""):
    """The skeleton row. The FACTS are derived; the prose is marked TODO, and
       `make_release`'s close gate refuses while a TODO stands in the newest
       row - so an unfinished close cannot ship and cannot be forgotten."""
    if not os.path.isfile(LOG):
        with io.open(LOG, "wb") as fh:
            fh.write((HEADER % REPO).encode("utf-8"))
        say("  created docs/SLOT_LOG.md")
    with io.open(LOG, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    m = re.search(r"^\|\s*Date\s*\|.*\n\|[-| :]+\|\n", src, re.M)
    if not m:
        say("  REFUSING: docs/SLOT_LOG.md has no table header to append under")
        return 2
    mine = HEADER.split("\n\n")[-1].split("\n")[0]
    theirs = src[m.start():m.end()].split("\n")[0]
    cols = lambda h: [c.strip().lower() for c in h.strip().strip("|").split("|")]
    if cols(theirs) != cols(mine):
        say("  REFUSING: this log's table is not the shape close.py writes.")
        say("    its columns:    %s" % " | ".join(c.strip() for c in
                                                   theirs.strip().strip("|").split("|")))
        say("    close.py's:     %s" % " | ".join(c.strip() for c in
                                                   mine.strip().strip("|").split("|")))
        say("  A row in the wrong shape breaks the table, so nothing was written.")
        say("  Write this close's row in the log's own shape.")
        return 2
    build = build_stamp()
    last, _ = last_close()
    marks = " | ".join(mark for _, mark, _ in moved_since())
    subs, more = subjects_capped()
    seed = "; ".join(s[:88] for s in subs[:6]) or (
        "no commits since the last close" if last
        else "no commits in this repo yet")
    if more:
        seed += "; (+%d more not listed)" % more
    row = ("| %s | **TODO name the session** | `%s` | %s | **TODO - what "
           "moved, and why.** %d commit(s) since %s: %s%s |\n"
           % (datetime.date.today().isoformat(), build, marks,
              len(subs) + more, last or "the beginning", seed,
              ("  DATED COPY: " + url) if url
              else "  **TODO - publish --dated and record its URL**"))
    src = src[:m.end()] + row + src[m.end():]
    tmp = LOG + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(src.encode("utf-8"))
    os.replace(tmp, LOG)
    say("  appended a skeleton row for %s (%d commits seeded)"
        % (build, len(subs)))
    say("  REPLACE every TODO - the close gate refuses while one stands.")
    return 0


def project_key():
    """(key, declared). The board's name for this repo's project: the first
       line of tools/close.project, or the folder name when nothing is
       declared - and the caller says which, because a guess that files a
       session under the wrong project is silent otherwise."""
    # THE SAME READER AS close.slots AND close.own. It had its own, which did
    # not skip comments, so a close.project opening with "# ..." printed the
    # comment as the board project (found in wavelength-suite, 2026-09-12).
    lines = declared_lines(PROJECT_FILE) or []
    if lines:
        return lines[0], True
    return REPO, False


def drop_is_mine(path):
    """Did close.py write this sessions file? True when it carries the marker,
       or when it has the one shape close.py wrote before the marker existed
       (every row the combined-slots summary). Unreadable is NOT mine - a file
       nobody can prove the owner of is not a file to overwrite."""
    try:
        with io.open(path, encoding="utf-8-sig") as fh:
            blob = json.load(fh)
    except (OSError, ValueError):
        return False
    if not isinstance(blob, dict):
        return False
    if blob.get("writer") == WRITER:
        return True
    rows = blob.get("sessions")
    return (isinstance(rows, list) and bool(rows) and all(
        isinstance(r, dict) and str(r.get("summary") or "").startswith(
            "All five slots, dated and combined") for r in rows))


def cmd_drop(url):
    """The drop file the board reads. It writes ONE file, named for this repo,
       and touches nothing else in that folder - the producer creates, Clarity
       consumes, and a second writer of it is the exact conflict the road
       exists to avoid."""
    if not url:
        say("  REFUSING: --drop needs the published URL")
        return 2
    if not re.match(r"^https?://", url):
        say("  REFUSING: %r has no scheme. Their validator refuses a "
            "schemeless url rather than repairing it, deliberately." % url)
        return 2
    drop = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents",
                        "Clarity", "Clarity Drop")
    if not os.path.isdir(drop):
        say("  no Clarity Drop folder at %s - nothing written" % drop)
        return 1
    out = os.path.join(drop, "%s.sessions.clarity.json" % REPO)
    if os.path.exists(out) and not drop_is_mine(out):
        say("  REFUSING: %s is written by another producer in this repo"
            % os.path.basename(out))
        say("  (it carries no \"writer\": \"close.py\"). Two writers of one"
            " drop file")
        say("  is the conflict the road forbids, so nothing was written. Add"
            " this")
        say("  close's dated URL through that producer instead: %s" % url)
        return 2
    key, declared = project_key()
    if not declared:
        say("  NO tools/close.project - filing under the folder name %r." % key)
        say("  If the board knows this repo's project by another name, write"
            " that")
        say("  name on one line in tools/close.project and run --drop again.")
    day = datetime.date.today().isoformat()
    payload = {
        "clarity": "session-entry", "from": REPO, "writer": WRITER,
        "sessions": [{
            "projects": [key], "tool": "Claude Code",
            "title": "%s - session close %s" % (REPO, day),
            "date": day, "url": url,
            "summary": "All five slots, dated and combined. The five "
                       "permanent slot addresses are unchanged.",
        }],
    }
    tmp = out + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(json.dumps(payload, indent=1).encode("utf-8"))
    os.replace(tmp, out)
    say("  wrote %s, filed under project %r" % (os.path.basename(out), key))
    say("  It reaches his board as a card. One tap, and nothing outside "
        "Clarity has written his config.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dated", action="store_true")
    ap.add_argument("--row", action="store_true")
    ap.add_argument("--drop", metavar="URL", default="")
    ap.add_argument("--all", metavar="URL", default="")
    ap.add_argument("--install", metavar="REPO", default="",
                    help="copy this tool into REPO/tools/ and stop")
    a = ap.parse_args()
    if a.install:
        return cmd_install(a.install)
    if in_house():
        # RULE 10's SHAPE, one level out: a tool that cannot tell which tree it
        # is acting on is the fault, not the folder it is stored in. Refusing
        # here is what lets the canonical copy be canonical.
        say("  This is the canonical copy in 00_House_Standards, and it will")
        say("  not act on that folder - it would write a close log into")
        say("  OneDrive. Install it into the repo instead:")
        say("")
        say("     python \"%s\" --install <repo>" % os.path.abspath(__file__))
        return 2
    tool = own_tool()
    if tool and (a.all or a.dated or a.row or a.drop):
        say("  This repo closes with %s (tools/close.own)." % tool)
        say("  close.py writes nothing here - run that. `python tools/close.py`")
        say("  with no option still reports what moved.")
        return 0
    if a.all:
        if not cmd_dated(quiet=True):
            return 2
        if cmd_row(a.all):
            say("  stopped before the drop: the log row was refused above.")
            return 2
        return cmd_drop(a.all)
    if a.dated:
        return 0 if cmd_dated() else 2
    if a.row:
        return cmd_row()
    if a.drop:
        return cmd_drop(a.drop)
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main() or 0)
