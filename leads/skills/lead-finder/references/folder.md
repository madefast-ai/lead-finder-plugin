# The Lead Finder folder

Created by the setup workflow in the folder the user picks (in Cowork, the working folder). Plain Markdown and one workbook per campaign, so the user can read and edit everything.

```
README.md
offer.md
campaigns/
  <campaign-slug>.md
topics.md
offers/
  <lead-key>.md        offer cards for individual leads
templates/
  connection-note.md
  after-connect.md
  cold-email.md
  follow-up-message.md
  follow-up-email.md
  reddit-reply.md
  instagram-dm.md
  free-report-*.md
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

- offer.md: what you sell. campaigns/: who you target. topics.md: phrases to check on demand.
- leads/*.xlsx: one workbook per campaign. Edit status, notes and drafts freely; Summary, Follow-ups and Pipeline are rebuilt automatically.
- The Lead Finder server keeps search results for 12 hours only. What you keep lives here, and is your responsibility: keep it secure, delete people who ask, don't share it.
- Tell every person you contact where you found their details and how to opt out.
```

## offer.md

A mirror of the offer saved on the Lead Finder server (`get_offer` returns it as Markdown). Build and change it with the `offer-builder` skill, which saves to the server and rewrites this file; don't edit it by hand. It looks like:

```markdown
# Offer

## What we sell
One or two sentences, in the customer's words.

## Who it's for
Company types, sizes, roles that buy, roles that use it.

## The problem it solves
The pain, as the buyer would describe it.

## Proof
Customers, results with numbers, testimonials. Only true things.

## Call to action
The low-effort next step: a 20-minute call, a free audit, a report, a trial.

## Sender
Name, role, company, website. Signature for emails (with an opt-out line).

## Languages
Which languages outreach is written in, and formal or informal address.
```

## offers/<lead-key>.md

One offer card per lead (the key with `:` replaced by `-`, e.g. `linkedin-pub-olivia-hart.md`): their goal in their words, the likely objection, what answers it, the first-touch offer, the angle, the next step, and the messages sent, newest last.

## campaigns/<slug>.md

```markdown
# <Campaign name>

Offer: offer.md
Workbook: leads/<slug>.xlsx
Status: active

## Ideal customer
Roles, seniority, company size, industries, locations. Who to exclude (customers, competitors, partners).

## Angle
Why this segment, now. The hook for the first message.

## Searches that work
- LinkedIn people: titles [...], seniority [...], locations [...], industries [...]
- LinkedIn posts: "phrase one", "phrase two"
- Reddit: r/<sub>: "phrase"
- Instagram: #hashtag, "keywords"

## Exclude
Company links or names never to contact.

## Learnings
What the user marked as good or bad fits, and why (use it in later scores and filters).
```

Update "Searches that work" and "Learnings" as you go: when the user says "more like this" or "less like this", write the reason there.

## topics.md

```markdown
# Saved topics

Checked only when I ask ("check my topics").

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
name: Connection note
channel: connection_note      # connection_note | message | inmail | email | reddit_reply | reddit_dm | instagram_dm
purpose: first_touch          # first_touch | after_connect | follow_up
language: English
subject:                      # emails only
source: starter pack          # or: user, or the tool that made it
---
Hi {{first_name}}, {{personal_hook}}. I work with teams like {{company}} on {{pain}}. Happy to connect.

Notes: Fit 200 characters (300 on Premium). No pitch, no link.
```

Placeholders: `{{first_name}}`, `{{salutation}}` (formal address in the template's language, only when the profile makes it clear, else the full name), `{{company}}`, `{{role}}`, `{{personal_hook}}` (one specific, true detail from their profile, post or comment), `{{pain}}`, `{{proof}}`, `{{call_to_action}}`, `{{sender_name}}`, `{{sender_company}}`, `{{data_source_note}}` (the opt-out line from outreach.md), `{{username}}` and `{{subreddit}}` (Reddit), `{{helpful_answer}}` (a genuine answer to their question), and for free-report templates `{{report_link}}`, `{{report_finding}}`, `{{report_quick_wins}}`, `{{report_quick_win}}` (from the lead's notes or the campaign file; never invent numbers).

Templates from another tool (for example a message-writing connector): save them as-is into `templates/` with `source: <tool name>`, and put their drafts in the workbook's draft columns.
