# The workbook

`leads/<campaign>.xlsx`. Always change it with the script; it merges on the `key` column and never overwrites the user's working columns.

```
S="${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py"
python3 "$S" create   leads/uk-dtc.xlsx
python3 "$S" merge    leads/uk-dtc.xlsx /tmp/rows.json --campaign uk-dtc --status to_engage
python3 "$S" review add    leads/uk-dtc.xlsx /tmp/result.json --source find-linkedin
python3 "$S" review list   leads/uk-dtc.xlsx [--platform linkedin|companies|reddit|instagram] [--decision keep|skip|undecided] [--all]
python3 "$S" review remove leads/uk-dtc.xlsx 101 102 | --expired | --decided | --all
python3 "$S" sources log    leads/uk-dtc.xlsx /tmp/stats.json [--by find-reddit] [--campaign uk-dtc]
python3 "$S" sources report leads/uk-dtc.xlsx [--days 7] [--platform linkedin|reddit|instagram]
python3 "$S" problems report leads/uk-dtc.xlsx [--days 30]
python3 "$S" interact leads/uk-dtc.xlsx linkedin:pub:jane-doe --by you --channel linkedin --kind comment --url https://www.linkedin.com/posts/…
python3 "$S" interact leads/uk-dtc.xlsx linkedin:pub:jane-doe --by them --channel linkedin --kind reply --note "Asked how we handle drop days"
python3 "$S" update   leads/uk-dtc.xlsx linkedin:pub:jane-doe status=offered offer_price=4200 offer_file=offers/linkedin-pub-jane-doe.md
python3 "$S" update   leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe "notes=Call after the 15th" next_touch=2026-10-15
python3 "$S" due      leads/uk-dtc.xlsx --days 1
python3 "$S" summary  leads/uk-dtc.xlsx
python3 "$S" remove   leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe
python3 "$S" import   leads/uk-dtc.xlsx imports/crm-export.csv [--sheet LinkedIn]
python3 "$S" export   leads/uk-dtc.xlsx exports/uk-dtc-talking.csv --status talking,meeting,offered
```

Every command prints JSON. Write rows for `merge` and `review add` to a temporary JSON file first (outside the folder).

Every command that writes takes a lock file next to the workbook (`leads/.uk-dtc.xlsx.lock`), so two tasks never write the same workbook at once. A second one waits up to a minute; if the first is still writing, it prints `{"error": "Another Lead Finder task is writing ..."}` and exits with code 4: wait a minute and run it again. A lock older than 10 minutes was left by a crashed task and is cleared on its own. `due`, `summary`, `export`, `review list`, `sources report` and `problems report` only read and never wait.

## Saving search results

The rows come from the review flow (Review and approve in `workflows.md`): only leads the user kept and you picked are saved here.

1. `get_results` (state picked) returns `{ "sheets": { "LinkedIn": [ {row}, ... ], ... } }`.
2. Add your fit score to each row before merging: `"score": 8, "score_reason": "Head of Growth at a 40-person DTC brand, posted about agency search last week"`. Rows that waited in To review get their score and reason from there when you leave them out (matched on `id`).
3. Save that JSON (the whole object is fine) and run `merge --status to_engage`. New rows get that status (`new` without `--status`) and today's `found_on`; existing rows get fresh source and research columns; the user's columns are kept.
4. Tell the user what was added and updated, and that the rest of the search results will be deleted from the server at `stored_until`.

## The To review sheet

Every find lands here first, as a preview: a score, the reason, who it is and what they wrote, but no link or handle. `review add` takes a search result as the tool returned it (`search_id`, `stored_until`, `platform`, `results` with `id` and the preview fields) or rows already shaped to the sheet's columns; it skips ids already there and drops rows whose `expires_at` has passed. The user sets `decision` to `keep` or `skip` in Excel, or says it in the chat. `review list` prints the rows waiting (`--decision keep` for the ones to approve; expired rows are counted and left out unless `--all`). `review remove` clears rows by id, `--decided`, `--expired` or `--all`. Every write of the workbook drops expired rows. To review is never exported.

- Columns: `id` (the server's result id, the one `pick_leads` takes), `search_id`, `platform`, `decision` (empty, keep or skip), `score`, `score_reason` (the fit score and why; a reason for 5 or less starts with `wrong fit:`, `not enough to judge:` or `rules out:`), `who` (the name, the post's title, the account's full name or the company), `about` (the headline, the post's text or the bio, at most 300 characters), `where` (company and location, the subreddit, or followers), `posted_at`, `signal`, `expires_at`, `found_on`, `campaign`, `source` (the command or playbook that added it).
- To add your scores, put `score` and `score_reason` on each result in the JSON before `review add` (the result object as the tool returned it, with the two fields added to each item, is fine). A file with several search results (a list of them) works too.
- `review add` prints `added`, `already_there`, `expired_removed` and `waiting`, and `unlabelled` when a row scored 5 or less has a reason without one of those labels (label the reasons before adding), `sources_logged` when it logged runs in the Sources sheet and `problems_logged` when it logged fitting Reddit posts in the Problems sheet. `review list` prints `rows`, `waiting`, `expired`, the count per decision and `earliest_expires`.
- A row never holds a URL, handle, username, email or key; links and email addresses in a text are replaced. The server refuses a row's id for research or offers until it's picked.
- `summary` reports `to_review` (waiting and expired) and the Summary sheet has a To review line.

## The Sources sheet

How each source did: one row per run and per source, so the user sees which subreddits, bio words and LinkedIn searches give good leads and where to move quota. It holds counts only (no person, handle or link) and is never exported, imported, counted in the platform totals or touched by `remove`.

- Columns: `date`, `platform` (linkedin, reddit or instagram; a company search counts under linkedin), `key` (the source: `r/<subreddit>`, `bio: <word>`, or the search's label without its ` (page N)`, so the pages of one search add up), `results` (shown in that run), `good` (scored 6 or more), `search_id`, `by` (the command or playbook), `campaign`.
- `review add` logs the run on its own when it's given a search result (`search_id` and `results`): results per subreddit from `shown_by_subreddit`, per bio word from `shown_by_word` (an account that matched two words counts under both), otherwise the result's `shown`; good from your scores on the rows. So keep those counts in the JSON as the tool returned them, put your scores on the rows, and run it even when nothing fits (an empty `results` list). The same result added twice is counted once. It prints `sources_logged` when it logged something. Rows already shaped to the To review columns log nothing.
- `sources log <workbook> <stats.json>` records a run by hand: a search result as above, or rows `{"platform": "reddit", "key": "r/dropdayshops", "results": 15, "good": 2}` (optional `search_id` and `date`). It prints `logged`, `already_there` and `total`.
- `sources report <workbook> [--days 7] [--platform P]` sums the last 7 days (today included) per source: `runs`, `results`, `good`, `kept` (leads found in that window and kept in the platform sheets, imports left out), `last_run` and the `verdict`, worst last; then `platforms` (results, good, kept and the keys to stop per platform), `stop` and the `rule`.
- The stop rule: a source with 10 or more results and fewer than 3 good leads in 7 days is `stop`; fewer than 10 results is `too few to judge` (a quiet subreddit or a rare bio word is not a bad one); the rest `ok`. What to do with a `stop` source is in Find leads, step 1b, of `workflows.md`: a subreddit is paused or removed, a bio word moves to Paused bio words, a LinkedIn search goes under Searches that didn't work. Only on the user's yes; a playbook only reports it.
- Runs older than 180 days are dropped on every write. `summary` reports `sources` (how many were run in the last 7 days, how many are `stop`).

## The Problems sheet

What came up in the Reddit posts Claude read: one row per post scored 6 or more, kept or not, written by `review add` when it adds the post to To review. It is what `/leads:problems` and the weekly report count. It holds no username, title, link, handle or email, and is never exported, imported, counted in the platform totals or touched by `remove`.

- Columns: `date` (the day it was added), `subreddit` (`r/<name>` lowercased; a post in a user's own profile counts as `r/[user profile]`), `score`, `problem` and `ask` (read from the reason `<the problem, in short>; asks for <the ask>`: the problem is the text before the first `;`, the ask what follows `asks for`, empty when there is no `asks for`), `phrase`, `search_id`, `id`, `campaign`, `source` (the command or playbook).
- `phrase`: put it on each fitting Reddit item next to `score` and `score_reason` before `review add`: the poster's own words for the problem, at most 12 words, no names. A post without one is logged without a phrase. It is not a To review column.
- Links, email addresses and handles in the problem, the ask, the phrase, the campaign and the source are replaced (`[link]`, `[email]`, `[handle]`); the phrase is cut at 100 characters. A post whose reason has no `;` or names no problem, a row added with `--source signals` (its reason quotes the post), a LinkedIn or Instagram find, and a post scored 5 or less log nothing. The same post (`search_id` and `id`) is logged once.
- `problems report <workbook> [--days 30]` reads the last 30 days (today included) and counts the posts per wording of the problem (lowercase, spaces and a trailing `.`, `!` or `,` ignored): `days`, `since`, `posts` (the rows in the window), `problems` (per wording: `problem` as first written, `count`, `asks` and `subreddits` with their counts, up to five distinct `phrases`, `last_seen`; most posts first, then the most recent), the window's `asks` and `subreddits`, and a `note`. It judges nothing: group the wordings that mean the same yourself (`/leads:problems` in `workflows.md`).
- Rows older than 180 days are dropped on every write. `summary` reports `problems` (the posts logged in the last 30 days).

## Sheets and columns

Platform sheets (source of truth): **LinkedIn**, **Companies**, **Reddit**, **Instagram**. **To review** (above) holds finds waiting for a decision, **Sources** (above) the counts per source and **Problems** (above) what came up in the fitting Reddit posts; none is a platform sheet. The first columns are who (name/company/username), then the working columns, then the source and research columns. `key` is hidden: `linkedin:pub:<slug>`, `linkedin:id:<ACoAA…>`, `linkedin:company:<slug>`, `reddit:u:<name>`, `instagram:u:<name>`, or `email:<address>` for imports without a profile.

Working columns (the user's; merges never overwrite them):

| Column | Meaning |
|---|---|
| status | new, to_engage, engaging, warm, talking, meeting, offered, won, lost, not_interested, do_not_contact |
| score, score_reason | fit 1-10 and why; 6 or more fits, a lower reason starts with `wrong fit:`, `not enough to judge:` or `rules out:` |
| next_touch | the date of the next thing to do with them (engage again, answer, follow up) |
| engage_channel | where the user engages them: linkedin, reddit, instagram, email |
| touches | how many times the user has engaged them |
| engaged_on | the first time the user engaged |
| last_their_action, last_their_action_on | what they did last (reply, comment, reaction, message) and when |
| interactions | the log, one line per touch: `2026-10-02 you: linkedin comment <post link> · note` / `2026-10-03 them: linkedin reply` |
| notes | anything the user wants to remember |
| draft_comment, draft_message | the current drafts |
| offered_on, offer_price, offer_file | when the offer was made on a call, the price offered, and its file in `offers/` |
| campaign | the campaign slug |

Source columns (filled by Lead Finder): LinkedIn: name, headline, role, company, company_url, location, profile_url, open_to_work, email, email_quality, signal, signal_text, signal_url, signal_date, source, search, found_on; research: about, experience, education, skills, followers, other_emails, recent_posts, recent_comments, recent_reactions. Companies: company, linkedin_url, industry, size, location, website, description, signal…; research: company_description, company_website, company_size, company_industry, company_hq, company_founded, company_specialities, company_funding, company_recent_posts. Reddit: username, profile_url, subreddit, type (post/comment), title, text, post_url, posted_at, upvotes, comments, signal…; research: recent_activity, karma, about. Instagram: username, full_name, profile_url, caption, hashtags, post_url, posted_at, likes, comments, signal…; research: bio, followers, website, business_category, business_account, posts_count, recent_posts.

Imported files keep unknown columns as `import_<name>`.

## What `interact` and `update` do for you

- `interact --by you`: logs the touch, counts it, sets `engage_channel` and `engaged_on` (first time), moves `new`/`to_engage` to `engaging`, next touch in 3 days.
- `interact --by them`: logs it, sets `last_their_action`; `engaging` becomes `warm`, or `talking` when they messaged, emailed or asked (`--kind message|dm|email|asked|call`); next touch tomorrow.
- `status=meeting`: pass the call date as `next_touch=YYYY-MM-DD`.
- `status=offered`: sets `offered_on`, next touch in 4 days. `offer_sent` from older files becomes `offered`.
- won, lost, not_interested, do_not_contact: clear `next_touch`.
- Dates are `YYYY-MM-DD`. Old statuses (to_contact, contacted, replied) are read as to_engage, engaging and talking.

## Generated sheets

- **Summary**: counts per sheet and status, next touches due, the To review line, and the sources of the last 7 days with the stop rule.
- **Next touches**: every open lead with a next-touch date, overdue first.
- **Pipeline**: everyone past "new", grouped by status.
They're rebuilt on every script write. If the user edited a platform sheet by hand, run `rebuild`.
