---
name: check
description: Check who engaged back - run check_lead_activity for the leads the user is engaging with, mark the ones who replied, commented or reacted as warm, suggest the next comment on their new posts, and ask about messages the check can't see. Use when the user types /leads:check or asks who engaged, replied or reacted.
user-invocable: true
---

Run the **Check who engaged back** workflow of the `lead-finder` skill (read its SKILL.md and `references/workflows.md`).

Up to 10 leads in `engaging` (and `warm` leads with no conversation yet), oldest touch first. Call `check_lead_activity` with their profile links and the post links from their interaction log (`engaged_posts`, and the links to the user's own comments when logged). Log every `engaged_back` with `workbook.py interact … --by them`, report who engaged and how (`replied_to_your_comment`, `commented_on_your_posts`, `commented_where_you_engaged` or `replied_where_you_engaged`, `reacted_to_your_posts`: say which, with the post), and suggest the next comment for leads with new posts. Then ask the user whether anyone messaged them, accepted a connection, followed back, replied to a DM or liked their Instagram post (the check can't see likes there), and log it. Say the Apify cost, and when the result says Instagram replies need a paid Apify plan, say that once.
