#!/usr/bin/env python3
"""Lead Finder workbook: one .xlsx per campaign, one sheet per platform, generated overview sheets.

The platform sheets (LinkedIn, Companies, Reddit, Instagram) are the single source of truth. Every row has a
stable `key` (e.g. linkedin:pub:jane-doe). Lead Finder fills the source columns; the user (and Claude) own the
working columns: status, score, the interaction log, notes, drafts. Merging never overwrites a working column.

Lead Finder never reaches out cold. A lead goes new → to_engage → engaging (the user comments, reacts, connects)
→ warm (they engaged back) → talking (a conversation) → meeting (a call booked) → offered (the offer, made on the
call) → won or lost.

Summary, Next touches and Pipeline are rebuilt on every write. Don't edit them by hand.

The To review sheet holds every find waiting for the user's decision: a preview with a score and no link, handle,
username, email or key. The user sets `decision` to keep or skip; only kept leads, once picked on the server, are
merged into a platform sheet. A row expires with the server's search results and is dropped on every write. To review
is never exported, imported, counted in the platform totals or touched by `remove`. A reason for a score of 5 or less
starts with `wrong fit:`, `not enough to judge:` or `rules out:`; `review add` reports rows without one as `unlabelled`.

The Sources sheet records every run per source (a subreddit, a bio word, a LinkedIn search): results, good leads
(scored 6 or more) and the search id. `review add` writes it from the search result it is given; `sources report` sums
the last 7 days and marks a source `stop` when it showed 10 or more results and gave fewer than 3 good leads. Sources
is never exported, imported or counted in the platform totals.

The Problems sheet records what came up in every Reddit post scored 6 or more, kept or not, when `review add` writes
it: the date, the subreddit, the score, the problem and the ask read from the reason (`<the problem>; asks for <the
ask>`; a reason without a `;` and rows from the signals source, whose reason quotes the post, log nothing), the
item's `phrase` (the poster's own words for the problem), the search id and the result id. It holds no username,
title, link, handle or email: every text has links, emails and handles masked, and the phrase is clipped.
`problems report` counts the posts of the last 30 days per wording. Rows older than 180 days are dropped on every
write. Problems is never exported, imported, counted in the platform totals or touched by `remove`.

Every command that writes takes a lock file next to the workbook (.<name>.xlsx.lock), so two tasks never write the
same workbook at once: a second one waits up to LF_LOCK_WAIT seconds (default 60), then gives up with exit code 4.
A lock older than 10 minutes was left by a crashed task and is removed.

Usage (python3; needs openpyxl: `pip install openpyxl`):
  workbook.py create   WORKBOOK
  workbook.py merge    WORKBOOK ROWS.json [--campaign NAME] [--status STATUS]   rows from get_results (JSON with "sheets") or a list; new rows get STATUS (default new)
  workbook.py update   WORKBOOK KEY field=value [field=value ...]
  workbook.py interact WORKBOOK KEY --by you|them --channel linkedin|reddit|instagram|email --kind comment|like|connect|reply|message|… [--note TEXT] [--url POST_URL]
  workbook.py remove   WORKBOOK KEY_OR_URL                    delete a person everywhere in this workbook
  workbook.py import   WORKBOOK FILE.csv|FILE.xlsx [--sheet LinkedIn|Companies|Reddit|Instagram]
  workbook.py export   WORKBOOK OUT.csv [--sheet NAME] [--status STATUS[,STATUS]]
  workbook.py due      WORKBOOK [--days N]                   next touches due within N days (default 0: today and overdue)
  workbook.py summary  WORKBOOK
  workbook.py rebuild  WORKBOOK
  workbook.py review add WORKBOOK ROWS.json [--source NAME]   finds to approve: a search result (search_id, stored_until, results) or shaped rows
  workbook.py review list WORKBOOK [--platform P] [--decision keep|skip|undecided] [--all]
  workbook.py review remove WORKBOOK ID [ID ...] | --expired | --decided | --all
  workbook.py sources log WORKBOOK STATS.json [--by NAME] [--campaign NAME]   per-source counts of a run: a search result, or rows {platform, key, results, good}
  workbook.py sources report WORKBOOK [--days 7] [--platform P]   results, good leads and kept per source, with the stop rule
  workbook.py problems report WORKBOOK [--days 30]   the problems that came up in the Reddit posts scored 6 or more, counted per wording
`review add` also takes --campaign NAME (default: the workbook's file name).
Every command prints a JSON result.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import tempfile
import time

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:  # pragma: no cover
    print(json.dumps({"error": "openpyxl is missing. Run: pip install openpyxl"}))
    sys.exit(2)

TODAY = dt.date.today()
ENGAGE_DAYS = 3  # after you engage, look again in 3 days
REPLY_DAYS = 1  # when they engage back, answer by tomorrow
OFFER_DAYS = 4  # after the offer on a call, follow up in 4 days

STATUSES = ["new", "to_engage", "engaging", "warm", "talking", "meeting", "offered", "won", "lost", "not_interested", "do_not_contact"]
OPEN_STATUSES = {"engaging", "warm", "talking", "meeting", "offered"}
CLOSED_STATUSES = {"won", "lost", "not_interested", "do_not_contact"}
NOT_ENGAGED = {"new", "to_engage", "engaging"}
# Statuses from older workbooks and CRM files.
LEGACY = {"to_contact": "to_engage", "contacted": "engaging", "replied": "talking", "offer_sent": "offered"}
CONVERSATION_KINDS = {"message", "dm", "email", "call", "asked"}

# Columns the user and Claude own. Merges never overwrite them.
WORK = [
    "status", "score", "score_reason", "next_touch", "engage_channel", "touches", "engaged_on", "last_their_action", "last_their_action_on",
    "interactions", "notes", "draft_comment", "draft_message", "offered_on", "offer_price", "offer_file", "campaign",
]
DATE_COLUMNS = {"next_touch", "engaged_on", "last_their_action_on", "offered_on", "found_on"}

# Source and research columns Lead Finder fills (same order as the server's SHEET_COLUMNS).
SOURCE = {
    "LinkedIn": [
        "name", "headline", "role", "company", "company_url", "location", "profile_url", "open_to_work", "email", "email_quality",
        "signal", "signal_text", "signal_url", "signal_date", "source", "search", "found_on",
        "about", "experience", "education", "skills", "followers", "other_emails", "recent_posts", "recent_comments", "recent_reactions",
    ],
    "Companies": [
        "company", "linkedin_url", "industry", "size", "location", "website", "description",
        "signal", "signal_text", "signal_url", "signal_date", "source", "search", "found_on",
        "company_description", "company_website", "company_size", "company_industry", "company_hq", "company_founded", "company_specialities",
        "company_funding", "company_recent_posts",
    ],
    "Reddit": [
        "username", "profile_url", "subreddit", "type", "title", "text", "post_url", "posted_at", "upvotes", "comments",
        "signal", "source", "search", "found_on", "recent_activity", "karma", "about",
    ],
    "Instagram": [
        "username", "full_name", "profile_url", "caption", "hashtags", "post_url", "posted_at", "likes", "comments",
        "signal", "source", "search", "found_on", "bio", "followers", "website", "business_category", "business_account", "posts_count", "recent_posts",
    ],
}
SHEETS = list(SOURCE)

# What the user sees first on each sheet: who, then the working columns, then everything else.
FRONT = {
    "LinkedIn": ["key", "name", "role", "company"],
    "Companies": ["key", "company", "industry", "size"],
    "Reddit": ["key", "username", "subreddit", "title"],
    "Instagram": ["key", "username", "full_name", "followers"],
}
FRONT_WORK = ["status", "score", "score_reason", "next_touch", "engage_channel", "touches", "last_their_action", "notes"]
BACK_WORK = [c for c in WORK if c not in FRONT_WORK]
URL_COLUMNS = {"profile_url", "company_url", "signal_url", "linkedin_url", "website", "post_url", "company_website"}
GENERATED = ["Summary", "Next touches", "Pipeline"]
OLD_GENERATED = ["Follow-ups"]

# Finds waiting for the user's keep or skip. Never in SHEETS: export, import, remove, due and the generated sheets
# ignore it. A row is a preview: it never holds a URL, handle, username, email or key.
REVIEW = "To review"
REVIEW_COLUMNS = ["id", "search_id", "platform", "decision", "score", "score_reason", "who", "about", "where", "posted_at", "signal", "expires_at", "found_on", "campaign", "source"]
DECISIONS = ("keep", "skip")
ABOUT_CHARS = 300
UTC = dt.timezone.utc

# How each source did: one row per run and per source (a subreddit, a bio word, a search's label). Never in SHEETS:
# export, import, remove, due and the platform totals ignore it. It holds counts only: no person, handle or URL.
SOURCES = "Sources"
SOURCES_COLUMNS = ["date", "platform", "key", "results", "good", "search_id", "by", "campaign"]
SOURCES_KEEP_DAYS = 180  # older runs are dropped on every write; reports look back far less
GOOD_SCORE = 6  # a find Claude scored this or more is a good lead (the same bar that sends a scanned post to To review)
# A reason for a score below GOOD_SCORE starts with one of these, so the user sees why at a glance and can filter by it.
LOW_SCORE_LABELS = ("wrong fit:", "not enough to judge:", "rules out:")
STOP_RULE = {"days": 7, "min_results": 10, "min_good": 3}  # 10 or more results and fewer than 3 good leads in 7 days

# What came up in the Reddit posts scored GOOD_SCORE or more, kept or not: one row per post when `review add` writes it.
# Never in SHEETS: export, import, remove, due and the platform totals ignore it. It holds Claude's words about a post
# and a short phrase, with links, emails and handles masked: no username, title or URL.
PROBLEMS = "Problems"
PROBLEMS_COLUMNS = ["date", "subreddit", "score", "problem", "ask", "phrase", "search_id", "id", "campaign", "source"]
PROBLEMS_KEEP_DAYS = 180  # the same as Sources; the report looks back 30 days
PROBLEMS_DAYS = 30
PHRASE_CHARS = 100  # a phrase is at most 12 words; this is the hard cut
PROBLEM_CHARS = 160
PROBLEMS_NOTE = "Counts are per wording. Group wordings that mean the same before ranking."
PHRASES_PER_PROBLEM = 5

PLATFORMS = ["linkedin", "reddit", "instagram"]
SHEET_PLATFORM = {"LinkedIn": "linkedin", "Companies": "linkedin", "Reddit": "reddit", "Instagram": "instagram"}

LOCK_STALE_SECONDS = 600  # a lock this old was left by a crashed task
LOCK_POLL_SECONDS = 0.2
MUTATING = {"create", "merge", "update", "interact", "remove", "import", "rebuild"}
SUBCOMMANDS = {"review": ("add", "list", "remove"), "sources": ("log", "report"), "problems": ("report",)}
MUTATING_SUB = {("review", "add"), ("review", "remove"), ("sources", "log")}  # review list, sources report and problems report only read
FLAGS = {"--all", "--expired", "--decided"}  # options without a value

# Headers people use in their own files → our columns (lower-case, spaces and punctuation removed).
ALIASES = {
    "fullname": "name", "firstname": "_first", "lastname": "_last", "title": "role", "jobtitle": "role", "position": "role",
    "companyname": "company", "organization": "company", "linkedin": "profile_url", "linkedinurl": "profile_url",
    "linkedinprofile": "profile_url", "profile": "profile_url", "url": "profile_url", "emailaddress": "email", "workemail": "email",
    "city": "location", "country": "location", "stage": "status", "leadstatus": "status", "comment": "notes", "comments_": "notes",
    "user": "username", "handle": "username", "instagram": "profile_url", "reddit": "profile_url", "companylinkedin": "company_url",
    "companyurl": "company_url", "domain": "website", "companywebsite": "website", "followup": "next_touch", "nextfollowup": "next_touch", "nexttouch": "next_touch",
}

HEADER_FILL = PatternFill("solid", fgColor="1D6B4F")
WORK_FILL = PatternFill("solid", fgColor="EAF3EE")


def out(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))


def norm(h: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", str(h or "").strip().lower().replace(" ", "_"))


def columns_for(sheet: str, extra=()) -> list[str]:
    front = FRONT[sheet]
    rest = [c for c in SOURCE[sheet] if c not in front]
    cols = front + FRONT_WORK + rest + BACK_WORK
    for e in extra:
        if e and e not in cols:
            cols.append(e)
    return cols


def to_date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


# ---------- workbook I/O ----------


def load(path: str):
    if not os.path.exists(path):
        return create(path, save=False)
    wb = load_workbook(path)
    for s in SHEETS:
        if s not in wb.sheetnames:
            ws = wb.create_sheet(s)
            ws.append(columns_for(s))
    if REVIEW not in wb.sheetnames:
        write_review(wb, [])  # older workbooks get the sheet on their next write
    if SOURCES not in wb.sheetnames:
        write_sources(wb, [])  # the same for Sources
    if PROBLEMS not in wb.sheetnames:
        write_problems(wb, [])  # and for Problems, after Sources
    return wb


def create(path: str, save: bool = True):
    wb = Workbook()
    wb.remove(wb.active)
    for g in GENERATED:
        wb.create_sheet(g)
    for s in SHEETS:
        ws = wb.create_sheet(s)
        ws.append(columns_for(s))
    write_review(wb, [])
    write_sources(wb, [])
    write_problems(wb, [])
    if save:
        write(wb, path)
    return wb


def read_rows(ws) -> tuple[list[str], list[dict]]:
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    header = [str(h) if h is not None else "" for h in rows[0]]
    data = []
    for r in rows[1:]:
        if r is None or all(v is None or v == "" for v in r):
            continue
        data.append({header[i]: r[i] for i in range(min(len(header), len(r))) if header[i]})
    return header, data


def write_sheet(wb, sheet: str, rows: list[dict]) -> None:
    extra = []
    for r in rows:
        for k in r:
            if k not in extra:
                extra.append(k)
    cols = columns_for(sheet, extra)
    # Drop empty source columns so sheets stay readable; keep every working column.
    used = {k for r in rows for k, v in r.items() if v not in (None, "")}
    cols = [c for c in cols if c in used or c in WORK or c in FRONT[sheet]]
    idx = wb.sheetnames.index(sheet)
    wb.remove(wb[sheet])
    ws = wb.create_sheet(sheet, idx)
    ws.append(cols)
    for r in rows:
        ws.append([r.get(c) for c in cols])
    style(ws, cols, with_status=True)


def style(ws, cols: list[str], with_status: bool = False) -> None:
    for i, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=i)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center")
        letter = get_column_letter(i)
        long = c in {"about", "experience", "signal_text", "text", "caption", "recent_posts", "recent_comments", "recent_reactions", "notes",
                     "interactions", "draft_comment", "draft_message", "description", "company_description", "bio", "recent_activity", "score_reason"}
        ws.column_dimensions[letter].width = 48 if long else 22 if c in URL_COLUMNS else 14 if c in {"status", "score", "engage_channel", "touches"} else 18
        if c == "key":
            ws.column_dimensions[letter].hidden = True
        if c in WORK:
            for row in range(2, ws.max_row + 1):
                ws.cell(row=row, column=i).fill = WORK_FILL
        if c in URL_COLUMNS:
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=i)
                if isinstance(cell.value, str) and cell.value.startswith("http"):
                    cell.hyperlink = cell.value
                    cell.font = Font(color="1D6B4F", underline="single")
        if c in DATE_COLUMNS:
            for row in range(2, ws.max_row + 1):
                ws.cell(row=row, column=i).number_format = "yyyy-mm-dd"
    ws.freeze_panes = "C2" if ws.max_column > 2 else "A2"
    if ws.max_row > 1:
        ws.auto_filter.ref = ws.dimensions
    if with_status and "status" in cols:
        dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True)
        col = get_column_letter(cols.index("status") + 1)
        dv.add(f"{col}2:{col}{max(ws.max_row, 2) + 500}")
        ws.add_data_validation(dv)


def write(wb, path: str) -> None:
    prune_review(wb)
    prune_sources(wb)
    prune_problems(wb)
    rebuild(wb)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=os.path.dirname(os.path.abspath(path)) or ".")
    os.close(fd)
    try:
        wb.save(tmp)
        os.replace(tmp, path)
    except BaseException as e:
        try:
            os.unlink(tmp)  # never leave a half-written copy next to the workbook
        except OSError:
            pass  # keep the original error
        if isinstance(e, PermissionError):
            out({"error": f"Can't write {path}: close it in Excel/Numbers first, then try again."})
            sys.exit(3)
        raise


def all_rows(wb) -> dict[str, list[dict]]:
    return {s: read_rows(wb[s])[1] for s in SHEETS if s in wb.sheetnames}


# ---------- generated sheets ----------


def label(sheet: str, r: dict) -> str:
    return str(r.get("name") or r.get("username") or r.get("company") or r.get("full_name") or r.get("key") or "")


def rebuild(wb) -> None:
    data = all_rows(wb)
    for g in GENERATED + OLD_GENERATED:
        if g in wb.sheetnames:
            wb.remove(wb[g])

    # Summary
    ws = wb.create_sheet("Summary", 0)
    ws.append(["Lead Finder workbook"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([f"Updated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}. Platform sheets are the source of truth; Summary, Next touches and Pipeline are rebuilt automatically."])
    ws.append(["Never message someone who hasn't interacted with you: engage in public first (comments, reactions). Delete anyone who asks."])
    ws.append([])
    ws.append(["Sheet"] + STATUSES + ["total"])
    for s in SHEETS:
        counts = [sum(1 for r in data.get(s, []) if (r.get("status") or "new") == st) for st in STATUSES]
        ws.append([s] + counts + [len(data.get(s, []))])
    due = touches_due(data, 0)
    ws.append([])
    ws.append(["Next touches due today or overdue", len(due)])
    ws.append([review_line(wb)])
    for row in (5,):
        for c in ws[row]:
            c.font = Font(bold=True)
    # How each source did in the stop rule's window, from the same report `sources report` prints.
    ws.append([])
    ws.append([f"Sources, last {STOP_RULE['days']} days"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append(["platform", "key", "results", "good", "kept", "verdict"])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for s in sources_report(wb, STOP_RULE["days"], None)["sources"]:
        ws.append([s["platform"], s["key"], s["results"], s["good"], s["kept"], s["verdict"]])
    ws.append([rule_line()])
    ws.column_dimensions["A"].width = 34

    # Next touches: due and planned, across platforms
    fu = wb.create_sheet("Next touches", 1)
    cols = ["due", "overdue_days", "sheet", "who", "status", "engage_channel", "last_their_action", "touches", "profile_url", "notes", "key"]
    fu.append(cols)
    for f in touches_due(data, 3650):
        fu.append([f.get(c) for c in cols])
    style(fu, cols)

    # Pipeline: everyone past "new", by status
    pl = wb.create_sheet("Pipeline", 2)
    cols = ["status", "sheet", "who", "score", "next_touch", "engaged_on", "engage_channel", "last_their_action", "profile_url", "key"]
    pl.append(cols)
    order = {s: i for i, s in enumerate(STATUSES)}
    rows = []
    for s, rs in data.items():
        for r in rs:
            st = r.get("status") or "new"
            if st in ("new",):
                continue
            rows.append([st, s, label(s, r), r.get("score"), to_date(r.get("next_touch")), to_date(r.get("engaged_on")), r.get("engage_channel"),
                         r.get("last_their_action"), r.get("profile_url") or r.get("linkedin_url"), r.get("key")])
    for row in sorted(rows, key=lambda x: (order.get(x[0], 99), x[4] or dt.date.max)):
        pl.append(row)
    style(pl, cols)


def touches_due(data: dict[str, list[dict]], days: int) -> list[dict]:
    limit = TODAY + dt.timedelta(days=days)
    out_rows = []
    for s, rs in data.items():
        for r in rs:
            st = r.get("status") or "new"
            d = to_date(r.get("next_touch"))
            if st in CLOSED_STATUSES or not d or d > limit:
                continue
            out_rows.append({
                "due": d, "overdue_days": max(0, (TODAY - d).days), "sheet": s, "who": label(s, r), "status": st, "engage_channel": r.get("engage_channel"),
                "last_their_action": r.get("last_their_action"), "touches": r.get("touches"), "profile_url": r.get("profile_url") or r.get("linkedin_url"),
                "notes": r.get("notes"), "key": r.get("key"),
            })
    return sorted(out_rows, key=lambda x: x["due"])


# ---------- commands ----------


def sheet_of_key(key: str, fallback: str | None = None) -> str:
    if key.startswith("linkedin:company"):
        return "Companies"
    if key.startswith("linkedin:"):
        return "LinkedIn"
    if key.startswith("reddit:"):
        return "Reddit"
    if key.startswith("instagram:"):
        return "Instagram"
    return fallback or "LinkedIn"


def incoming_rows(payload) -> list[tuple[str, dict]]:
    """get_results output ({"sheets": {...}}), a {"LinkedIn": [...]} map, or a plain list of rows with keys."""
    if isinstance(payload, dict) and "sheets" in payload:
        payload = payload["sheets"]
    rows = []
    if isinstance(payload, dict):
        for s, rs in payload.items():
            if s in SHEETS:
                rows += [(s, r) for r in rs]
    elif isinstance(payload, list):
        rows = [(sheet_of_key(str(r.get("key", ""))), r) for r in payload]
    return rows


def clean_incoming(r: dict) -> dict:
    r = {k: v for k, v in r.items() if k not in ("id", "state") and v not in (None, "")}
    if "score" in r and "upvotes" not in r and str(r.get("key", "")).startswith("reddit:"):
        r["upvotes"] = r.pop("score")  # Reddit's upvote score isn't the user's fit score
    return r


def merge_rows(wb, incoming: list[tuple[str, dict]], campaign: str | None, source_label: str | None = None, status: str | None = None) -> dict:
    data = all_rows(wb)
    # A kept lead that waited in To review brings its score and reason along (matched on the result id).
    reviewed = {id_key(r.get("id")): r for r in read_review(wb)}
    added = updated = 0
    for s, raw in incoming:
        r = clean_incoming(raw)
        seen = reviewed.get(id_key(raw.get("id"))) if raw.get("id") not in (None, "") else None
        if seen:
            for k in ("score", "score_reason"):
                if r.get(k) in (None, "") and seen.get(k) not in (None, ""):
                    r[k] = seen[k]
        key = str(r.get("key") or "").strip()
        if not key:
            key = derive_key(s, r)
            if not key:
                continue
            r["key"] = key
        rows = data.setdefault(s, [])
        existing = next((x for x in rows if str(x.get("key")) == key), None)
        if existing is None:
            if r.get("profile_url"):
                existing = next((x for x in rows if x.get("profile_url") and str(x.get("profile_url")).rstrip("/").lower() == str(r["profile_url"]).rstrip("/").lower()), None)
        if existing is None:
            new = dict(r)
            new.setdefault("status", status or "new")
            new.setdefault("found_on", TODAY.isoformat())
            if campaign:
                new.setdefault("campaign", campaign)
            if source_label:
                new.setdefault("source", source_label)
            rows.append(new)
            added += 1
        else:
            changed = False
            for k, v in r.items():
                if k in WORK and existing.get(k) not in (None, ""):
                    continue  # never overwrite the user's working columns
                if k == "key":
                    continue
                if existing.get(k) != v:
                    existing[k] = v
                    changed = True
            updated += int(changed)
    for s, rows in data.items():
        write_sheet(wb, s, rows)
    return {"added": added, "updated": updated}


def derive_key(sheet: str, r: dict) -> str | None:
    url = str(r.get("profile_url") or r.get("linkedin_url") or "")
    m = re.search(r"linkedin\.com/in/([^/?#]+)", url, re.I)
    if m:
        slug = m.group(1)
        return f"linkedin:id:{slug}" if re.match(r"^AC[a-zA-Z0-9]AA", slug) else f"linkedin:pub:{slug.lower()}"
    m = re.search(r"linkedin\.com/company/([^/?#]+)", url, re.I)
    if m:
        return f"linkedin:company:{m.group(1).lower()}"
    m = re.search(r"reddit\.com/(?:u|user)/([^/?#]+)", url, re.I)
    if m or (sheet == "Reddit" and r.get("username")):
        return f"reddit:u:{(m.group(1) if m else str(r['username'])).lower()}"
    m = re.search(r"instagram\.com/([^/?#]+)", url, re.I)
    if m or (sheet == "Instagram" and r.get("username")):
        return f"instagram:u:{(m.group(1) if m else str(r['username']).lstrip('@')).lower()}"
    if sheet == "Companies" and r.get("company"):
        return f"linkedin:company-name:{str(r['company']).strip().lower()}"
    if r.get("email"):
        return f"email:{str(r['email']).strip().lower()}"
    return None


def find_row(data: dict[str, list[dict]], key: str):
    for s_, rows in data.items():
        for r in rows:
            if str(r.get("key")) == key or (r.get("profile_url") and str(r.get("profile_url")).rstrip("/") == key.rstrip("/")):
                return s_, rows, r
    return None, None, None


def apply_sets(r: dict, sets: dict) -> None:
    for k, v in sets.items():
        r[k] = to_date(v) if k in DATE_COLUMNS and v else (None if v == "" else v)


def in_days(n: int) -> str:
    return (TODAY + dt.timedelta(days=n)).isoformat()


def cmd_update(wb, key: str, pairs: list[str]) -> dict:
    data = all_rows(wb)
    sets = {}
    for p in pairs:
        if "=" not in p:
            raise SystemExit(f"Expected field=value, got {p}")
        k, v = p.split("=", 1)
        sets[k.strip()] = v
    s_, rows, r = find_row(data, key)
    if r is None:
        return {"error": f"No row with key or profile_url {key}"}
    st = sets.get("status")
    if st:
        st = sets["status"] = LEGACY.get(st, st)
        if st not in STATUSES:
            raise SystemExit(f"Unknown status {st}. Use one of: {', '.join(STATUSES)}")
        if st == "engaging" and not r.get("engaged_on"):
            sets.setdefault("engaged_on", TODAY.isoformat())
            sets.setdefault("next_touch", in_days(ENGAGE_DAYS))
        if st in ("warm", "talking"):
            sets.setdefault("next_touch", in_days(REPLY_DAYS))
        if st == "offered":
            sets.setdefault("offered_on", TODAY.isoformat())
            sets.setdefault("next_touch", in_days(OFFER_DAYS))
        if st in CLOSED_STATUSES:
            sets.setdefault("next_touch", "")
    apply_sets(r, sets)
    write_sheet(wb, s_, rows)
    return {"updated": key, "sheet": s_, "row": {k: r.get(k) for k in ["status", "next_touch", "engaged_on", "offered_on", "notes"] if r.get(k) not in (None, "")}}


def cmd_interact(wb, key: str, by: str, channel: str, kind: str, note: str | None, url: str | None) -> dict:
    """Logs one interaction and moves the lead along: your touches make them engaging; theirs make them warm or talking."""
    if by not in ("you", "them"):
        raise SystemExit("--by must be you or them")
    data = all_rows(wb)
    s_, rows, r = find_row(data, key)
    if r is None:
        return {"error": f"No row with key or profile_url {key}"}
    st = LEGACY.get(r.get("status") or "new", r.get("status") or "new")
    line = f"{TODAY.isoformat()} {by}: {channel} {kind}" + (f" {url}" if url else "") + (f" · {note}" if note else "")
    log = [x for x in str(r.get("interactions") or "").split("\n") if x.strip()]
    sets: dict = {"interactions": "\n".join((log + [line])[-30:])}
    if by == "you":
        sets["touches"] = str(int(r.get("touches") or 0) + 1)
        sets["engage_channel"] = channel
        if not r.get("engaged_on"):
            sets["engaged_on"] = TODAY.isoformat()
        if st in ("new", "to_engage"):
            sets["status"] = "engaging"
        if st in NOT_ENGAGED:
            sets["next_touch"] = in_days(ENGAGE_DAYS)
    else:
        sets["last_their_action"] = f"{kind} ({channel})"
        sets["last_their_action_on"] = TODAY.isoformat()
        if kind in CONVERSATION_KINDS and st in NOT_ENGAGED | {"warm"}:
            sets["status"] = "talking"
        elif st in NOT_ENGAGED:
            sets["status"] = "warm"
        if st not in CLOSED_STATUSES:
            sets["next_touch"] = in_days(REPLY_DAYS)
    apply_sets(r, sets)
    write_sheet(wb, s_, rows)
    return {"logged": line, "sheet": s_, "row": {k: r.get(k) for k in ["status", "touches", "last_their_action", "next_touch"] if r.get(k) not in (None, "")}}


def cmd_remove(wb, needle: str) -> dict:
    data = all_rows(wb)
    removed = []
    n = needle.rstrip("/").lower()
    for s, rows in data.items():
        keep = []
        for r in rows:
            vals = {str(r.get(c) or "").rstrip("/").lower() for c in ("key", "profile_url", "email", "username")}
            if n in vals:
                removed.append({"sheet": s, "who": label(s, r)})
            else:
                keep.append(r)
        if len(keep) != len(rows):
            write_sheet(wb, s, keep)
    return {"removed": removed}


def read_any(path: str) -> list[dict]:
    if path.lower().endswith((".xlsx", ".xlsm")):
        wb = load_workbook(path, read_only=True, data_only=True)
        rows = []
        for ws in wb.worksheets:
            if ws.title in (REVIEW, SOURCES, PROBLEMS):
                continue  # previews of people nobody kept yet, counts per source and problems are never leads
            header, data = read_rows(ws)
            if header:
                rows += data
        return rows
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        return list(csv.DictReader(f, dialect=dialect))


def map_row(r: dict) -> dict:
    out_row: dict = {}
    extra: dict = {}
    for k, v in r.items():
        if v in (None, ""):
            continue
        n = norm(k)
        target = n if any(n in cols for cols in SOURCE.values()) or n in WORK or n == "key" else ALIASES.get(n.replace("_", ""))
        if target:
            if target in out_row:
                out_row[target] = f"{out_row[target]}, {v}" if target == "location" else out_row[target]
            else:
                out_row[target] = v
        else:
            extra[n or "column"] = v
    # "LinkedIn URL" columns usually hold people's profiles, not company pages.
    if "/in/" in str(out_row.get("linkedin_url", "")) and not out_row.get("profile_url"):
        out_row["profile_url"] = out_row.pop("linkedin_url")
    if "_first" in out_row or "_last" in out_row:
        out_row.setdefault("name", " ".join(str(out_row.get(x, "")) for x in ("_first", "_last")).strip())
    out_row.pop("_first", None)
    out_row.pop("_last", None)
    if isinstance(out_row.get("status"), str):
        s = out_row["status"].strip().lower().replace(" ", "_")
        s = LEGACY.get(s, s)
        out_row["status"] = s if s in STATUSES else "new"
    out_row.update({f"import_{k}": v for k, v in extra.items()})
    return out_row


def guess_sheet(r: dict) -> str:
    url = str(r.get("profile_url") or "")
    if "reddit.com" in url or r.get("subreddit"):
        return "Reddit"
    if "instagram.com" in url:
        return "Instagram"
    if "linkedin.com/company" in url or (r.get("company") and not r.get("name") and not r.get("username")):
        return "Companies"
    return "LinkedIn"


def cmd_import(wb, path: str, sheet: str | None) -> dict:
    rows = [map_row(r) for r in read_any(path)]
    incoming = [(sheet or guess_sheet(r), r) for r in rows]
    skipped = sum(1 for s, r in incoming if not (r.get("key") or derive_key(s, r)))
    res = merge_rows(wb, incoming, None, source_label=f"import: {os.path.basename(path)}")
    res["rows_in_file"] = len(rows)
    res["skipped_without_identifier"] = skipped
    return res


def cmd_export(wb, path: str, sheet: str | None, statuses: str | None) -> dict:
    data = all_rows(wb)
    wanted = set(statuses.split(",")) if statuses else None
    rows = []
    for s, rs in data.items():
        if sheet and s != sheet:
            continue
        for r in rs:
            if wanted and (r.get("status") or "new") not in wanted:
                continue
            rows.append({"sheet": s, **{k: v for k, v in r.items() if k != "key"}, "key": r.get("key")})
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([safe_cell(r.get(c)) for c in cols])
    return {"exported": len(rows), "file": path}


def safe_cell(v):
    if v is None:
        return ""
    if isinstance(v, dt.datetime):
        s = v.date().isoformat() if (v.hour, v.minute, v.second) == (0, 0, 0) else v.isoformat(sep=" ", timespec="minutes")
    elif isinstance(v, dt.date):
        s = v.isoformat()
    else:
        s = str(v)
    return "'" + s if s[:1] in ("=", "+", "-", "@") else s


def cmd_summary(wb) -> dict:
    data = all_rows(wb)
    live, expired = split_expired(read_review(wb))
    week = sources_report(wb, STOP_RULE["days"], None)
    return {
        "sheets": {s: {st: n for st in STATUSES if (n := sum(1 for r in rs if (r.get("status") or "new") == st))} | {"total": len(rs)} for s, rs in data.items()},
        "touches_due": len(touches_due(data, 0)),
        "touches_next_7_days": len(touches_due(data, 7)),
        "to_review": {"waiting": len(live), "expired": len(expired)},
        # sources run in the stop rule's window, and how many of them the rule marks stop
        "sources": {"stop": len(week["stop"]), "last_7_days": sum(1 for s in week["sources"] if s["runs"])},
        # fitting Reddit posts logged in the Problems sheet in the report's default window
        "problems": {"last_30_days": problems_report(wb, PROBLEMS_DAYS)["posts"]},
    }


# ---------- the To review sheet ----------


def now_utc() -> dt.datetime:
    return dt.datetime.now(UTC)


def parse_when(v) -> dt.datetime | None:
    """A moment as the server returns it ("2026-11-03 14:30 UTC"), ISO 8601 (with Z or an offset), or a date. Naive is UTC."""
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v if v.tzinfo else v.replace(tzinfo=UTC)
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day, 23, 59, tzinfo=UTC)
    if isinstance(v, (int, float)):
        try:
            return dt.datetime.fromtimestamp(v / 1000 if v > 1e12 else v, UTC)
        except (OverflowError, OSError, ValueError):
            return None
    s = str(v).strip()
    if s.upper().endswith("UTC"):
        s = s[:-3].strip()
    if s[-1:] in ("Z", "z"):
        s = s[:-1] + "+00:00"
    s = s.replace(" ", "T", 1)
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:T(\d{2}):(\d{2}))?", s)
        if not m:
            return None
        try:
            d = dt.datetime.fromisoformat(m.group(1) + (f"T{m.group(2)}:{m.group(3)}" if m.group(2) else "T23:59"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=UTC)


def fmt_when(d: dt.datetime) -> str:
    return d.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")


def id_key(v) -> str:
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v if v is not None else "").strip()


def id_value(v):
    """Result ids are numbers on the server; keep them numbers so they go straight to pick_leads."""
    k = id_key(v)
    return int(k) if k.isdigit() else k


def decision_of(r: dict) -> str:
    d = str(r.get("decision") or "").strip().lower()
    return d if d in DECISIONS else ""


def no_links(v):
    """Review rows are previews: links, email addresses and handles in a text are replaced.
    Emails go first so an address becomes [email] rather than a handle."""
    if not isinstance(v, str):
        return v
    v = re.sub(r"(?i)\b(?:https?://|www\.)\S+", "[link]", v)
    v = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", v)
    v = re.sub(r"(?<![\w.])@[\w.]{2,}", "[handle]", v)
    v = re.sub(r"(?i)(?<!\w)u_[\w-]{3,}", "[handle]", v)  # a Reddit user's profile community: u_name
    return re.sub(r"(?<![\w/])/?u/[\w-]{3,}", "[handle]", v)  # Reddit users: u/name, /u/name


def clip(v, n: int = ABOUT_CHARS):
    if v is None or v == "":
        return None
    s = " ".join(str(v).split())
    return s if len(s) <= n else s[: n - 3].rstrip() + "..."


def joined(*parts) -> str | None:
    s = ", ".join(str(p).strip() for p in parts if p not in (None, "") and str(p).strip())
    return s or None


def read_review(wb) -> list[dict]:
    if REVIEW not in wb.sheetnames:
        return []
    return [{c: r.get(c) for c in REVIEW_COLUMNS} for r in read_rows(wb[REVIEW])[1] if r.get("id") not in (None, "")]


def write_review(wb, rows: list[dict]) -> None:
    if REVIEW in wb.sheetnames:
        idx = wb.sheetnames.index(REVIEW)
        wb.remove(wb[REVIEW])
    else:
        idx = len(wb.sheetnames)
    ws = wb.create_sheet(REVIEW, idx)
    ws.append(REVIEW_COLUMNS)
    for r in rows:
        ws.append([r.get(c) for c in REVIEW_COLUMNS])
    style(ws, REVIEW_COLUMNS)
    for c, width in {"id": 10, "search_id": 14, "platform": 12, "decision": 12, "score": 8, "who": 32, "where": 26, "expires_at": 20}.items():
        ws.column_dimensions[get_column_letter(REVIEW_COLUMNS.index(c) + 1)].width = width
    col = get_column_letter(REVIEW_COLUMNS.index("decision") + 1)
    for row in range(2, ws.max_row + 1):
        ws[f"{col}{row}"].fill = WORK_FILL
    dv = DataValidation(type="list", formula1='"' + ",".join(DECISIONS) + '"', allow_blank=True)
    dv.add(f"{col}2:{col}{max(ws.max_row, 2) + 500}")
    ws.add_data_validation(dv)
    ws.freeze_panes = "E2"


def split_expired(rows: list[dict], at: dt.datetime | None = None) -> tuple[list[dict], list[dict]]:
    """Rows still waiting, and rows whose search results the server has deleted. A row without a readable time waits."""
    at = at or now_utc()
    live, gone = [], []
    for r in rows:
        when = parse_when(r.get("expires_at"))
        (gone if when is not None and when <= at else live).append(r)
    return live, gone


def prune_review(wb) -> int:
    """Drops the rows whose results are gone from the server. Runs on every write."""
    rows = read_review(wb)
    live, gone = split_expired(rows)
    if gone or REVIEW not in wb.sheetnames:
        write_review(wb, live)
    return len(gone)


def review_line(wb) -> str:
    live, _ = split_expired(read_review(wb))
    if not live:
        return "To review: 0 waiting"
    times = [t for t in (parse_when(r.get("expires_at")) for r in live) if t]
    return f"To review: {len(live)} waiting" + (f", earliest expire {fmt_when(min(times))}" if times else "")


def sheet_of_result(platform: str, r: dict) -> str:
    p = str(platform or r.get("platform") or "").strip().lower()
    if p in ("companies", "company"):
        return "Companies"
    if p == "reddit":
        return "Reddit"
    if p == "instagram":
        return "Instagram"
    if r.get("company") and not (r.get("name") or r.get("headline") or r.get("role") or r.get("who")):
        return "Companies"  # a company search on LinkedIn
    return "LinkedIn"


def preview_to_review(sheet: str, r: dict) -> dict:
    """Who, about and where from a result's preview columns."""
    if sheet == "Reddit":
        text = r.get("text")
        return {"who": clip(r.get("title"), 120) or clip(text, 80), "about": clip(text), "where": r.get("subreddit"), "posted_at": r.get("posted_at"), "signal": r.get("signal")}
    if sheet == "Instagram":
        f = r.get("followers")
        followers = f"{f} followers" if f not in (None, "") else None
        return {"who": clip(r.get("full_name"), 120) or clip(r.get("caption"), 80), "about": clip(r.get("bio") or r.get("caption")),
                "where": joined(followers, r.get("business_category")), "posted_at": r.get("posted_at"), "signal": r.get("signal")}
    if sheet == "Companies":
        return {"who": r.get("company"), "about": clip(r.get("description")), "where": joined(r.get("industry"), r.get("size")),
                "posted_at": r.get("signal_date"), "signal": clip(joined(r.get("signal"), r.get("signal_text")))}
    return {"who": r.get("name"), "about": clip(r.get("headline") or r.get("role")), "where": joined(r.get("company"), r.get("location")),
            "posted_at": r.get("signal_date"), "signal": clip(joined(r.get("signal"), r.get("signal_text")))}


def review_items(payload) -> list[tuple[dict, dict]]:
    """(row, defaults) pairs from a search result, a list of them, get_results output, or rows shaped to the sheet."""
    out_items: list[tuple[dict, dict]] = []
    if isinstance(payload, dict) and "results" in payload:
        d = {"search_id": payload.get("search_id"), "platform": payload.get("platform"), "expires_at": payload.get("stored_until")}
        out_items += [(r, d) for r in payload.get("results") or [] if isinstance(r, dict)]
    elif isinstance(payload, dict) and "sheets" in payload:
        for s, rs in (payload.get("sheets") or {}).items():
            if s in SHEETS:
                d = {"platform": s.lower(), "expires_at": payload.get("stored_until")}
                out_items += [(r, d) for r in rs if isinstance(r, dict)]
    elif isinstance(payload, list):
        for x in payload:
            if isinstance(x, dict) and "results" in x:
                out_items += review_items(x)
            elif isinstance(x, dict):
                out_items.append((x, {}))
    return out_items


def labelled(score, reason) -> bool:
    """A score below GOOD_SCORE needs a reason that starts with one of LOW_SCORE_LABELS (case and leading spaces
    ignored). A row without a readable score, or scored GOOD_SCORE or more, needs no label."""
    s = as_score(score)
    low = s is not None and s < GOOD_SCORE
    return not low or str(reason or "").strip().lower().startswith(LOW_SCORE_LABELS)


def review_add(wb, payload, source: str | None, campaign: str | None) -> dict:
    rows = read_review(wb)
    live, gone = split_expired(rows)
    have = {id_key(r.get("id")) for r in live}
    added = already = expired_skipped = skipped = unlabelled = 0
    added_rows: list[dict] = []  # what log_problems reads: the row before masking, plus the item's phrase
    at = now_utc()
    for item, defaults in review_items(payload):
        rid = item.get("id")
        if rid in (None, "") or item.get("state") in ("picked", "excluded"):
            skipped += 1  # kept rows belong in a platform sheet; excluded ones were turned down
            continue
        if id_key(rid) in have:
            already += 1
            continue
        when = parse_when(item.get("expires_at") or item.get("stored_until") or defaults.get("expires_at"))
        if when is None:
            skipped += 1  # without an expiry the row could outlive the server's results
            continue
        if when <= at:
            expired_skipped += 1
            continue
        sheet = sheet_of_result(item.get("platform") or defaults.get("platform"), item)
        row = preview_to_review(sheet, item)
        for c in ("score", "score_reason", "who", "about", "where", "posted_at", "signal", "campaign", "source", "decision"):
            if item.get(c) not in (None, ""):
                row[c] = item[c]
        row.update({
            "id": id_value(rid),
            "search_id": item.get("search_id") or defaults.get("search_id"),
            "platform": sheet.lower(),
            "decision": decision_of(row) or None,
            "about": clip(row.get("about")),
            "score_reason": clip(row.get("score_reason")),
            "expires_at": fmt_when(when),
            "found_on": TODAY.isoformat(),
        })
        row["campaign"] = row.get("campaign") or campaign
        row["source"] = row.get("source") or source
        live.append({c: no_links(row.get(c)) for c in REVIEW_COLUMNS})
        added_rows.append(dict(row, phrase=item.get("phrase")))
        have.add(id_key(rid))
        added += 1
        if not labelled(row.get("score"), row.get("score_reason")):
            unlabelled += 1  # written anyway: a run without labels must not lose its finds
    write_review(wb, live)
    res = {"added": added, "already_there": already, "expired_removed": len(gone), "waiting": len(live)}
    if expired_skipped:
        res["expired_skipped"] = expired_skipped
    if skipped:
        res["skipped"] = skipped
    if unlabelled:
        res["unlabelled"] = unlabelled
    # The run's counts per source go to the Sources sheet on their own, so no find leaves a hole in the week.
    logged = log_sources(wb, payload, source, campaign, results_only=True)["logged"]
    if logged:
        res["sources_logged"] = logged
    # What each fitting Reddit post was about goes to the Problems sheet, kept or not, so a month can be counted.
    problems = log_problems(wb, added_rows, campaign, source)
    if problems:
        res["problems_logged"] = problems
    return res


def review_list(wb, platform: str | None, decision: str | None, include_expired: bool) -> dict:
    rows = read_review(wb)
    live, gone = split_expired(rows)
    shown = [dict(r) for r in live] + ([dict(r, expired=True) for r in gone] if include_expired else [])
    if platform:
        shown = [r for r in shown if str(r.get("platform") or "").strip().lower() == platform.strip().lower()]
    if decision:
        want = "" if decision.strip().lower() == "undecided" else decision.strip().lower()
        shown = [r for r in shown if decision_of(r) == want]
    for r in shown:
        r["id"] = id_value(r.get("id"))
        r["decision"] = decision_of(r) or None
    times = [t for t in (parse_when(r.get("expires_at")) for r in live) if t]
    res = {
        "rows": shown,
        "waiting": len(live),
        "expired": len(gone),
        "decisions": {d: sum(1 for r in live if decision_of(r) == d) for d in DECISIONS} | {"undecided": sum(1 for r in live if not decision_of(r))},
    }
    if times:
        res["earliest_expires"] = fmt_when(min(times))
    return res


def review_remove(wb, ids: list[str], expired: bool, decided: bool, everything: bool) -> dict:
    if not (ids or expired or decided or everything):
        return {"error": "Say which rows to remove: ids, --expired, --decided or --all."}
    rows = read_review(wb)
    _, gone = split_expired(rows)
    gone_ids = {id_key(r.get("id")) for r in gone}
    wanted = {id_key(i) for i in ids}
    keep = []
    for r in rows:
        k = id_key(r.get("id"))
        if everything or k in wanted or (expired and k in gone_ids) or (decided and decision_of(r)):
            continue
        keep.append(r)
    write_review(wb, keep)
    return {"removed": len(rows) - len(keep), "left": len(keep)}


# ---------- the Sources sheet ----------


def as_int(v) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def as_score(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


USER_PROFILE_KEY = "r/[user profile]"


def subreddit_key(v) -> str:
    """`r/<name>` lowercased. A post made in a user's own profile (community `u_<username>`, or `u/<username>`)
    counts under one fixed key, so the sheet never holds a username."""
    name = re.sub(r"(?i)^/?r/", "", str(v or "").strip()).strip("/ ").lower()
    if re.match(r"u[_/]", name):
        return USER_PROFILE_KEY
    return f"r/{name}" if name else ""


def word_key(v) -> str:
    word = " ".join(str(v or "").split()).strip("\"' ").lower()
    return f"bio: {word}" if word else ""


def label_key(v) -> str:
    return re.sub(r"\s*\(page \d+\)$", "", " ".join(str(v or "").split()))


def source_key(platform: str, value) -> str:
    """The key a run is counted under and a kept lead is matched on: `r/<subreddit>` lowercased (with or without the
    leading r/ on Reddit), `bio: <word>` lowercased, or a search's label without its ` (page N)` suffix, so the pages
    of one search add up. A link in a label (the post of a commenters search) becomes [link] and a handle [handle], and
    a Reddit user's profile counts under r/[user profile]: the sheet holds no URL and no username."""
    v = " ".join(str(value or "").split())
    if re.match(r"(?i)^/?r/\w", v) or (platform == "reddit" and re.fullmatch(r"(?i)\w{2,21}|/?u[_/][\w-]+", v)):
        key = subreddit_key(v)
    elif v.lower().startswith("bio:"):
        key = word_key(v[4:])
    else:
        key = label_key(v)
    return str(no_links(key) or "")


def words_of(v) -> list[str]:
    items = v if isinstance(v, (list, tuple)) else str(v or "").split(",")
    return [w for w in (str(x).strip() for x in items) if w]


def row_keys(platform: str, row: dict, label) -> list[str]:
    """The sources one find counts under: its subreddit on Reddit; on Instagram each bio word it matched (a bio that
    matched two words counts under both, as `shown_by_word` does), read from `matched_words` or from a signal
    `bio matches "w1", "w2"`; otherwise the search's label."""
    keys: list[str] = []
    if platform == "reddit" and row.get("subreddit"):
        keys = [source_key(platform, "r/" + re.sub(r"(?i)^/?r/", "", str(row["subreddit"]).strip()))]
    elif platform == "instagram":
        words = words_of(row.get("matched_words"))
        signal = str(row.get("signal") or "")
        if not words and signal.lower().startswith("bio matches"):
            words = re.findall(r'"([^"]+)"', signal)
        keys = [source_key(platform, f"bio: {w}") for w in words]
    if not keys and label not in (None, ""):
        keys = [source_key(platform, label)]
    return list(dict.fromkeys(k for k in keys if k))


def platform_of(v, row: dict | None = None) -> str:
    """linkedin, reddit or instagram; a company search counts under linkedin. Without a platform, read from the row."""
    p = str(v or "").strip().lower()
    if p in ("linkedin", "companies", "company"):
        return "linkedin"
    if p:
        return p
    row = row or {}
    if row.get("subreddit"):
        return "reddit"
    if row.get("matched_words") or row.get("full_name") or row.get("bio"):
        return "instagram"
    return "linkedin"


def is_search_result(x) -> bool:
    """A finished search as a tool returned it: a search id and a list of results (a running or failed one has none)."""
    return isinstance(x, dict) and x.get("search_id") not in (None, "") and isinstance(x.get("results"), list)


def run_counts(result: dict) -> tuple[str, list[tuple[str, int, int]]]:
    """(platform, [(key, results, good)]) for one search result. Results per key come from `shown_by_subreddit` or
    `shown_by_word` when the result has them (so a scan with `results` trimmed to the fitting posts still counts every
    post shown), else from `shown` (or the number of rows); good is the rows scored GOOD_SCORE or more."""
    rows = [r for r in result.get("results") or [] if isinstance(r, dict)]
    platform = platform_of(result.get("platform"), rows[0] if rows else None)
    label = result.get("what") or result.get("search") or f"{platform} search"
    shown: dict[str, int] = {}
    for field, keyer in (("shown_by_subreddit", subreddit_key), ("shown_by_word", word_key)):
        counts = result.get(field)
        if isinstance(counts, dict) and counts:
            for k, n in counts.items():
                key = str(no_links(keyer(k)) or "")
                if key:
                    shown[key] = shown.get(key, 0) + as_int(n)
            break
    found: dict[str, int] = {}
    good: dict[str, int] = {}
    for r in rows:
        score = as_score(r.get("score"))
        for k in row_keys(platform, r, label):
            found[k] = found.get(k, 0) + 1
            if score is not None and score >= GOOD_SCORE:
                good[k] = good.get(k, 0) + 1
    if not shown:
        whole = source_key(platform, label)
        if set(found) <= {whole}:
            n = result.get("shown")
            shown = {whole: as_int(n) if n not in (None, "") else len(rows)}
        else:
            shown = dict(found)  # a Reddit keyword search: per subreddit, from its rows
    for k, n in found.items():
        shown.setdefault(k, n)  # a find under a key the counts didn't name
    return platform, [(k, max(n, good.get(k, 0)), good.get(k, 0)) for k, n in shown.items()]


def read_sources(wb) -> list[dict]:
    if SOURCES not in wb.sheetnames:
        return []
    rows = []
    for r in read_rows(wb[SOURCES])[1]:
        if r.get("key") in (None, ""):
            continue
        row = {c: r.get(c) for c in SOURCES_COLUMNS}
        d = to_date(row["date"])
        row["date"] = d.isoformat() if d else row["date"]
        row["platform"] = str(row.get("platform") or "").strip().lower()
        row["key"] = str(row["key"])
        row["results"] = as_int(row["results"])
        row["good"] = as_int(row["good"])
        row["search_id"] = id_value(row["search_id"]) if id_key(row["search_id"]) else None
        rows.append(row)
    return rows


def write_sources(wb, rows: list[dict]) -> None:
    if SOURCES in wb.sheetnames:
        idx = wb.sheetnames.index(SOURCES)
        wb.remove(wb[SOURCES])
    else:
        idx = len(wb.sheetnames)
    ws = wb.create_sheet(SOURCES, idx)
    ws.append(SOURCES_COLUMNS)
    for r in rows:
        ws.append([r.get(c) for c in SOURCES_COLUMNS])
    style(ws, SOURCES_COLUMNS)
    for c, width in {"date": 12, "platform": 12, "key": 48, "results": 10, "good": 10, "search_id": 12, "by": 18, "campaign": 18}.items():
        letter = get_column_letter(SOURCES_COLUMNS.index(c) + 1)
        ws.column_dimensions[letter].width = width
        ws.column_dimensions[letter].hidden = False  # style() hides a column named key on the lead sheets
    ws.freeze_panes = "D2"


def prune_sources(wb) -> int:
    """Drops runs older than SOURCES_KEEP_DAYS. Runs on every write; adds the sheet to older workbooks."""
    rows = read_sources(wb)
    cutoff = TODAY - dt.timedelta(days=SOURCES_KEEP_DAYS)
    keep = [r for r in rows if (d := to_date(r.get("date"))) is None or d >= cutoff]
    if len(keep) != len(rows) or SOURCES not in wb.sheetnames:
        write_sources(wb, keep)
    return len(rows) - len(keep)


def log_sources(wb, payload, by: str | None, campaign: str | None, results_only: bool = False) -> dict:
    """Records a run per source: from a search result (or a list of them), or, unless results_only, from rows
    {platform, key, results, good, search_id?, date?}. A (search_id, key) already in the sheet is not logged again,
    so adding the same result twice counts it once."""
    rows = read_sources(wb)
    have = {(id_key(r.get("search_id")), r["key"]) for r in rows if id_key(r.get("search_id"))}
    logged = already = 0

    def add(entry: dict) -> None:
        nonlocal logged, already
        sid = id_key(entry.get("search_id"))
        if sid and (sid, entry["key"]) in have:
            already += 1
            return
        rows.append(entry)
        logged += 1
        if sid:
            have.add((sid, entry["key"]))

    items = payload if isinstance(payload, list) else [payload]
    for item in items:
        if is_search_result(item):
            if str(item.get("status") or "done") not in ("done", ""):
                continue
            platform, counts = run_counts(item)
            for key, results, good in counts:
                add({"date": TODAY.isoformat(), "platform": platform, "key": key, "results": results, "good": good,
                     "search_id": id_value(item["search_id"]), "by": by, "campaign": campaign})
        elif not results_only and isinstance(item, dict) and item.get("key") not in (None, "") and not isinstance(item.get("results"), list):
            platform = platform_of(item.get("platform"))
            key = source_key(platform, item.get("key"))
            if not key:
                continue
            sid = item.get("search_id")
            add({"date": (to_date(item.get("date")) or TODAY).isoformat(), "platform": platform, "key": key,
                 "results": as_int(item.get("results")), "good": as_int(item.get("good")),
                 "search_id": id_value(sid) if id_key(sid) else None, "by": item.get("by") or by, "campaign": item.get("campaign") or campaign})
    if logged:
        write_sources(wb, rows)
    return {"logged": logged, "already_there": already, "total": len(rows)}


def verdict(results: int, good: int) -> str:
    if results < STOP_RULE["min_results"]:
        return "too few to judge"  # a quiet subreddit or a rare bio word is not a bad one
    return "stop" if good < STOP_RULE["min_good"] else "ok"


def rule_line() -> str:
    return f"Stop rule: fewer than {STOP_RULE['min_good']} good leads from {STOP_RULE['min_results']} or more results in {STOP_RULE['days']} days"


def sources_report(wb, days: int, platform: str | None) -> dict:
    """Results, good leads and kept per source over the last `days` days (today included), with the stop rule's verdict.
    Kept comes from the platform sheets: rows found in the window, imports left out, keyed like the runs."""
    days = max(1, int(days))
    since = TODAY - dt.timedelta(days=days - 1)
    want = platform_of(platform) if platform else None
    agg: dict[tuple[str, str], dict] = {}

    def entry(p: str, k: str) -> dict:
        return agg.setdefault((p, k), {"platform": p, "key": k, "runs": 0, "results": 0, "good": 0, "kept": 0, "last_run": None})

    for r in read_sources(wb):
        d = to_date(r.get("date"))
        if d is None or d < since or (want and r["platform"] != want):
            continue
        e = entry(r["platform"], r["key"])
        e["runs"] += 1
        e["results"] += r["results"]
        e["good"] += r["good"]
        e["last_run"] = max(e["last_run"] or "", d.isoformat())
    kept_rows: dict[str, int] = {}
    for sheet, rows in all_rows(wb).items():
        p = SHEET_PLATFORM[sheet]
        if want and p != want:
            continue
        for r in rows:
            d = to_date(r.get("found_on"))
            if d is None or d < since or str(r.get("source") or "").strip().lower().startswith("import"):
                continue
            kept_rows[p] = kept_rows.get(p, 0) + 1
            for k in row_keys(p, r, r.get("search")):
                entry(p, k)["kept"] += 1
    order = {p: i for i, p in enumerate(PLATFORMS)}

    def rank(e: dict):
        ratio = e["good"] / e["results"] if e["results"] else None
        return (order.get(e["platform"], len(order)), e["platform"], ratio is None, -(ratio or 0), e["key"])

    sources = sorted(agg.values(), key=rank)
    platforms: dict[str, dict] = {}
    for e in sources:
        e["verdict"] = verdict(e["results"], e["good"])
        pl = platforms.setdefault(e["platform"], {"results": 0, "good": 0, "kept": kept_rows.get(e["platform"], 0), "stop": []})
        pl["results"] += e["results"]
        pl["good"] += e["good"]
        if e["verdict"] == "stop":
            pl["stop"].append(e["key"])
    return {
        "days": days,
        "since": since.isoformat(),
        "rule": dict(STOP_RULE),
        "sources": sources,
        "platforms": platforms,
        "stop": [{"platform": e["platform"], "key": e["key"], "results": e["results"], "good": e["good"]} for e in sources if e["verdict"] == "stop"],
    }


# ---------- the Problems sheet ----------


def tidy(v) -> str:
    """Surrounding spaces and one trailing full stop removed."""
    s = str(v or "").strip()
    return s[:-1].rstrip() if s.endswith(".") else s


def masked(v, n: int) -> str:
    return str(clip(no_links(tidy(v)), n) or "")


def parse_reason(reason) -> tuple[str, str]:
    """(problem, ask) from a Reddit reason `<the problem, in short>; asks for <the ask>`. The problem is the text up to
    the first `;` (the whole reason when there is none); the ask is what follows `asks for` after it (any case), empty
    without a `;` or an `asks for`. Both lose surrounding spaces and a trailing full stop, have links, emails and
    handles masked, and are clipped to PROBLEM_CHARS."""
    head, sep, rest = str(reason or "").partition(";")
    m = re.search(r"(?is)\basks\s+for\b(.*)", rest) if sep else None
    return masked(head, PROBLEM_CHARS), masked(m.group(1) if m else "", PROBLEM_CHARS)


def read_problems(wb) -> list[dict]:
    if PROBLEMS not in wb.sheetnames:
        return []
    rows = []
    for r in read_rows(wb[PROBLEMS])[1]:
        if r.get("problem") in (None, ""):
            continue
        row = {c: r.get(c) for c in PROBLEMS_COLUMNS}
        d = to_date(row["date"])
        row["date"] = d.isoformat() if d else row["date"]
        for c in ("subreddit", "problem", "ask", "phrase", "campaign", "source"):
            row[c] = "" if row[c] is None else str(row[c])
        score = as_score(row["score"])
        row["score"] = int(score) if score is not None and score.is_integer() else score
        for c in ("search_id", "id"):
            row[c] = id_value(row[c]) if id_key(row[c]) else None
        rows.append(row)
    return rows


def write_problems(wb, rows: list[dict]) -> None:
    if PROBLEMS in wb.sheetnames:
        idx = wb.sheetnames.index(PROBLEMS)
        wb.remove(wb[PROBLEMS])
    else:
        idx = len(wb.sheetnames)
    ws = wb.create_sheet(PROBLEMS, idx)
    ws.append(PROBLEMS_COLUMNS)
    for r in rows:
        ws.append([None if r.get(c) == "" else r.get(c) for c in PROBLEMS_COLUMNS])
    style(ws, PROBLEMS_COLUMNS)
    for c, width in {"date": 12, "subreddit": 24, "score": 8, "problem": 48, "ask": 36, "phrase": 48, "search_id": 12, "id": 10, "campaign": 18, "source": 18}.items():
        ws.column_dimensions[get_column_letter(PROBLEMS_COLUMNS.index(c) + 1)].width = width
    ws.freeze_panes = "E2"


def prune_problems(wb) -> int:
    """Drops rows older than PROBLEMS_KEEP_DAYS. Runs on every write; adds the sheet to older workbooks."""
    rows = read_problems(wb)
    cutoff = TODAY - dt.timedelta(days=PROBLEMS_KEEP_DAYS)
    keep = [r for r in rows if (d := to_date(r.get("date"))) is None or d >= cutoff]
    if len(keep) != len(rows) or PROBLEMS not in wb.sheetnames:
        write_problems(wb, keep)
    return len(rows) - len(keep)


def log_problems(wb, added_rows: list[dict], campaign: str | None, source: str | None) -> int:
    """Logs the fitting Reddit posts `review add` just wrote (its rows before masking, with the item's `phrase`): a row
    on reddit scored GOOD_SCORE or more whose reason has the form `<problem>; asks for <ask>` (it holds a `;`). Rows
    from the signals source are skipped: their reason quotes the post itself. A (search_id, id) already in the sheet is
    not logged again. The subreddit goes through subreddit_key (a user's profile becomes r/[user profile]); the problem,
    the ask, the phrase, the campaign and the source have links, emails and handles masked, and the problem, the ask
    and the phrase are clipped. Returns the number of rows logged."""
    rows = read_problems(wb)
    have = {(id_key(r.get("search_id")), id_key(r.get("id"))) for r in rows}
    logged = 0
    for r in added_rows:
        platform = str(r.get("platform") or "").strip().lower()
        score = as_score(r.get("score"))
        if not (platform == "reddit" and score is not None and score >= GOOD_SCORE):
            continue
        row_source = r.get("source") or source
        if str(row_source or "").strip().lower() == "signals":
            continue  # the signals playbook quotes the post as the reason, which may hold a name
        reason = str(r.get("score_reason") or "")
        if ";" not in reason:
            continue  # only the `<problem>; asks for <ask>` form names a problem without quoting the post
        problem, ask = parse_reason(reason)
        if not problem:
            continue  # a reason that names no problem has nothing to count
        ident = (id_key(r.get("search_id")), id_key(r.get("id")))
        if ident in have:
            continue
        have.add(ident)
        sid, rid = r.get("search_id"), r.get("id")
        rows.append({
            "date": TODAY.isoformat(),
            "subreddit": str(no_links(subreddit_key(r.get("where"))) or ""),
            "score": int(score) if score.is_integer() else score,
            "problem": problem,
            "ask": ask,
            "phrase": str(clip(no_links(r.get("phrase")), PHRASE_CHARS) or ""),
            "search_id": id_value(sid) if id_key(sid) else None,
            "id": id_value(rid) if id_key(rid) else None,
            "campaign": str(no_links(r.get("campaign") or campaign) or ""),
            "source": str(no_links(row_source) or ""),
        })
        logged += 1
    if logged:
        write_problems(wb, rows)
    return logged


def wording(v) -> str:
    """The key a problem or an ask is counted under: lowercase, whitespace collapsed, trailing . ! and , removed."""
    return re.sub(r"[.!,\s]+$", "", " ".join(str(v or "").split()).lower())


def most_first(counts: dict[str, int]) -> dict[str, int]:
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower())))


def problems_report(wb, days: int) -> dict:
    """The Problems rows of the last `days` days (today included), counted per wording of the problem: the asks, the
    subreddits, up to PHRASES_PER_PROBLEM distinct phrases in order of first appearance and the last date per problem,
    most posts first, then the most recent, then alphabetical. It judges nothing: grouping wordings that mean the same
    is left to Claude, as the note says."""
    days = max(1, int(days))
    since = TODAY - dt.timedelta(days=days - 1)
    groups: dict[str, dict] = {}
    asks: dict[str, int] = {}
    subreddits: dict[str, int] = {}
    ask_names: dict[str, str] = {}  # an ask is shown as first written
    posts = 0
    for r in read_problems(wb):
        d = to_date(r.get("date"))
        if d is None or d < since:
            continue
        posts += 1
        g = groups.setdefault(wording(r["problem"]), {"problem": r["problem"], "count": 0, "asks": {}, "subreddits": {}, "phrases": [], "last_seen": None})
        g["count"] += 1
        g["last_seen"] = max(g["last_seen"] or "", d.isoformat())
        if r["ask"]:
            name = ask_names.setdefault(wording(r["ask"]), r["ask"])
            g["asks"][name] = g["asks"].get(name, 0) + 1
            asks[name] = asks.get(name, 0) + 1
        if r["subreddit"]:
            g["subreddits"][r["subreddit"]] = g["subreddits"].get(r["subreddit"], 0) + 1
            subreddits[r["subreddit"]] = subreddits.get(r["subreddit"], 0) + 1
        phrase = r["phrase"]
        if phrase and len(g["phrases"]) < PHRASES_PER_PROBLEM and wording(phrase) not in {wording(p) for p in g["phrases"]}:
            g["phrases"].append(phrase)
    problems = sorted(groups.values(), key=lambda g: (-g["count"], -dt.date.fromisoformat(g["last_seen"]).toordinal(), g["problem"].lower()))
    for g in problems:
        g["asks"] = most_first(g["asks"])
        g["subreddits"] = most_first(g["subreddits"])
    return {
        "days": days,
        "since": since.isoformat(),
        "posts": posts,
        "problems": problems,
        "asks": most_first(asks),
        "subreddits": most_first(subreddits),
        "note": PROBLEMS_NOTE,
    }


# ---------- the write lock ----------


def lock_path(path: str) -> str:
    folder, name = os.path.split(os.path.abspath(path))
    return os.path.join(folder, f".{name}.lock")


def lock_wait() -> float:
    try:
        return max(0.0, float(os.environ.get("LF_LOCK_WAIT", "60")))
    except ValueError:
        return 60.0


def is_stale(path: str) -> bool:
    return time.time() - os.path.getmtime(path) > LOCK_STALE_SECONDS


def take_over_stale_lock(lock: str) -> bool:
    """Removes a lock left by a crashed task. Returns True when the caller should try to
    create the lock again now, False when a live lock is in place and the caller waits.

    The lock is moved aside with one rename, so when several tasks find the same stale lock
    only one of them gets it; the others see it gone and try again. If the file moved aside
    turns out to be fresh (a live lock created after the staleness check), it is put back."""
    moved = f"{lock}.stale.{os.getpid()}"
    try:
        if not is_stale(lock):
            return False
        try:
            os.unlink(moved)  # a leftover from an earlier crash of a task with the same pid
        except FileNotFoundError:
            pass
        os.rename(lock, moved)
    except FileNotFoundError:
        return True  # released or taken over by another task in between
    try:
        if is_stale(moved):
            return True
        restore_lock(moved, lock)
        return False
    finally:
        try:
            os.unlink(moved)
        except FileNotFoundError:
            pass


def restore_lock(moved: str, lock: str) -> None:
    """Puts a live lock back under its name, unless a new lock is already there."""
    try:
        os.link(moved, lock)
        return
    except FileExistsError:
        return
    except OSError:
        pass  # hard links not supported here: recreate it with the same token
    try:
        with open(moved, encoding="utf-8") as f:
            token = f.read()
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except (FileExistsError, FileNotFoundError):
        return
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(token)


def acquire_lock(path: str) -> str:
    """Creates the lock file or waits for it. Returns the token written into it."""
    lock = lock_path(path)
    os.makedirs(os.path.dirname(lock), exist_ok=True)
    token = f"{os.getpid()} {dt.datetime.now().isoformat(timespec='seconds')}"
    deadline = time.monotonic() + lock_wait()
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(token)
            return token
        except FileExistsError:
            if take_over_stale_lock(lock):
                continue
            if time.monotonic() >= deadline:
                out({"error": f"Another Lead Finder task is writing {path}. Try again in a minute."})
                sys.exit(4)
            time.sleep(LOCK_POLL_SECONDS)


def release_lock(path: str, token: str) -> None:
    lock = lock_path(path)
    try:
        with open(lock, encoding="utf-8") as f:
            if f.read() != token:
                return  # not ours any more
        os.unlink(lock)
    except FileNotFoundError:
        pass


# ---------- command line ----------


def parse_args(args: list[str]) -> tuple[dict, set, list]:
    opts: dict = {}
    flags: set = set()
    positional: list = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in FLAGS:
            flags.add(a)
            i += 1
        elif a.startswith("--"):
            if i + 1 < len(args):
                opts[a] = args[i + 1]
            i += 2
        else:
            positional.append(a)
            i += 1
    return opts, flags, positional


def main(argv: list[str]) -> None:
    if len(argv) < 3 or argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(1)
    cmd = argv[1]
    sub = None
    if cmd in SUBCOMMANDS:
        if len(argv) < 4 or argv[2] not in SUBCOMMANDS[cmd]:
            print(__doc__)
            sys.exit(1)
        sub, path, rest = argv[2], argv[3], argv[4:]
    else:
        path, rest = argv[2], argv[3:]
    opts, flags, positional = parse_args(rest)

    if cmd in MUTATING or (cmd, sub) in MUTATING_SUB:
        token = acquire_lock(path)
        try:
            run(cmd, sub, path, opts, flags, positional)
        finally:
            release_lock(path, token)
    else:
        run(cmd, sub, path, opts, flags, positional)


def run(cmd: str, sub: str | None, path: str, opts: dict, flags: set, positional: list) -> None:
    if cmd == "create":
        if os.path.exists(path):
            out({"exists": path})
            return
        create(path)
        out({"created": path, "sheets": GENERATED + SHEETS + [REVIEW, SOURCES, PROBLEMS]})
        return

    wb = load(path)
    if cmd == "problems":
        out(problems_report(wb, as_int(opts.get("--days")) or PROBLEMS_DAYS))
        return
    if cmd == "sources":
        if sub == "report":
            out(sources_report(wb, as_int(opts.get("--days")) or STOP_RULE["days"], opts.get("--platform")))
            return
        with open(positional[0], encoding="utf-8") as f:
            payload = json.load(f)
        campaign = opts.get("--campaign") or os.path.splitext(os.path.basename(path))[0]
        res = log_sources(wb, payload, opts.get("--by"), campaign)
    elif cmd == "review":
        if sub == "list":
            out(review_list(wb, opts.get("--platform"), opts.get("--decision"), "--all" in flags))
            return
        if sub == "add":
            with open(positional[0], encoding="utf-8") as f:
                payload = json.load(f)
            campaign = opts.get("--campaign") or os.path.splitext(os.path.basename(path))[0]
            res = review_add(wb, payload, opts.get("--source"), campaign)
        else:
            res = review_remove(wb, positional, "--expired" in flags, "--decided" in flags, "--all" in flags)
    elif cmd == "merge":
        status = opts.get("--status")
        if status:
            status = LEGACY.get(status, status)
            if status not in STATUSES:
                raise SystemExit(f"Unknown status {status}. Use one of: {', '.join(STATUSES)}")
        with open(positional[0], encoding="utf-8") as f:
            payload = json.load(f)
        res = merge_rows(wb, incoming_rows(payload), opts.get("--campaign"), status=status)
    elif cmd == "update":
        res = cmd_update(wb, positional[0], positional[1:])
    elif cmd == "interact":
        res = cmd_interact(wb, positional[0], opts.get("--by", ""), opts.get("--channel", "linkedin"), opts.get("--kind", "comment"), opts.get("--note"), opts.get("--url"))
    elif cmd == "remove":
        res = cmd_remove(wb, positional[0])
    elif cmd == "import":
        res = cmd_import(wb, positional[0], opts.get("--sheet"))
    elif cmd == "export":
        out(cmd_export(wb, positional[0], opts.get("--sheet"), opts.get("--status")))
        return
    elif cmd == "due":
        out({"due": touches_due(all_rows(wb), int(opts.get("--days", "0")))})
        return
    elif cmd == "summary":
        out(cmd_summary(wb))
        return
    elif cmd == "rebuild":
        res = {"rebuilt": True}
    else:
        print(__doc__)
        sys.exit(1)
    if "error" not in res:
        write(wb, path)
    out(res)


if __name__ == "__main__":
    main(sys.argv)
