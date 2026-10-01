---
name: follow-ups
description: Show the follow-ups due across the Lead Finder workbooks and draft the next message for each. Use when the user types /leads:follow-ups or asks who to follow up with.
user-invocable: true
---

Run the **Follow-ups** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/outreach.md`).

Check every workbook in `leads/` with `workbook.py due --days 1`. Group by overdue, today and tomorrow. Draft each follow-up into `draft_follow_up`, and log sends with `update … status=contacted` once the user confirms they sent them.
