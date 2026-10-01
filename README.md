# Lead Finder plugin for Claude

Find B2B leads on LinkedIn, Reddit and Instagram from Claude (Cowork, Desktop, Claude Code), keep them in a workbook in a folder on your computer, draft outreach and track follow-ups. Searches run on your own Apify account. Nothing is ever sent for you.

## Install

1. Get a Lead Finder account: https://leadfinder.madefast.dev (sign in with your email, accept the terms, add your Apify token).
2. In Claude Desktop: **Customize → Plugins → Add marketplace**, enter `madefast-ai/lead-finder-plugin`, then install **Lead Finder**.
3. Open the plugin's **Connectors** tab and click **Connect**; sign in with the same email.
   If Connect stays greyed out, add it by hand: **Customize → Connectors → Add custom connector**, URL `https://leadfinder.madefast.dev/mcp`.
4. In Cowork, pick a folder for your leads and type `/leads:setup`.

## What's inside

- `leads/.mcp.json`: the Lead Finder connector (`https://leadfinder.madefast.dev/mcp`, OAuth sign-in).
- `leads/skills/lead-finder/`: the working method (folder layout, workbook, workflows, outreach rules), the workbook script (`scripts/workbook.py`, needs Python 3 and openpyxl) and starter templates.
- `leads/skills/offer-builder/` and `leads/skills/offer/`: build the offer once (saved on the server), then write an offer for one lead on any platform.
- Slash commands: `/leads:setup`, `/leads:find`, `/leads:offer-builder`, `/leads:offer`, `/leads:follow-ups`, `/leads:import`.

## Updating

Bump `version` in `leads/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, commit and push. Users get the update with **Check for updates** (or automatically when sync is on).

## Data

The Lead Finder server keeps search results for 12 hours, then deletes them; the leads you keep live in your folder. See https://leadfinder.madefast.dev/terms, /privacy and /gdpr.
