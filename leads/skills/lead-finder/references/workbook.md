# The workbook

`leads/<campaign>.xlsx`. Always change it with the script; it merges on the `key` column and never overwrites the user's working columns.

```
S="${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py"
python3 "$S" create  leads/uk-dtc.xlsx
python3 "$S" merge   leads/uk-dtc.xlsx /tmp/rows.json --campaign uk-dtc
python3 "$S" update  leads/uk-dtc.xlsx linkedin:pub:jane-doe status=contacted channel=linkedin
python3 "$S" update  leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe "notes=Asked to talk after the 15th" next_follow_up=2026-10-15
python3 "$S" due     leads/uk-dtc.xlsx --days 1
python3 "$S" summary leads/uk-dtc.xlsx
python3 "$S" remove  leads/uk-dtc.xlsx https://www.linkedin.com/in/jane-doe
python3 "$S" import  leads/uk-dtc.xlsx imports/crm-export.csv [--sheet LinkedIn]
python3 "$S" export  leads/uk-dtc.xlsx exports/uk-dtc-contacted.csv --status contacted,replied
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
| status | new, to_contact, contacted, replied, meeting, won, lost, not_interested, do_not_contact |
| score, score_reason | fit 1-10 and why |
| next_follow_up | date the next nudge is due |
| contacted_on | first contact date |
| channel | linkedin_note, linkedin_message, inmail, email, reddit_reply, reddit_dm, instagram_dm |
| follow_ups | how many follow-ups were sent |
| last_reply_on | date of their last reply |
| notes | anything the user wants to remember |
| draft_first_message, draft_follow_up | the current drafts |
| data_source_note_sent | yes once the first message told them where their details came from |
| campaign | the campaign slug |
| offer_angle, offer_first, offer_channel | the angle, first-touch offer and channel of the last offer sent |
| offer_card | path of the offer card in `offers/` |

Source columns (filled by Lead Finder): LinkedIn: name, headline, role, company, company_url, location, profile_url, open_to_work, email, email_quality, signal, signal_text, signal_url, signal_date, source, search, found_on; research: about, experience, education, skills, followers, other_emails, recent_posts, recent_comments, recent_reactions. Companies: company, linkedin_url, industry, size, location, website, description, signal…; research: company_description, company_website, company_size, company_industry, company_hq, company_founded, company_specialities, company_funding, company_recent_posts. Reddit: username, profile_url, subreddit, type (post/comment), title, text, post_url, posted_at, upvotes, comments, signal…; research: recent_activity, karma, about. Instagram: username, full_name, profile_url, caption, hashtags, post_url, posted_at, likes, comments, signal…; research: bio, followers, website, business_category, business_account, posts_count, recent_posts.

Imported files keep unknown columns as `import_<name>`.

## Status updates (what `update` does for you)

- `status=contacted`: the first time sets `contacted_on` to today; later times count a follow-up. Either way `next_follow_up` becomes today + 4 days unless you pass one.
- `status=replied`: sets `last_reply_on`, clears `next_follow_up` (set a new one if they asked to talk later).
- won, lost, not_interested, do_not_contact: clear `next_follow_up`.
- Dates are `YYYY-MM-DD`.

## Generated sheets

- **Summary**: counts per sheet and status, follow-ups due, the data-source reminder.
- **Follow-ups**: every open lead with a follow-up date, overdue first.
- **Pipeline**: everyone past "new", grouped by status.
They're rebuilt on every script write. If the user edited a platform sheet by hand, run `rebuild`.
