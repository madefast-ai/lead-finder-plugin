# Scoring

Every find gets a score from 1 to 10 and a one-line reason, against the saved offer and the campaign file. The score is a suggestion: the user decides who to keep. Score from what the result shows; never guess what isn't there.

Never score on age, gender, nationality, ethnicity, religion, health, family status or photos, and never write them in a reason.

## The score

- **6 or more fits** and is worth engaging. It's the same bar everywhere: a scanned Reddit post needs it to go to To review, and the Sources sheet counts a find scored 6 or more as a good lead (the stop rule reads it).
- **5 or less** doesn't fit, or there wasn't enough to tell. The reason starts with a label.
- **1 or 2** is a disqualifier match: the campaign's Disqualifiers rule the lead out even when the rest fits.

| Score | What it means |
|---|---|
| 9-10 | the right person (or post) with a clear signal or ask |
| 7-8 | fits; the signal or the ask is close to the offer without naming it |
| 6 | fits and is worth engaging, nothing more |
| 3-5 | `wrong fit:` or `not enough to judge:` |
| 1-2 | `rules out:` and the rule |

## The labels

A reason for a score of 5 or less starts with one of these, lowercase, with the colon, as its first words:

- `wrong fit:` the result is clear and it's someone the offer isn't for (another role, a company too small or too big, a reseller, an agency, a post that sells). Say what doesn't fit.
- `not enough to judge:` what is shown doesn't tell (a one-word headline, a bio too short, a post without its text). Say what's missing.
- `rules out:` a disqualifier matched (scores 1 or 2). Name the rule as the campaign file writes it.

The labels live in `score_reason`, so the To review sheet, the platform sheets and the chat table show the same words, and the user can filter the column in Excel by its first words. `review add` reports rows scored 5 or less without a label as `unlabelled`: label them and add again.

"Not enough to judge" is not a good lead. A source that keeps giving such finds falls under the stop rule like any other; the counts per source tell the user why.

## LinkedIn: the person

Score the person: role, company, need, signal.

- Role: the job titles in the campaign's LinkedIn section, or the person who decides on what the user sells.
- Company: industry, size and location against the section.
- Need: a recent post, comment or hiring signal about the problem the offer solves raises the score; a profile alone stays at 6 to 8.
- A company (from a company search) is scored on its reason to buy: hiring for the role the user replaces, ads, growth.

## Reddit: the post

Reddit scores the post, not the poster: how closely it matches 'Problems, in their words' and what the poster asks for ('Looking for, when they post'). The poster's history or profile is never scored (the preview doesn't show it).

What the poster asks for, and how it scores when the problem fits:

| The ask | Score when the problem fits |
|---|---|
| a recommendation (a tool, a developer, an agency) | 8 or more |
| help with a fix | 8 or more |
| how others do it | 8 or more |
| an opinion or validation | 6 to 8 |
| hiring | 6 to 8 |
| venting | 6 or 7 at most |
| selling (the poster offers the thing) | `wrong fit:` |

A post whose problem doesn't fit is a `wrong fit:` whatever it asks for.

The reason for 6 or more names the problem and the ask, in this form: `<the problem, in short>; asks for <the ask>`. The engage step reads the ask from it, so the comment answers what the poster asked. When the post matches one of the campaign's 'Problems, in their words', use that phrase as the problem part of the reason, so the same problem reads the same across posts; otherwise the problem in short, in the poster's terms. The reason names no person, business or post title. `review add` logs the problem, the ask and the item's `phrase` (the poster's own words for the problem, at most 12 words, no names) in the Problems sheet, which `/leads:problems` counts.

The scan shows text clipped to 280 characters. Before calling a post `not enough to judge:`, read its full text with `get_results` (state `new` and the scan's `search_id`); the clip is the usual cause.

## Instagram: the account

Score the account against 'A good bio shows' in the campaign's Instagram section. The server matched words only: a bio word can match someone else.

- The bio shows what a good bio shows (the kind of business, how it sells): 6 or more.
- `wrong fit:` the word matched and the bio shows someone else (an agency, a shopper, a reseller).
- `not enough to judge:` a bio too short to tell.

Followers and the business category help; photos never count.

## The reason, per band

- 9-10 and 7-8: who they are and the signal or the ask, in one line.
- 6: who they are and why it fits.
- 3-5: the label, then what doesn't fit or what's missing.
- 1-2: `rules out:` and the rule.

One line, plain words, no em or en dashes.

## Examples

Fictional, for a developer who fixes slow online shops on launch days.

| Score | Reason |
|---|---|
| 9 | checkout slowed down on drop day; asks for a developer recommendation |
| 8 | Head of Ecommerce at a 40-person apparel brand, posted about a crash during last week's launch |
| 8 | store can't handle traffic on launches; asks how others do it |
| 6 | lost sales during a launch; venting |
| 6 | Founder of Fernhill Goods, runs product drops from its own shop |
| 4 | wrong fit: agency selling launch support |
| 4 | wrong fit: Marketing Assistant, doesn't decide on development work |
| 3 | not enough to judge: the bio says only "shop" |
| 3 | not enough to judge: the title only, the post has no text |
| 2 | rules out: sells on marketplaces only, no own store |
