---
name: find-linkedin
description: Find LinkedIn leads for a campaign by role and company - the campaign's job titles, industries, company size and locations, with posts and commenters as the warm signals; every find goes to the workbook's To review sheet and the ones the user keeps are saved. Use when the user types /leads:find-linkedin or asks for LinkedIn leads.
user-invocable: true
---

Run the **Find leads on LinkedIn (`/leads:find-linkedin`)** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/workbook.md`).

If there are several campaigns, ask which one that lists LinkedIn. The method: people by role and company with `search_linkedin_people`, from the job titles (several variants), industries, company size and locations in the campaign's LinkedIn section, leaving out the companies on its Exclude list. Before searching, `sources report` says how each search did in the last 7 days; one with 10 or more results and fewer than 3 good leads is under the stop rule: ask to note it under Searches that didn't work, write it only on the user's yes, and change the search. Search 15 at a time. When someone talks about the problem now, their posts and the people commenting on a relevant post are the warm signals (`search_linkedin_posts`, `search_post_engagers`); companies hiring or advertising for the problem lead to the right roles there. Score every result 1-10 with a one-line reason and apply the campaign's disqualifiers: a match scores 1 or 2 and the reason names the rule. 6 or more fits; a reason for 5 or less starts with 'wrong fit:' or 'not enough to judge:' (`references/scoring.md`).

Results are previews without links or handles. Every find is written to To review first; approving is the pick: `pick_leads` counts and unlocks the ones the user keeps, and they go into the LinkedIn sheet (Companies for companies) as `to_engage`. Research comes after the pick, never before. Say the quota left and the Apify cost, and suggest `/leads:engage` as the next step.
