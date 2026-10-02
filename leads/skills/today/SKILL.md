---
name: today
description: What's due today across the Lead Finder workbooks - leads to answer, offers to follow up, leads to engage again, calls - with a draft for each. Use when the user types /leads:today or asks what to do today, who to follow up with or who's waiting for an answer.
user-invocable: true
---

Run the **Today** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/engagement.md`).

Check every workbook in `leads/` with `workbook.py due --days 0`. Group by what to do: answer (talking, warm), follow up an offer (offer_sent; at most two follow-ups, each adding something new), engage again (engaging, to_engage), calls (meeting). Draft each one (a reply, an offer follow-up with the `offer` skill at stage follow_up, or a comment) and run `check_message`. Log what the user says they did with `workbook.py interact`.
