---
name: problems
description: A short roundup of the problems that came up most in the Reddit posts Claude read for a campaign in the last 30 days, in the posters' own words, with what they asked for and where, counted from the workbook's Problems sheet and written to problems/YYYY-MM-DD.md with three content ideas. Use when the user types /leads:problems or asks what problems come up on Reddit, what my market says, or for content ideas from Reddit.
user-invocable: true
---

Run the **Problems summary (`/leads:problems`)** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md`, `references/workbook.md` and `references/engagement.md`).

If there are several campaigns that list Reddit, ask which one (or all of them); a campaign without Reddit has no roundup. The window is the last 30 days unless the user names another. Run `workbook.py problems report <workbook> --days 30`: it counts, per wording, the Reddit posts Claude scored 6 or more for this campaign, kept or not, with what they asked for, the subreddits and short phrases in the posters' own words. Group the wordings that mean the same and count the posts per group from the report's figures only. With fewer than 5 posts in the window, list them and say the sample is small instead of ranking.

Write `problems/YYYY-MM-DD.md` (create `problems/` when it's missing) with a section per campaign: what the roundup covers (only the posts Claude read and scored for this campaign in the window), the problems that came up most with their counts, one or two phrases each, what they asked for and the subreddits; then three content ideas, one per top problem, each a post of the user's own that answers what posters asked for, and the wording to reuse in comments on LinkedIn and Instagram; then the phrases not yet in the campaign's 'Problems, in their words', added to the campaign file only on the user's yes.

The roundup carries no name, title, link or handle, and no username or email; phrases are at most 12 words. Never invent counts, results or trends. It is material for the user's own posts and comments, never a private message to someone who hasn't engaged. Every comment drafted from it follows `references/engagement.md` and goes through `check_message`. Nothing is searched: the roundup reads the workbook only, so it costs nothing on the user's Apify account and doesn't touch the quota.
