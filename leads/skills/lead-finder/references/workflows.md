# Workflows

`S` below is `${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py`.

## Set up (first run)

1. `my_account`: show plan, quota, status, token. If the account waits for approval or has no token, say so and continue with the file setup anyway.
2. Create the folders `campaigns/`, `templates/`, `offers/`, `leads/`, `imports/`, `exports/`, and `README.md` (text in `folder.md`). Never overwrite existing files.
3. Copy the starter templates from this skill's `assets/templates/` into `templates/` (skip files that exist).
4. The offer: `get_offer`. If there's none, run the `offer-builder` skill (one question at a time, saved on the server after each answer). Write `offer.md` from `get_offer`'s markdown.
5. Propose 2-3 target segments with a one-line reason each. The user picks one: write `campaigns/<slug>.md`, then `python3 "$S" create leads/<slug>.xlsx`.
6. Suggest a first search (the warmest source for this offer) and say what it costs and how it counts against the quota.

## Find leads

1. `get_offer` (or `offer.md`) and the campaign file (ideal customer, exclusions, learnings).
2. Pick the source (say why):
   - Someone asking for it now: `search_reddit` (phrases people would write, a subreddit when known), `search_linkedin_posts`, `search_instagram` (hashtags or keywords).
   - People reacting to a relevant post (a competitor's launch, an influencer's post on the problem): `search_post_engagers`.
   - Companies with a reason to buy: `search_hiring` (a role they'd replace or support), `search_ads` (budget), `search_companies`; keep the good ones (merge the Companies rows), then `search_linkedin_people` with `company_urls` for the right roles there.
   - A cold list by profile: `search_linkedin_people` (several title variants; LinkedIn location names; `exclude_company_urls` from the campaign's exclusions).
3. Small first (10-25), then more once the user likes the fit. Mention the cost and the quota left.
4. If the result says `running`, tell the user and call `check_search` with the search_id after ~30-60 seconds.
5. Present a compact table, best first: score (1-10), who, role and company (or subreddit / handle), the signal, one-line reason. Say how many were hidden as already delivered.
6. Ask which to keep ("1-5 and 8", "all but 3", "the 8+"). `pick_leads` with the ids (or all: true); `exclude_leads` for the clear misfits.
7. `get_results`, add scores, merge into the campaign's workbook (see `workbook.md`). Report added and updated counts.
8. Write what the user liked or rejected, and why, into the campaign's "Learnings". Use it next time.

`more_results` continues a LinkedIn people, post or company search. Repeating the same LinkedIn people filters continues automatically after the pages already fetched.

## Research before contacting

1. For the leads the user will contact first: `research_lead` with their result ids (or profile links for older leads), `email: true` only when they'll email. Companies: `research_company`.
2. If results are still in the cache: `get_results` and merge (research columns land in the rows). For older leads, write the returned columns with `update` (e.g. `"about=..." "recent_posts=..."`).
3. Summarise per lead: what they do now, what they post or comment about (the hook), the email and its quality.

## Offer for one lead

Use the `offer` skill: `tailor_offer` (channel + stage + lead), the offer card and the message, `check_offer`, save to the row (`draft_*`, `offer_angle`, `offer_first`, `offer_channel`) and `offers/<lead-key>.md`, then `record_offer`.

## Draft outreach from a template

1. Ask which template and language (list `templates/` with channel and purpose). Never choose for them.
2. Per lead, fill the template from the row (research, signal) and the offer, following `outreach.md`. Check limits.
3. Run `check_offer` on each draft and fix every error. Save with `python3 "$S" update <workbook> <key> "draft_first_message=<text>" data_source_note_sent=yes` (only `yes` if the draft has the note). Show the drafts; edit on request.
4. After the user says they sent it: `update <key> status=contacted channel=<channel>`.

If another connector writes messages, use it for the text and still save the drafts (and any templates it gives) here.

## Follow-ups

1. For each workbook in `leads/`: `python3 "$S" due <workbook> --days 1`.
2. Show them grouped by overdue / today / tomorrow, with the last message and notes.
3. Draft the follow-up with the `offer` skill at stage `follow_up` (`tailor_offer` shows what was already pitched, so the follow-up adds a new angle, proof point or first-touch offer; never "just bumping this") into `draft_follow_up`.
4. When sent: `update <key> status=contacted` (counts the follow-up and sets the next date). After 3 follow-ups without a reply, suggest `lost` or a long pause.

## Log outcomes

"She replied" → `status=replied` (+ notes). "Booked a call" → `status=meeting next_follow_up=<call date>`. "Signed" → `won`. "Not now" → `not_interested` or a later `next_follow_up`. "Remove me" → the forget workflow.

## Topics (on demand only)

1. `topics.md` lists topics with phrases per platform. Check only when asked ("check my topics", "anything new on bookkeeping?").
2. Run the searches for the chosen topic(s); people delivered before are hidden automatically.
3. Treat the results as an inbox: present, the user picks, merge the picked into the topic's campaign workbook. Update "Last checked".

## Import a spreadsheet

1. The user drops a CSV or XLSX in `imports/` (or points to one).
2. Ask: add to an existing campaign workbook, or create a new campaign? (Create the campaign file for a new one.)
3. `python3 "$S" import <workbook> <file>`; add `--sheet Reddit|Instagram|Companies` when the file is clearly one platform.
4. Report added, updated and skipped rows (rows without a profile link, handle or email are skipped). Imported rows don't count against the quota.
5. Offer research for imported leads that lack details.

## Export for a CRM

`python3 "$S" export <workbook> exports/<name>.csv [--sheet LinkedIn] [--status contacted,replied]`. In a plain chat without files, use `export_csv` for download links instead.

## Forget a person

1. `forget_person` with their profile link (removes them from the server and blocks them from future results).
2. `python3 "$S" remove <workbook> <profile link or key>` for every workbook in `leads/`, delete their offer card in `offers/`, and their mentions in notes.
3. Remind the user to remove them from their CRM and email tools, and to confirm to the person if they asked.
