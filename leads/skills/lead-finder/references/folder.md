# The Lead Finder folder

Created by the setup workflow in the folder the user picks (in Cowork, the working folder). Plain Markdown and one workbook per campaign, so the user can read and edit everything.

```
README.md
offer.md
campaigns/
  <campaign-slug>.md
topics.md
offers/
  <lead-key>.md        the offer for one lead and the call plan
templates/
  linkedin-comment.md
  reddit-comment.md
  instagram-comment.md
  connection-request.md
  reply-to-message.md
  suggest-a-call.md
  offer-follow-up.md
  call-recap.md
leads/
  <campaign-slug>.xlsx
problems/
  YYYY-MM-DD.md        the roundups of what came up most on Reddit, one file per run
imports/
exports/
```

`problems/` is created by `/leads:problems` on its first run; setup doesn't create it.

Slugs: lowercase, words joined with `-`, e.g. `uk-dtc-fashion`. The workbook has the same slug as its campaign.

## README.md

Write this once (adapt the names):

```markdown
# Lead Finder

This folder is your lead database. Claude reads and updates it with the Lead Finder plugin.

- offer.md: what you sell. campaigns/: who you target. topics.md: phrases to check on demand. offers/: the offer for each lead you have a call with.
- leads/*.xlsx: one workbook per campaign. Finds wait in the To review sheet until you mark keep or skip. The Sources sheet shows how each subreddit, bio word and search did. The Problems sheet keeps the problem, the ask and a short phrase of every fitting Reddit post, without names or links. Edit status, notes and drafts freely; Summary, Next touches and Pipeline are rebuilt automatically.
- problems/: the roundups of the problems your market describes on Reddit, for your own content.
- Engage in public first (comments, reactions). Write privately only to people who've interacted with you.
- The Lead Finder server keeps search results for 12 hours only. What you keep lives here, and is your responsibility: keep it secure, delete people who ask, don't share it.
```

## offer.md

A mirror of the offer saved on the Lead Finder server (`get_offer` returns it as Markdown). Build and change it with the `offer-builder` skill, which saves to the server and rewrites this file; don't edit it by hand. Sections: who it's for, the result they want, problems solved, what's included (with durations), price and terms, proof, guarantee, what happens quickly, what they don't have to do, bonuses, real limits, on the call (anchor, Option A, Option B, fallback), next step, sender, languages.

## offers/<lead-key>.md

The offer for one lead and the call plan (the key with `:` replaced by `-`, e.g. `linkedin-pub-olivia-hart.md`), written by the `offer` skill before the call and completed after it:

```markdown
# Offer for Olivia Hart · Linden Knitwear

Call: 3 Oct, 30 minutes · offered 4,200 EUR

## Her goal
"A site that keeps up with drop days" (her message, 30 Sep)

## What's included for Linden
- Store rebuild on Shopify, checkout set up for launch traffic · 6 weeks
- Migration of products, customers and redirects
- Launch-day monitoring for the spring drop

## Price
4,200 EUR one-off · 50% upfront, 50% at launch

## Why it'll work for her
Harbour & Co grew conversion 38% after the rebuild. If the store isn't live in 8 weeks, we work for free until it is.

## The call plan
Her goal first. Anchor: Rebuild + 12 months of growth, 14,000 EUR. Then her offer, then stop.
Expect: "Can we do it after the drop?" Answer: the 6-week timeline and launch-day monitoring.
After a no: "Is it the total, or paying it all at once?" Option A: 3 payments of 1,400 EUR. Option B: without the monitoring, 2,600 EUR.

## After the call
(What was offered, what she said, the next step. Then the recap and any follow-ups, newest last.)
```

## campaigns/<slug>.md

```markdown
# <Campaign name>

Offer: offer.md
Workbook: leads/<slug>.xlsx
Status: active

## Ideal customer
Who they are in one or two lines: the role that signs, the company type, what they want. Who to exclude (customers, competitors, partners).

## Platforms
Only the platforms listed here are searched for this campaign. A campaign file without this section is searched on all three.

### LinkedIn
Finds people directly, by role and company.
- Job titles: Head of Ecommerce, Ecommerce Director, Founder
- Industries: Retail, Apparel and Fashion
- Company size: 11-50, 51-200
- Locations: United Kingdom

### Reddit
Finds posts where someone describes a problem you solve, so you can answer in the thread. Their words here also teach you how they talk.
- Problems, in their words: "site crashed on drop day", "shopify checkout slow", "lost sales during the launch", "store can't handle traffic" (as many as you can; never job titles)
- Looking for, when they post: a fix before the next drop, a developer or agency recommendation, someone who had the same problem
- Subreddits (approved, checked 2026-11-03, topics: shopify, ecommerce, small online shops; re-check monthly with /leads:update):
  - r/dropdayshops: 42k members, 1.1k weekly visitors, 160 weekly contributions, newest post 3 hours ago. Promotion: "No self-promotion or store links" (rule 2). DMs: not mentioned.
  - r/indiebrandowners: 18k members, 600 weekly visitors, 70 weekly contributions, newest post 9 hours ago. Promotion: not mentioned. DMs: "Don't message members to sell" (rule 5).

### Instagram
Finds accounts whose bio contains one of the bio words (a web search of Instagram profiles, then each profile read in full). Bio words: short phrases people write in their bio, in their language, with plural or spelling variants as their own entries.
- Bio words: "slow fashion", "small batch", "independent label"
- Paused bio words: "drops" (paused 2026-11-10: 1 good lead from 22 accounts in 7 days)
- A good bio shows: a brand selling its own products online, launches in drops, a shop link

## Disqualifiers
Rules that rule a lead out, applied in every score: a match scores 1 or 2 and the reason names the rule. Fit only: role, company, business model, need; never age, gender, nationality, ethnicity, religion, health, family status or photos.
- Sells on marketplaces only, no own store
- Agencies and freelancers who serve brands
- Fewer than 3 people

## Searches that work
- LinkedIn people: titles [...], seniority [...], locations [...], industries [...]
- LinkedIn posts: "phrase one", "phrase two"
- Reddit: r/<sub>: "phrase"
- Instagram: #hashtag, "keywords"

## Searches that didn't work
- LinkedIn people: titles [...], locations [...] (retired 2026-11-10: 1 good lead from 15 results in 7 days)

## Exclude
Company links or names never to engage with.

## Learnings
What the user marked as good or bad fits, what got people to engage back, and why (use it in later scores and suggestions).
```

Update "Searches that work" and "Learnings" as you go; on Reddit, add the phrases from good posts to "Problems, in their words" (`/leads:problems` offers the ones its roundup found missing, added on the user's yes). The Reddit phrases are what Claude judges posts against in the daily scan, not search terms. `/leads:update` changes Platforms and Disqualifiers.

The Subreddits block holds only subreddits the user approved after the subreddit check, one line each with the figures, the promotion and DM rules in short (quoted, never paraphrased) and the date; an entry can end with `(paused YYYY-MM-DD: reason)` and is then left out of searches until the next re-check. An older one-line `- Subreddits: r/a, r/b` is unchecked: offer `check_subreddits` before searching, and `/leads:update` turns it into the block. A subreddit under the stop rule (10 or more posts, fewer than 3 good leads in 7 days, from `sources report`) is paused with the same marker, for example `(paused 2026-11-10: 1 good lead from 240 posts in 7 days)`, or removed, on the user's answer.

`Paused bio words` (optional, in the Instagram section) holds the bio words paused under the stop rule on the user's yes, each with the date and the counts; they are left out of searches until the user moves one back to Bio words with `/leads:update`. A campaign file without the line has no paused words.

`## Searches that didn't work` lists the searches the stop rule retired, one line each with the date, results and good leads; the find commands add to it on the user's yes, like Learnings, and never run a search listed there as it is.

Older campaign files may have a "Where they talk" section and no Platforms section: read "Where they talk" as before, search all three platforms, and use "Ideal customer" as the LinkedIn details until the user runs `/leads:update`.

## topics.md

```markdown
# Saved topics

Checked only when I ask ("check my topics"), or by a playbook.

## <Topic name>
Campaign: <slug>
- Reddit: "can anyone recommend a bookkeeper", "hate doing my own books" (r/smallbusiness)
- LinkedIn posts: "looking for a bookkeeper", "recommend an accountant"
- Instagram: #smallbusinessowner
Last checked: 2026-10-01
```

## templates/*.md

One file per template. Frontmatter plus the text, with placeholders:

```markdown
---
name: LinkedIn comment
channel: linkedin_comment     # linkedin_comment | linkedin_connect | linkedin_message | reddit_comment | reddit_dm | instagram_comment | instagram_dm | email
purpose: engage               # engage | conversation | call | recap | follow_up
language: English
subject:                      # emails only
source: starter pack          # or: user, or the tool that made it
---
{{specific_detail_from_their_post}}: {{your_point_or_experience}}. {{a_real_question_about_their_situation}}

Notes: …
```

Placeholders describe what goes there in plain words (`{{answer_to_what_they_said}}`, `{{price_and_how_they_pay}}`). Fill them from the lead's row (their posts, the interaction log, what they said) and the saved offer; never invent numbers or results.

Templates from another tool: save them as-is into `templates/` with `source: <tool name>`, after checking they don't pitch strangers.
