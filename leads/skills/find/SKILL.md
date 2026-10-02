---
name: find
description: Find new leads for a campaign - pick the best source (LinkedIn, Reddit, Instagram), search, score, let the user choose, and save the picked leads to the workbook to engage with. Use when the user types /leads:find, optionally with what or who to look for.
user-invocable: true
---

Run the **Find leads** workflow of the `lead-finder` skill (read its SKILL.md and `references/workflows.md`).

If the user gave a request with the command, use it together with the campaign file. If there are several campaigns, ask which one. Prefer people who post and comment: they're the ones the user can engage with. Always end by saving the picked leads into the campaign's workbook as `to_engage`, and say the quota left and the Apify cost. Suggest `/leads:engage` as the next step.
