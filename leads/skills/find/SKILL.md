---
name: find
description: Find new leads for a campaign - approve what's waiting in the workbook's To review sheet, then search each of the campaign's chosen platforms by its own method (or one platform with /leads:find linkedin, reddit or instagram), score, write the finds to To review and save the ones the user keeps. Use when the user types /leads:find, optionally with a platform or what to look for.
user-invocable: true
---

Run the **Find leads (`/leads:find`)** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/workbook.md`).

If there are several campaigns, ask which one. If the user named a platform, run only that platform's section: the same as `/leads:find-linkedin`, `/leads:find-reddit` or `/leads:find-instagram`. Otherwise start with Review and approve for what's already waiting in the workbook's To review sheet, then search each platform in turn. Search only the platforms the campaign lists (all three when it lists none), each by its own method, and apply the campaign's disqualifiers to every score. If the user gave a request with the command, use it together with the campaign file. Prefer people who post and comment: they're the ones the user can engage with. Before each platform's search, read how its sources did (`sources report`) and apply the stop rule: a subreddit, bio word or search with 10 or more results and fewer than 3 good leads in 7 days is paused or retired, on the user's yes. Search 15 at a time.

Results are previews without links or handles; every find is written to the workbook's To review sheet before you ask, and picking unlocks and counts the ones the user keeps. Research comes after the pick, never before. End with Review and approve: the kept leads go into the platform's sheet as `to_engage`, and say the quota left and the Apify cost. Suggest `/leads:engage` as the next step.
