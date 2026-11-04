# Workflows

`S` below is `${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py`.

## Set up (first run)

1. `my_account`: show plan, quota, status, token and the user's own profiles. If the account waits for approval or has no token, say so and continue with the file setup anyway. If their profiles are missing, ask for their LinkedIn link, Reddit username and Instagram handle and save them with `set_my_profiles` (used to see when leads engage back).
2. Create the folders `campaigns/`, `templates/`, `offers/`, `leads/`, `imports/`, `exports/`, and `README.md` (text in `folder.md`). Never overwrite existing files.
3. Copy the starter templates from this skill's `assets/templates/` into `templates/` (skip files that exist).
4. The offer: `get_offer`. If there's none, run the `offer-builder` skill. Write `offer.md` from `get_offer`'s markdown.
5. Propose 2-3 target segments with a one-line reason each. The user picks one.
6. Platforms: ask which of the three to search for this campaign, with each one's role in a line: LinkedIn finds people directly by role and company; Reddit finds posts where someone describes a problem you solve, so you can answer in the thread, and teaches you how they talk; Instagram finds accounts whose bio matches your ideal client. Then, for each chosen platform, only its own questions, each with a proposal from the offer and the segment that the user edits:
   - LinkedIn: job titles (several variants), industries, company size, locations.
   - Reddit: the problems the ideal client has, written the way they would say them (propose many short phrases and ask for more: the more, the better Claude can judge posts; never job titles or labels, nobody writes 'Head of Ecommerce' in a post); what they are looking for when they post about it; then the subreddit check: propose 5 to 8 short topics from the problems and the segment (a trade, a product, a platform; never a sentence), `find_subreddits` with them, show the active ones with their figures and say how many were left out as quiet, shortlist at most 15 (plus any the user knows), `check_subreddits` for their rules, and show one table: members, weekly visitors, weekly contributions, newest post, and the rules on promotion and DMs quoted as written ('not mentioned' when no rule names them). The user approves; only approved subreddits go into the file, as the Subreddits block in `folder.md`, with today's date and the topics. No Reddit search for this campaign before that.
   - Instagram: the words the ideal client would put in their bio; what a good bio shows, in one or two lines.
7. Disqualifiers: what rules a lead out even when the rest fits (for example practitioners who get clients through insurance). Propose two or three from the offer; the user adds, removes or confirms. They're applied in every score. A disqualifier is about fit only (role, company, business model, need), never age, gender, nationality, ethnicity, religion, health, family status or photos; if the user asks for one, say so and leave it out.
8. Write `campaigns/<slug>.md` in the format of `folder.md` (Ideal customer, the chosen platforms with their details, the disqualifiers), then `python3 "$S" create leads/<slug>.xlsx`.
9. Explain the method in two lines: find people, engage with them in public until they engage back, offer only when they're interested. Suggest a first search on one of the chosen platforms and say what it costs and that only the people they keep count toward the quota.

## Update a campaign (`/leads:update`)

1. The campaign (ask which when there are several). Read it and show, compactly: the platforms, each one's details, the disqualifiers. A file without a Platforms section: say that it's searched on all three today and ask the platforms and their questions as in Set up.
2. Ask what to change: add or remove a platform, change a platform's details, add or remove disqualifiers (same rule as Set up, step 7: fit only). Adding a platform asks only that platform's questions (Set up, step 6). Removing one stops searches there; its leads stay in the workbook with their statuses.
   2b. Subreddits (Reddit campaigns): when the Subreddits block is older than 30 days, or the user asks, re-check: `check_subreddits` with the approved ones (which went quiet, whose rules changed), `find_subreddits` with the block's topics for new ones, one table as in Set up, step 6; the user approves, removes or pauses; rewrite the block with today's date. An older one-line Subreddits entry is checked the same way and becomes the block. A pause from the stop rule is lifted or confirmed like any other.
   2c. Paused bio words (Instagram campaigns): when the user asks, move a word back to Bio words or drop it; the Sources sheet (`sources report --days 28`) shows how it did.
3. Rewrite only the `## Platforms` and `## Disqualifiers` sections; Ideal customer, Searches that work, Searches that didn't work, Exclude and Learnings stay as they are. Show the changed sections.
4. When a platform is now searched by no campaign, offer `set_quota_split` with 0 for it (nothing is kept there by mistake); when one comes back, offer `null` to lift the limit. Only on a yes.
5. No lead search runs here. Suggest `/leads:find` to try the new details.

## Find leads (`/leads:find`)

`/leads:find linkedin`, `/leads:find reddit` or `/leads:find instagram` runs that platform's section below. `/leads:find` alone runs Review and approve first (what's already waiting), then each platform the campaign lists, in the campaign file's order; a campaign without a Platforms section runs all three, with Ideal customer as the LinkedIn details. Results are previews: no links or handles until the user keeps someone. Every find is written to the workbook's To review sheet before you ask about it, so a session that ends without an answer loses nothing.

The steps are the same on every platform:

1. `get_offer` (or `offer.md`) and the campaign file: ideal customer, the platforms and each one's details, the disqualifiers, exclusions, learnings.
1b. How the sources did: `python3 "$S" sources report <workbook>` for this platform. Say per source (subreddit, bio word or search) the results, good leads and kept of the last 7 days. A source marked `stop` (10 or more results, fewer than 3 good leads): on Reddit ask whether to remove the subreddit from the Subreddits block or pause it (`(paused YYYY-MM-DD: N good leads from M posts in 7 days)`) until the monthly re-check; on Instagram ask to move the word to `Paused bio words` with the same note and move it only on the user's yes; on LinkedIn ask whether to add the search with its counts to `## Searches that didn't work` and write it only on the user's yes, then change the titles, locations or method instead of repeating it. Search with what is left: never a paused subreddit or bio word, never a search listed under didn't work. When one platform's kept reached its weekly limit this week while another gave fewer good leads than its room, suggest one `set_quota_split` change with both figures; only on a yes.
2. The platform's own method (its section below), following each platform's role:
   - LinkedIn: people by role and company with `search_linkedin_people` from the titles, industries, sizes and locations in the file; posts and engagers when someone talks about the problem now.
   - Reddit: `scan_subreddits` on the approved subreddits (the Subreddits block; never an unapproved one), the posts of the last 24 hours, no keywords (never titles or labels); read them and keep the posts where someone describes a problem the user solves, judged against 'Problems, in their words' and 'Looking for, when they post'. The post is the lead: to answer helpfully in the thread. `search_reddit` with a phrase only when the user asks for one. Add the phrases from good posts to the campaign's Reddit section.
   - Instagram: `search_instagram_bios` with the bio words of the campaign's Instagram section (at most 10 per call). The server shows only accounts whose bio contains one of the words and says which (`matched_words`); check each bio against 'A good bio shows' before it scores above 5. `search_instagram` in `hashtags` mode when the file lists hashtags.

   People who post and comment are the ones you can engage with:
   - Someone talking about the problem now: `search_linkedin_posts`, `search_reddit` (a phrase people would write, when the user asks for one; a campaign's daily method is the scan; only the last 48 hours), `search_instagram` (hashtags or keywords; only posts from the last 72 hours).
   - People commenting on a relevant post (a competitor's launch, an influencer's post on the problem): `search_post_engagers`.
   - Companies with a reason to buy: `search_hiring`, `search_ads`, `search_companies`; then `search_linkedin_people` with `company_urls` for the right roles there.
   - People by profile: `search_linkedin_people` (several title variants; LinkedIn location names; `exclude_company_urls`). Check they post before planning to engage.
3. 15 at a time (`max_results: 15`), more once the user likes the fit. Mention the cost and how many can still be kept this week (`quota.left`, and per platform when `quota.platforms` is there).
4. If the result says `running`, tell the user and call `check_search` with the search_id after about 30-60 seconds.
5. A compact table, best first: score (1-10), who (the name, or on Reddit the post's title), role and company (or the subreddit), the signal, one-line reason. Results are previews: no links or handles yet. Score from what is shown. Score per `references/scoring.md`: 6 or more fits; a reason for 5 or less starts with `wrong fit:` or `not enough to judge:`. Apply the campaign's Disqualifiers first: a lead that matches one scores 1 or 2 and the reason names the rule (for example 'rules out: insurance clients'); never drop them silently, and suggest skip for them (`exclude_leads` at approval). Say how many were hidden as kept before.
6. Before you ask: save the result with your score and reason on each item to a temporary JSON file and run `python3 "$S" review add <workbook> <result.json> --source find-<platform>` (see `workbook.md`). The finds now wait in To review; the user can also decide later in Excel. Run it even when nothing fits (the result with an empty `results` list and its counts): `review add` records the run's results and good leads per source in the Sources sheet.
7. Ask which to keep, then Review and approve (below): `pick_leads` counts and unlocks the kept ones, `exclude_leads` hides the skipped ones, and the kept ones are merged into the platform's sheet as `to_engage`. Report added and updated counts.
8. Write what the user liked or rejected, and why, into the campaign's "Learnings".
9. Research (`research_lead`) is optional, after the pick, for kept leads the user wants to engage, and costs Apify credit.

The user can cap one platform's share of the weekly quota (for example "keep LinkedIn to 100 a week"): `set_quota_split` with that platform's limit (`null` removes it), or the account page. Platforms without a limit share what's left of the total.

Reddit searches never look further back than 48 hours and Instagram post searches never further than 72 hours. `max_age_hours` can only narrow that window (for example 24 for a keyword search of the last day). When many results were left out as too old, suggest other keywords on Reddit (after a daily scan, the same scan tomorrow), or a subreddit re-check with /leads:update, and other hashtags or keywords on Instagram.

`more_results` continues a LinkedIn people, post or company search.

## Find leads on LinkedIn (`/leads:find-linkedin`)

1. The offer and the campaign's LinkedIn section: job titles, industries, company size, locations; the disqualifiers, the Exclude list and the learnings. A campaign without a Platforms section: Ideal customer stands in.
1b. How the searches did: `python3 "$S" sources report <workbook> --platform linkedin`. Say per search the results, good leads and kept of the last 7 days. A search marked `stop` (10 or more results, fewer than 3 good leads): ask whether to add it with its counts to `## Searches that didn't work`, write it only on the user's yes, and change the titles, locations or method instead of repeating it. Never run a search listed under didn't work as it is. When LinkedIn's kept reached its weekly limit this week while another platform gave fewer good leads than its room, suggest one `set_quota_split` change with both figures; only on a yes.
2. People by role and company: `search_linkedin_people` with several title variants, the industries and sizes, LinkedIn location names, and `exclude_company_urls` for the Exclude list. Posts and commenters are the warm signals when they fit: `search_linkedin_posts` for people posting about the problem now, `search_post_engagers` for people commenting on a relevant post (a competitor's launch, an influencer's post on the problem). Companies with a reason to buy: `search_hiring`, `search_ads` or `search_companies`, then `search_linkedin_people` with `company_urls` for the right roles there. Check people post before planning to engage. `more_results` continues a search.
3. 15 at a time (`max_results: 15`), more once the user likes the fit. Mention the cost and how many can still be kept this week (`quota.left`, and per platform when `quota.platforms` is there).
4. If the result says `running`, `check_search` with the search_id after about 30-60 seconds.
5. The scored table of Find leads, step 5, with the disqualifiers applied first; the person is scored (role, company, need, signal), per `references/scoring.md`.
6. `python3 "$S" review add <workbook> <result.json> --source find-linkedin` before you ask. Run it even when nothing fits, so the Sources sheet records the search's results and good leads.
7. Review and approve: `pick_leads` for the kept rows, `exclude_leads` for the skipped ones, then merge the kept into the LinkedIn sheet (Companies for companies) as `to_engage`.
8. What the user liked or rejected, and why, into "Learnings"; searches that found good people into "Searches that work".
9. Research (`research_lead`) is optional, after the pick, and costs Apify credit.

## Find leads on Reddit (`/leads:find-reddit`)

1. The offer and the campaign's Reddit section: 'Problems, in their words', 'Looking for, when they post', the approved subreddits and the block's checked date; the disqualifiers, the Exclude list and the learnings.
1b. How the subreddits did: `python3 "$S" sources report <workbook> --platform reddit`. Say per subreddit the posts shown, good leads and kept of the last 7 days. A subreddit marked `stop` (10 or more posts, fewer than 3 good leads): ask whether to remove it from the Subreddits block or pause it (`(paused YYYY-MM-DD: N good leads from M posts in 7 days)`) until the monthly re-check, and change the block only on the user's answer. Scan what is left: never a paused subreddit. When Reddit's kept reached its weekly limit this week while another platform gave fewer good leads than its room, suggest one `set_quota_split` change with both figures; only on a yes.
2. The daily scan: `scan_subreddits` with the approved, unpaused entries of the Subreddits block (at most 10 per call; a second call for the rest), the posts of the last 24 hours, no keywords. No approved subreddits yet (no block, or an older one-line entry): run the subreddit check of Set up, step 6, and ask for approval before anything runs; when the block is older than 30 days, say so and suggest `/leads:update`, then scan. Read every post, title and text (`get_results` with `state: new` and the search id gives the full text), and keep only the posts where someone describes a problem the user solves: 'Problems, in their words' and 'Looking for, when they post' are the yardstick for judging, never search terms (never titles or labels). Comments aren't read. `search_reddit` with a phrase only when the user asks for one (posts and comments from the last 48 hours).
3. The cost, about $0.02 per run plus $0.002 per post (15 posts per subreddit by default), and how many can still be kept this week (`quota.left`, and per platform when `quota.platforms` is there).
4. If the result says `running`, `check_search` with the search_id after about 30-60 seconds.
5. The scored table of Find leads, step 5, of the fitting posts only (6 or more): who is the post's title, where is the subreddit, and the score is about the post, not the poster: how closely it matches 'Problems, in their words' and what the poster asks for ('Looking for, when they post'); the reason names the ask (`references/scoring.md`). Say per subreddit how many posts were read, how many fit, and of the rest how many were wrong fit and how many not enough to judge; read the full text (`get_results`) before calling a post not enough to judge. The disqualifiers are applied first.
6. `python3 "$S" review add <workbook> <fitting.json> --source find-reddit` with the fitting posts only in `results`, each with `phrase` (the poster's own words for the problem, at most 12 words, no names; the Problems sheet keeps it) and its reason in the form `<the problem, in short>; asks for <the ask>` (the reason names no person, business or post title; a reason without the `;` is not logged), and the result's `shown_by_subreddit` kept as returned, before you ask; run it even when no post fits, so the Sources sheet records the day's counts per subreddit. Never `pick_leads` with `all: true` after a scan: it would keep every post read.
7. Review and approve: `pick_leads` for the kept rows, `exclude_leads` for the skipped ones, then merge the kept into the Reddit sheet as `to_engage`. Then engage: a helpful answer in their thread is the best first touch.
8. Add the phrases from good posts to the campaign's Reddit section ('Problems, in their words'), and what the user liked or rejected to "Learnings".
9. Research (`research_lead`) is optional, after the pick, and costs Apify credit.

## Find leads on Instagram (`/leads:find-instagram`)

1. The offer and the campaign's Instagram section: the bio words and 'A good bio shows'; the disqualifiers, the Exclude list and the learnings.
1b. How the bio words did: `python3 "$S" sources report <workbook> --platform instagram`. Say per bio word the accounts shown, good leads and kept of the last 7 days. A word marked `stop` (10 or more accounts, fewer than 3 good leads): move it to `Paused bio words` with the note (`(paused YYYY-MM-DD: N good leads from M accounts in 7 days)`), on the user's yes. Search with what is left: never a paused bio word. When Instagram's kept reached its weekly limit this week while another platform gave fewer good leads than its room, suggest one `set_quota_split` change with both figures; only on a yes.
2. Accounts whose bio matches the ideal client: `search_instagram_bios` with the bio words (at most 10 per call; a second call for the rest). The server keeps only accounts whose bio contains one of the words and tells which words matched; check each remaining bio against 'A good bio shows' before it scores above 5. `search_instagram` in `hashtags` mode when the section lists hashtags (posts from the last 72 hours only; when many were left out as too old, try other hashtags or keywords).
3. 15 at a time (`max_results: 15`), more once the user likes the fit. Mention the cost (about $0.005 per page of web results plus $0.003 per profile read) and how many can still be kept this week (`quota.left`, and per platform when `quota.platforms` is there).
4. If the result says `running`, `check_search` with the search_id after about 30-60 seconds.
5. The scored table of Find leads, step 5: who is the account's full name, about is the bio, where is the followers, the signal is the bio words that matched. Say per bio word how many accounts were shown (`shown_by_word`). The disqualifiers are applied first; a reason for 5 or less starts with `wrong fit:` (the word matched but the bio shows someone else) or `not enough to judge:` (a bio too short to tell), per `references/scoring.md`.
6. `python3 "$S" review add <workbook> <result.json> --source find-instagram` before you ask, with the result's `shown_by_word` kept as returned. Run it even when nothing fits, so the Sources sheet records the run's counts per bio word.
7. Review and approve: `pick_leads` for the kept rows, `exclude_leads` for the skipped ones, then merge the kept into the Instagram sheet as `to_engage`.
8. What the user liked or rejected, and why, into "Learnings"; bio words that found good accounts, and plural or spelling variants that would have matched, into the Instagram section.
9. Research (`research_lead`) is optional, after the pick, and costs Apify credit.

## Review and approve

What waits in a workbook's To review sheet becomes leads here: right after a search, when the user says "approve my review list", at the start of `/leads:find` and `/leads:today`, or after they marked rows in Excel.

1. `python3 "$S" review list <workbook>`: the rows waiting, with the user's decisions. In a chat, show the undecided ones compactly (score, who, about, where) and ask which to keep; `keep` rows from Excel need no question.
2. `pick_leads` with the ids of the kept rows (it counts them and unlocks their links); `exclude_leads` with the ids of the skipped rows. If some stayed previews (`over_quota`), say the week's quota or a platform limit is used up and when it frees up; they stay in To review until they expire. People not kept cost nothing and may come back in later searches.
3. `get_results` (picked rows are full; pass the rows' `search_id`s), add each row's score and reason from the review list, `python3 "$S" merge <workbook> rows.json --campaign <slug> --status to_engage`.
4. `python3 "$S" review remove <workbook> --decided --expired`; say how many were added, skipped, and how many expired (they may come back in a later search). When some kept rows stayed previews, remove the others by id instead (`review remove <workbook> <id> ...`), so those keep waiting.
5. Never look up, research or draft for a row still in To review: it's a preview, and the server refuses its id until it's picked.

## Engage (`/leads:engage`)

1. Who: the leads in `to_engage`, `engaging` or `warm` whose `next_touch` is today or earlier (`python3 "$S" due <workbook>`), or the ones the user names. A handful at a time (5-10 a day is plenty).
2. For each, find something to engage with: their latest posts from the row (`recent_posts`, `signal_text`), or fresh ones with `research_lead` (posts) or `check_lead_activity`.
3. Suggest a genuine comment per lead with `engagement.md` and the templates (`linkedin-comment`, `reddit-comment`, `instagram-comment`), the post's link and why it's worth commenting on. First write down, for yourself, what the post asks for (on Reddit it's in the row's `score_reason`; elsewhere the post's point or question); the comment answers that in its first sentence, then adds the user's experience or one thing to watch, then a question if any. Run `check_message` (stage `engage`) and fix every error and every warning on a comment. Save it with `update <key> "draft_comment=<text>"`.
4. The user posts it themselves. When they say "done" (or "I commented on Olivia's post"), log it: `interact <workbook> <key> --by you --channel <platform> --kind comment --url <post link>`. On LinkedIn, ask for the link to their own comment (Copy link to comment) and log that instead of the post link when they have it: it lets the check see replies to that comment.
5. After 3-4 comments over a week or two, on LinkedIn suggest a connection request (`connection-request` template, or no note).

## Check who engaged back (`/leads:check`)

1. The leads in `engaging` (and `warm` leads with no conversation yet), up to 10 at a time.
2. `check_lead_activity` with their profile links, `since_days` (7 by default) and `engaged_posts`: the post links from their `interactions` log lines that start with `you:`, and the links to the user's own comments when they were logged (LinkedIn: Copy link to comment).
3. For each lead with `engaged_back`: log it (`interact … --by them --kind reply|comment|reaction`, the kind matching what the result says), so they become `warm`. Tell the user what they did and where.
4. For leads with `new_posts`: suggest the next comment (the Engage workflow).
5. Ask the user about anything the check can't see: "Did anyone message you, accept a connection, reply to a DM or like your Instagram post?" Log what they say (`--kind message` makes the lead `talking`).
6. Leads with no response after 4-5 touches over three weeks: suggest pausing them (a later `next_touch`) or `lost`.

## When someone engages back or writes

"She replied to my comment" → `interact … --by them --kind reply`. "He messaged me asking about X" → `interact … --by them --kind message --note "asked about X"`. Then help the user answer (template `reply-to-message`, `check_message` stage `conversation`). Their goal and what's in the way go into `notes`: the offer will answer them. When they're interested (they ask about the work, the cost, availability): suggest a 30-minute call (template `suggest-a-call`), without the price in writing. Booked: `update <key> status=meeting next_touch=<call date>`.

## Offer for one lead (`/leads:offer`)

Only for leads in `talking`, `meeting` or `offered` who've shown interest. The offer is presented on a 1:1 call, never in a message. Use the `offer` skill:
1. Before the call: `tailor_offer` (stage `call`), their offer and the call plan in `offers/<lead-key>.md`, edited with the user.
2. After the call: `record_offer`, `update <key> status=offered offer_price=<price> offer_file=offers/<file>` (or won, lost, not_interested), then the recap (`tailor_offer` stage `recap`, template `call-recap`, `check_message`).
3. No decision yet: at most two follow-ups (stage `follow_up`), each adding something new.

## Today (`/leads:today`)

1. For each workbook in `leads/`: `python3 "$S" review list <workbook>`; approve the rows marked `keep` (Review and approve), say how many are still undecided and when the earliest expire, then `python3 "$S" due <workbook> --days 0`. Then `python3 "$S" sources report <workbook>`: when a source is marked `stop`, say it in one line (results, good leads, the week) and ask whether to pause or remove it (Find leads, step 1b).
2. Group by what to do: answer (talking, warm), calls to prepare (meeting), follow up after a call (offered, at most two follow-ups), engage again (engaging, to_engage).
3. For each: the next step and a draft (comment, reply, the call plan, or a follow-up via the `offer` skill at stage `follow_up`).

## Problems summary (`/leads:problems`)

A short roundup of the problems that came up most in the Reddit posts Claude read and scored 6 or more for a campaign, kept or not, in the posters' own words, with what they asked for: material for the user's own posts and for comments on LinkedIn and Instagram. It reads the workbook only: no search runs, nothing is spent on the user's Apify account and nothing reaches the server.

1. The campaign: ask which when several list Reddit (or all of them, a section each); a campaign without Reddit has no roundup, say so. The window is the last 30 days unless the user names another.
2. `python3 "$S" problems report <workbook> --days 30`: the posts of the window counted per wording of the problem, most first, each with the asks, the subreddits, up to five phrases and the last date, then the window's totals (`posts`, `asks`, `subreddits`). It judges nothing; its `note` says the counts are per wording.
3. Group the wordings that mean the same (for example "site crashed on drop day" and "store went down during the drop"). Per group, add up the posts, the asks and the subreddits from the report's figures, never from memory or an estimate, and pick one or two of its phrases.
4. With fewer than 5 posts in the window, list them (the problem, what they asked for, the subreddit, a phrase) and say the sample is small: no ranking and no "most". With 5 or more, the groups by posts, at most five.
5. Write `problems/YYYY-MM-DD.md` with today's date (create `problems/` on first write; when today's file exists, add or replace this campaign's section). A section per campaign:
   - What it covers, in one line: only the N posts Claude read and scored 6 or more for this campaign from the first day of the window to today, kept or not.
   - The problems that came up most: per group the number of posts, one or two phrases in quotes, what they asked for, the subreddits.
   - Use it: three content ideas, one per top problem (fewer when there are fewer groups), each a post of the user's own that answers what posters asked for; and the wording to reuse in comments on LinkedIn and Instagram, from the posters' phrases.
   - Not yet in the campaign file: the phrases missing from 'Problems, in their words'.
6. Show the file's path and the top groups in the chat. Offer to add the missing phrases to the campaign's Reddit section, and write them only on the user's yes.

The file and the chat carry no name, title, link or handle, and no username or email: the report holds none, and nothing from the Reddit sheet or To review is added to it. Phrases are at most 12 words, as the report gives them. Counts come only from the report; never invent results, numbers or trends. The roundup feeds the user's own public posts and comments: never a private message to someone who hasn't engaged. A comment drafted from it follows `engagement.md` (plain words, no em or en dashes) and goes through `check_message`.

## Log outcomes

"Booked a call" → `status=meeting next_touch=<call date>`, then prepare the offer for it. "Made the offer on the call" → the After the call step of the `offer` skill. "Signed" → `won`. "Not now" → `not_interested` or a later `next_touch`. "Remove me" → the forget workflow.

## Topics (on demand only)

1. `topics.md` lists topics with phrases per platform. Check only when asked ("check my topics"), or in a playbook.
2. Run the searches for the chosen topic(s); people kept before are hidden automatically.
3. Treat the results as finds: `review add` them to the topic's campaign workbook, then Review and approve. Update "Last checked".

## Import a spreadsheet

1. `my_account` first. If `features.own_leads` is false (Basic), say that importing your own lead lists is a Pro feature and that on Basic Lead Finder works with the people it finds for you, point at the account page (`account_page`; the `pro` line says how to get Pro), and stop: don't read the file and don't run `import`. If `my_account` doesn't exist, the connector isn't connected (see SKILL.md) and stop.
2. The user drops a CSV or XLSX in `imports/` (or points to one).
3. Ask: add to an existing campaign workbook, or create a new campaign?
4. `python3 "$S" import <workbook> <file>`; add `--sheet Reddit|Instagram|Companies` when the file is clearly one platform.
5. Report added, updated and skipped rows. Imported rows don't count against the quota.
6. Offer research for imported leads that lack details.

## Export for a CRM

`python3 "$S" export <workbook> exports/<name>.csv [--sheet LinkedIn] [--status talking,meeting,offered]`. In a plain chat without files, use `export_csv` for download links instead.

## Forget a person

1. `forget_person` with their profile link (removes them from the server and blocks them from future results).
2. `python3 "$S" remove <workbook> <profile link or key>` for every workbook in `leads/`, delete their file in `offers/`, and their mentions in notes.
3. Remind the user to remove them from their CRM and email tools, and to confirm to the person if they asked.
