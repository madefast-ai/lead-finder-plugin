# The Lead Finder folder

Created by the setup workflow in the folder the user picks (in Cowork, the working folder). Plain Markdown and one workbook per campaign, so the user can read and edit everything.

```
README.md
offer.md
campaigns/
  <campaign-slug>.md
topics.md
offers/
  <lead-key>.md        the offer for one lead, as sent
templates/
  linkedin-comment.md
  reddit-comment.md
  instagram-comment.md
  connection-request.md
  reply-to-message.md
  offer-message.md
  offer-follow-up.md
  call-recap.md
leads/
  <campaign-slug>.xlsx
imports/
exports/
```

Slugs: lowercase, words joined with `-`, e.g. `uk-dtc-fashion`. The workbook has the same slug as its campaign.

## README.md

Write this once (adapt the names):

```markdown
# Lead Finder

This folder is your lead database. Claude reads and updates it with the Lead Finder plugin.

- offer.md: what you sell. campaigns/: who you target. topics.md: phrases to check on demand. offers/: the offer you sent each lead.
- leads/*.xlsx: one workbook per campaign. Edit status, notes and drafts freely; Summary, Next touches and Pipeline are rebuilt automatically.
- Engage in public first (comments, reactions). Write privately only to people who've interacted with you.
- The Lead Finder server keeps search results for 12 hours only. What you keep lives here, and is your responsibility: keep it secure, delete people who ask, don't share it.
```

## offer.md

A mirror of the offer saved on the Lead Finder server (`get_offer` returns it as Markdown). Build and change it with the `offer-builder` skill, which saves to the server and rewrites this file; don't edit it by hand. Sections: who it's for, the result they want, problems solved, what's included (with durations), price and terms, proof, guarantee, what happens quickly, what they don't have to do, bonuses, real limits, on the call (anchor, Option A, Option B, fallback), next step, sender, languages.

## offers/<lead-key>.md

The offer for one lead (the key with `:` replaced by `-`, e.g. `linkedin-pub-olivia-hart.md`), written by the `offer` skill:

```markdown
# Offer for Olivia Hart · Linden Knitwear

Status: sent 2 Oct on LinkedIn · 4,200 EUR

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

## For the call
Anchor: Rebuild + 12 months of growth, 14,000 EUR. Option A: 3 payments of 1,400 EUR. Option B: without the redesign and monitoring, 2,600 EUR.

## Messages
(The offer message and any follow-ups, newest last.)
```

## campaigns/<slug>.md

```markdown
# <Campaign name>

Offer: offer.md
Workbook: leads/<slug>.xlsx
Status: active

## Ideal customer
Roles, seniority, company size, industries, locations. Who to exclude (customers, competitors, partners).

## Where they talk
The topics they post about, the subreddits and hashtags they use: where to engage with them.

## Searches that work
- LinkedIn people: titles [...], seniority [...], locations [...], industries [...]
- LinkedIn posts: "phrase one", "phrase two"
- Reddit: r/<sub>: "phrase"
- Instagram: #hashtag, "keywords"

## Exclude
Company links or names never to engage with.

## Learnings
What the user marked as good or bad fits, what got people to engage back, and why (use it in later scores and suggestions).
```

Update "Searches that work" and "Learnings" as you go.

## topics.md

```markdown
# Saved topics

Checked only when I ask ("check my topics"), or by a routine.

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
purpose: engage               # engage | conversation | offer | follow_up | call
language: English
subject:                      # emails only
source: starter pack          # or: user, or the tool that made it
---
{{specific_detail_from_their_post}}: {{your_point_or_experience}}. {{a_real_question_about_their_situation}}

Notes: …
```

Placeholders describe what goes there in plain words (`{{answer_to_what_they_said}}`, `{{price_and_how_they_pay}}`). Fill them from the lead's row (their posts, the interaction log, what they said) and the saved offer; never invent numbers or results.

Templates from another tool: save them as-is into `templates/` with `source: <tool name>`, after checking they don't pitch strangers.
