---
name: find-instagram
description: Find Instagram accounts whose bio contains the campaign's bio words - a web search of Instagram profiles for each word, each profile read in full, and only accounts whose bio contains one of the words shown, each checked against what a good bio shows before it scores above 5; hashtags when the campaign lists some. Finds go to the workbook's To review sheet. Use when the user types /leads:find-instagram or asks for Instagram leads.
user-invocable: true
---

Run the **Find leads on Instagram (`/leads:find-instagram`)** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/workbook.md`).

If there are several campaigns, ask which one that lists Instagram. The method: `search_instagram_bios` with the bio words in the campaign's Instagram section (at most 10 per call); the server shows only accounts whose bio contains one of the words and says which matched; check each bio against 'A good bio shows' before it scores above 5. `search_instagram` in hashtags mode when the section lists hashtags (posts from the last 72 hours only). Before searching, `sources report` says how each bio word did in the last 7 days; one with 10 or more results and fewer than 3 good leads is under the stop rule: ask to move it to Paused bio words, and move it only on the user's yes. Search 15 at a time. Score every account 1-10 with a one-line reason and apply the campaign's disqualifiers: a match scores 1 or 2 and the reason names the rule. 6 or more fits; a reason for 5 or less starts with 'wrong fit:' or 'not enough to judge:' (`references/scoring.md`).

Results are previews without handles or links. Every find is written to To review first; approving is the pick: `pick_leads` counts and unlocks the ones the user keeps, and they go into the Instagram sheet as `to_engage`. Research comes after the pick, never before. Say the quota left and the Apify cost, and suggest `/leads:engage` as the next step.
