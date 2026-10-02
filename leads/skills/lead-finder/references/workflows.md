# Workflows

`S` below is `${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py`.

## Set up (first run)

1. `my_account`: show plan, quota, status, token and the user's own profiles. If the account waits for approval or has no token, say so and continue with the file setup anyway. If their profiles are missing, ask for their LinkedIn link, Reddit username and Instagram handle and save them with `set_my_profiles` (used to see when leads engage back).
2. Create the folders `campaigns/`, `templates/`, `offers/`, `leads/`, `imports/`, `exports/`, and `README.md` (text in `folder.md`). Never overwrite existing files.
3. Copy the starter templates from this skill's `assets/templates/` into `templates/` (skip files that exist).
4. The offer: `get_offer`. If there's none, run the `offer-builder` skill. Write `offer.md` from `get_offer`'s markdown.
5. Propose 2-3 target segments with a one-line reason each. The user picks one: write `campaigns/<slug>.md`, then `python3 "$S" create leads/<slug>.xlsx`.
6. Explain the method in two lines: find people, engage with them in public until they engage back, offer only when they're interested. Suggest a first search (the warmest source) and say what it costs and how it counts against the quota.

## Find leads

1. `get_offer` (or `offer.md`) and the campaign file (ideal customer, where they talk, exclusions, learnings).
2. Pick the source (say why). People who post and comment are the ones you can engage with:
   - Someone talking about the problem now: `search_linkedin_posts`, `search_reddit` (phrases people would write, a subreddit when known), `search_instagram` (hashtags or keywords).
   - People commenting on a relevant post (a competitor's launch, an influencer's post on the problem): `search_post_engagers`.
   - Companies with a reason to buy: `search_hiring`, `search_ads`, `search_companies`; then `search_linkedin_people` with `company_urls` for the right roles there.
   - People by profile: `search_linkedin_people` (several title variants; LinkedIn location names; `exclude_company_urls`). Check they post before planning to engage.
3. Small first (10-25), then more once the user likes the fit. Mention the cost and the quota left.
4. If the result says `running`, tell the user and call `check_search` with the search_id after ~30-60 seconds.
5. A compact table, best first: score (1-10), who, role and company (or subreddit / handle), the signal, one-line reason. Say how many were hidden as already delivered.
6. Ask which to keep. `pick_leads` with the ids (or all: true); `exclude_leads` for the clear misfits.
7. `get_results`, add scores, merge into the campaign's workbook (see `workbook.md`), and set the kept ones to `to_engage`. Report added and updated counts.
8. Write what the user liked or rejected, and why, into the campaign's "Learnings".

`more_results` continues a LinkedIn people, post or company search.

## Engage (`/leads:engage`)

1. Who: the leads in `to_engage`, `engaging` or `warm` whose `next_touch` is today or earlier (`python3 "$S" due <workbook>`), or the ones the user names. A handful at a time (5-10 a day is plenty).
2. For each, find something to engage with: their latest posts from the row (`recent_posts`, `signal_text`), or fresh ones with `research_lead` (posts) or `check_lead_activity`.
3. Suggest a genuine comment per lead with `engagement.md` and the templates (`linkedin-comment`, `reddit-comment`, `instagram-comment`), the post's link and why it's worth commenting on. Run `check_message` (stage `engage`) and fix every error. Save it with `update <key> "draft_comment=<text>"`.
4. The user posts it themselves. When they say "done" (or "I commented on Olivia's post"), log it: `interact <workbook> <key> --by you --channel <platform> --kind comment --url <post link>`.
5. After 3-4 comments over a week or two, on LinkedIn suggest a connection request (`connection-request` template, or no note).

## Check who engaged back (`/leads:check`)

1. The leads in `engaging` (and `warm` leads with no conversation yet), up to 10 at a time.
2. `check_lead_activity` with their profile links, `since_days` (7 by default) and `engaged_posts`: the post links from their `interactions` log lines that start with `you:`.
3. For each lead with `engaged_back`: log it (`interact … --by them --kind reply|comment|reaction`), so they become `warm`. Tell the user what they did.
4. For leads with `new_posts`: suggest the next comment (the Engage workflow).
5. Ask the user about anything the check can't see: "Did anyone message you, accept a connection or reply to a DM?" Log what they say (`--kind message` makes the lead `talking`).
6. Leads with no response after 4-5 touches over three weeks: suggest pausing them (a later `next_touch`) or `lost`.

## When someone engages back or writes

"She replied to my comment" → `interact … --by them --kind reply`. "He messaged me asking about X" → `interact … --by them --kind message --note "asked about X"`. Then help the user answer (template `reply-to-message`, `check_message` stage `conversation`). Their goal and what's in the way go into `notes`: the offer will answer them.

## Offer for one lead (`/leads:offer`)

Only for leads in `warm`, `talking`, `offer_sent` or `meeting` who've shown interest. Use the `offer` skill: `tailor_offer`, the lead's offer in `offers/<lead-key>.md` (edited with the user), the message, `check_message`, then after sending `record_offer` and `update <key> status=offer_sent offer_price=<price> offer_file=offers/<file>`.

## Today (`/leads:today`)

1. For each workbook in `leads/`: `python3 "$S" due <workbook> --days 0`.
2. Group by what to do: answer (talking, warm), follow up an offer (offer_sent, at most two follow-ups), engage again (engaging, to_engage), calls (meeting).
3. For each: the next step and a draft (comment, reply or offer follow-up via the `offer` skill at stage `follow_up`).

## Log outcomes

"Booked a call" → `status=meeting next_touch=<call date>`. "Signed" → `won`. "Not now" → `not_interested` or a later `next_touch`. "Remove me" → the forget workflow.

## Topics (on demand only)

1. `topics.md` lists topics with phrases per platform. Check only when asked ("check my topics"), or in a routine.
2. Run the searches for the chosen topic(s); people delivered before are hidden automatically.
3. Treat the results as an inbox: present, the user picks, merge the picked into the topic's campaign workbook as `to_engage`. Update "Last checked".

## Import a spreadsheet

1. The user drops a CSV or XLSX in `imports/` (or points to one).
2. Ask: add to an existing campaign workbook, or create a new campaign?
3. `python3 "$S" import <workbook> <file>`; add `--sheet Reddit|Instagram|Companies` when the file is clearly one platform.
4. Report added, updated and skipped rows. Imported rows don't count against the quota.
5. Offer research for imported leads that lack details.

## Export for a CRM

`python3 "$S" export <workbook> exports/<name>.csv [--sheet LinkedIn] [--status talking,offer_sent]`. In a plain chat without files, use `export_csv` for download links instead.

## Forget a person

1. `forget_person` with their profile link (removes them from the server and blocks them from future results).
2. `python3 "$S" remove <workbook> <profile link or key>` for every workbook in `leads/`, delete their file in `offers/`, and their mentions in notes.
3. Remind the user to remove them from their CRM and email tools, and to confirm to the person if they asked.
