# The workbook

`leads/<campaign>.xlsx`. Always change it with the script; it merges on the `key` column and never overwrites the user's working columns.

```
S="${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py"
python3 "$S" create   leads/uk-dtc.xlsx
python3 "$S" merge    leads/uk-dtc.xlsx /tmp/rows.json --campaign uk-dtc
python3 "$S" interact leads/uk-dtc.xlsx linkedin:pub:jane-doe --by you --channel linkedin --kind comment --url https://www.linkedin.com/posts/…
python3 "$S" interact leads/uk-dtc.xlsx linkedin:pub:jane-doe --by them --channel linkedin --kind reply --note "Asked how we handle drop days"
python3 "$S" update   leads/uk-dtc.xlsx linkedin:pub:jane-doe status=offer_sent offer_price=4200 offer_file=offers/linkedin-pub-jane-doe.md
python3 "$S" update   leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe "notes=Call after the 15th" next_touch=2026-10-15
python3 "$S" due      leads/uk-dtc.xlsx --days 1
python3 "$S" summary  leads/uk-dtc.xlsx
python3 "$S" remove   leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe
python3 "$S" import   leads/uk-dtc.xlsx imports/crm-export.csv [--sheet LinkedIn]
python3 "$S" export   leads/uk-dtc.xlsx exports/uk-dtc-talking.csv --status talking,offer_sent
```

Every command prints JSON. Write rows for `merge` to a temporary JSON file first (outside the folder).

## Saving search results

1. `get_results` (state picked) returns `{ "sheets": { "LinkedIn": [ {row}, ... ], ... } }`.
2. Add your fit score to each row before merging: `"score": 8, "score_reason": "Head of Growth at a 40-person DTC brand, posted about agency search last week"`. Leave them out if you didn't score.
3. Save that JSON (the whole object is fine) and run `merge`. New rows get `status=new` and today's `found_on`; existing rows get fresh source and research columns; the user's columns are kept.
4. Tell the user what was added and updated, and that the rest of the search results will be deleted from the server at `stored_until`.

## Sheets and columns

Platform sheets (source of truth): **LinkedIn**, **Companies**, **Reddit**, **Instagram**. The first columns are who (name/company/username), then the working columns, then the source and research columns. `key` is hidden: `linkedin:pub:<slug>`, `linkedin:id:<ACoAA…>`, `linkedin:company:<slug>`, `reddit:u:<name>`, `instagram:u:<name>`, or `email:<address>` for imports without a profile.

Working columns (the user's; merges never overwrite them):

| Column | Meaning |
|---|---|
| status | new, to_engage, engaging, warm, talking, offer_sent, meeting, won, lost, not_interested, do_not_contact |
| score, score_reason | fit 1-10 and why |
| next_touch | the date of the next thing to do with them (engage again, answer, follow up) |
| engage_channel | where the user engages them: linkedin, reddit, instagram, email |
| touches | how many times the user has engaged them |
| engaged_on | the first time the user engaged |
| last_their_action, last_their_action_on | what they did last (reply, comment, reaction, message) and when |
| interactions | the log, one line per touch: `2026-10-02 you: linkedin comment <post link> · note` / `2026-10-03 them: linkedin reply` |
| notes | anything the user wants to remember |
| draft_comment, draft_message | the current drafts |
| offer_sent_on, offer_price, offer_file | when the offer went out, the price quoted, and its file in `offers/` |
| campaign | the campaign slug |

Source columns (filled by Lead Finder): LinkedIn: name, headline, role, company, company_url, location, profile_url, open_to_work, email, email_quality, signal, signal_text, signal_url, signal_date, source, search, found_on; research: about, experience, education, skills, followers, other_emails, recent_posts, recent_comments, recent_reactions. Companies: company, linkedin_url, industry, size, location, website, description, signal…; research: company_description, company_website, company_size, company_industry, company_hq, company_founded, company_specialities, company_funding, company_recent_posts. Reddit: username, profile_url, subreddit, type (post/comment), title, text, post_url, posted_at, upvotes, comments, signal…; research: recent_activity, karma, about. Instagram: username, full_name, profile_url, caption, hashtags, post_url, posted_at, likes, comments, signal…; research: bio, followers, website, business_category, business_account, posts_count, recent_posts.

Imported files keep unknown columns as `import_<name>`.

## What `interact` and `update` do for you

- `interact --by you`: logs the touch, counts it, sets `engage_channel` and `engaged_on` (first time), moves `new`/`to_engage` to `engaging`, next touch in 3 days.
- `interact --by them`: logs it, sets `last_their_action`; `engaging` becomes `warm`, or `talking` when they messaged, emailed or asked (`--kind message|dm|email|asked|call`); next touch tomorrow.
- `status=offer_sent`: sets `offer_sent_on`, next touch in 4 days.
- won, lost, not_interested, do_not_contact: clear `next_touch`.
- Dates are `YYYY-MM-DD`. Old statuses (to_contact, contacted, replied) are read as to_engage, engaging and talking.

## Generated sheets

- **Summary**: counts per sheet and status, next touches due.
- **Next touches**: every open lead with a next-touch date, overdue first.
- **Pipeline**: everyone past "new", grouped by status.
They're rebuilt on every script write. If the user edited a platform sheet by hand, run `rebuild`.
