---
name: update
description: Change a campaign's setup - add or remove the platforms Lead Finder searches (LinkedIn, Reddit, Instagram), change what each platform looks for (job titles and locations, the problems in the customer's words, the bio words) and the disqualifiers that rule a lead out, and re-check the approved subreddits about once a month (which went quiet, which new ones appeared), and lift or confirm what was paused under the stop rule (a subreddit, a bio word). Use when the user types /leads:update or wants to change where or who Lead Finder searches for.
user-invocable: true
---

Run the **Update a campaign** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/folder.md`).

Ask which campaign when there are several. Show what's set now, change only what the user asks for, and rewrite only the Platforms and Disqualifiers sections of the campaign file; learnings, the searches that work or didn't, and the workbook stay as they are. Removing a platform removes no lead. This command never searches for leads; the subreddit re-check runs on the user's Apify account.
