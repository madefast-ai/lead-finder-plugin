---
name: engage
description: Engage with leads in public before ever messaging them - pick today's leads, find their latest posts, suggest a genuine comment for each, and log it when the user has posted it. Use when the user types /leads:engage, asks who to engage with, or says they commented on, reacted to or connected with someone.
user-invocable: true
---

Run the **Engage** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/engagement.md`).

Pick 5-10 leads in `to_engage`, `engaging` or `warm` whose next touch is due (or the ones the user names). For each: one post worth engaging with (link, what it's about) and a suggested comment that adds something, never a pitch. Run `check_message` with stage `engage` and fix every error. Save drafts with `workbook.py update <key> "draft_comment=…"`.

The user posts the comments themselves. When they say they did ("done", "commented on Olivia's"), log each one: `workbook.py interact <workbook> <key> --by you --channel <platform> --kind comment --url <post link>`. After 3-4 comments on LinkedIn, suggest a connection request without a pitch.
