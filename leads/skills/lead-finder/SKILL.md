---
name: lead-finder
description: Lead Finder's working method in a folder on the user's computer. Use whenever the user wants to find leads or prospects (LinkedIn, Reddit, Instagram), keep or pick leads, approve the review list, save them to their lead workbook, research a lead, engage with leads (comments, reactions), log an interaction ("I commented on…", "she replied"), check who engaged back, answer a lead who wrote to them, create an offer for a lead, see what's due today, get a roundup of the problems that come up on Reddit, import or export a leads spreadsheet, check saved topics, or remove a person. Works with the Lead Finder connector (tools such as my_account, search_linkedin_people, get_results, check_lead_activity).
---

# Lead Finder

Lead Finder finds B2B leads through the user's own Apify account and helps turn them into conversations. The **server** keeps search results for 12 hours only. **Everything else lives in the user's folder**: what they sell, campaigns, saved topics, templates, the offers sent, and one workbook per campaign with every lead's status, interaction log, notes and drafts. You do the file work; the connector does the searching.

**Never reach someone who hasn't interacted with the user.** The user engages in public first (genuine comments, reactions, a connection request without a pitch); private messages, DMs and email only once the lead has engaged back or written; the offer only once they're interested. Never send anything and never use the user's social accounts: the user does every interaction themselves, and tells you so you can log it. Details: `references/engagement.md`.

## Before anything else

1. Call `my_account`, then `get_offer`: the user's offer is saved on the server. Never ask them to explain their business again when it exists. If the tool doesn't exist, the connector isn't connected: tell the user to open the plugin's Connectors tab (or More → Customize → Connectors, adding a custom connector with `https://leadfinder.madefast.dev/mcp`) and sign in, then stop.
2. Handle what it says: waiting for approval (searches won't run yet; setup still works), no Apify token (the account page, or `set_api_key` if they paste it), terms to accept (the link it gives), no `my_profiles` (ask for their LinkedIn link, Reddit username, Instagram handle: `set_my_profiles`). Say **Basic** and **Pro**, never free and paid.
   - `features.own_leads` false (Basic): `/leads:import` is off, and research, the activity check and the offer work only for people Lead Finder found; when the server skips or refuses someone for that reason, tell the user once that working with your own leads is a Pro feature and move on, never retry with another link.
   - `features.max_offers` is a number (Basic keeps one saved offer) and `features.offers_saved` has reached it: another offer can't be created; update the saved offer instead, or `delete_offer` first. When `features.max_offers` is null (Pro), there is no cap.
   - A token refused as already saved on another account: say so once and point at the account page; never suggest another token of the same Apify account.
3. Find the Lead Finder folder: the working folder if it has `offer.md` and `leads/`; otherwise ask where it is, or run the setup workflow.

## The folder

Read `references/folder.md` for the layout and the formats of `offer.md`, campaign files, `topics.md`, templates and `offers/`. In short:

```
offer.md                a mirror of the saved offer (the server keeps the original)
campaigns/<slug>.md     one ideal-customer segment: the platforms to search, what each one looks for, what rules a lead out
topics.md               saved phrases to check on demand, per platform
templates/*.md          comment, reply and offer templates
offers/<lead-key>.md    the offer for one lead and the call plan
leads/<slug>.xlsx       the workbook of that campaign
problems/YYYY-MM-DD.md  a roundup of the problems that came up most on Reddit
imports/  exports/      files in and out
```

## The workbook

One `.xlsx` per campaign with sheets **LinkedIn**, **Companies**, **Reddit**, **Instagram** (the main lists, the source of truth), **To review** (every find waits here with a score and no links until the user keeps or skips it), **Sources** (how each subreddit, bio word and search did: results, good leads, kept), **Problems** (what came up in the Reddit posts Claude read: the problem, the ask, a phrase) and **Summary**, **Next touches**, **Pipeline** (rebuilt automatically, never edit them). Always change it through the script:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py" <command> leads/<slug>.xlsx ...
```

If `${CLAUDE_PLUGIN_ROOT}` isn't set, find `workbook.py` in this skill's `scripts/` folder. If openpyxl is missing, `pip install openpyxl`. Statuses: new → to_engage → engaging → warm → talking → meeting → offered → won / lost (plus not_interested, do_not_contact). Commands and columns: `references/workbook.md`. Close the file in Excel first if the script says it can't write; if it says another Lead Finder task is writing the workbook, wait a minute and run the command again.

## Workflows

Details for each are in `references/workflows.md`. Load it when you run one.

- **Set up** (first time, or `/leads:setup`): folders, README, starter templates, the user's profiles, the offer (the `offer-builder` skill, once), a first campaign (the segment, the platforms and what each one needs, the subreddit check when Reddit is chosen (active subreddits with their rules on promotion and DMs, approved by the user), the disqualifiers), an empty workbook.
- **Update a campaign** (`/leads:update`): add or remove platforms, change a platform's details or the disqualifiers, and re-checks the approved subreddits about once a month; rewrites only those sections, runs no lead search.
- **Find leads** (`/leads:find`, or one platform with `/leads:find-linkedin`, `/leads:find-reddit`, `/leads:find-instagram`): each platform by its own method (LinkedIn by role and company, Reddit by reading the new posts of the day in the approved subreddits (no keywords), Instagram by the bio), 15 at a time, the sources under the stop rule paused first on the user's yes, a compact table scored 1-10 with the disqualifiers applied, every find written to the workbook's To review sheet, then Review and approve: `keep` rows are picked (`pick_leads` counts and unlocks the links), merged into the platform sheet as `to_engage`, and cleared from To review; `skip` rows are excluded; expired rows drop out.
- **Research**: `research_lead` / `research_company` for kept leads the user wants to engage: their posts and comments are what to engage with. People still in preview are picked first; the server refuses their result ids.
- **Engage** (`/leads:engage`): today's leads to engage, a genuine comment suggested per lead that answers what they asked for first (`check_message` stage engage), logged with `interact --by you` once the user posted it.
- **Check who engaged back** (`/leads:check`): `check_lead_activity`, log what they did (`interact --by them`: they become warm), suggest the next comment, ask about messages the check can't see.
- **Answer a lead who wrote**: log it (`--kind message`: talking), help the user reply (template `reply-to-message`), note their goal.
- **Offer for one lead** (`/leads:offer`): the `offer` skill, for interested leads only: suggest a call (`status=meeting`), prepare their offer and the call plan in `offers/`, edited with the user. The offer is presented on the call, never in a message. After it: `record_offer`, `status=offered`, the recap and at most two follow-ups.
- **Today** (`/leads:today`): the review rows marked keep first, then what's due: answers, calls to prepare, follow-ups after a call, engagement.
- **Problems summary** (`/leads:problems`): the problems that came up most on Reddit for a campaign in the last 30 days, grouped and counted from the workbook's Problems sheet, written to `problems/YYYY-MM-DD.md` with content ideas; no name, title, link or handle in it.
- **Topics**: check the phrases in `topics.md` only when the user asks; results go to To review and through Review and approve.
- **Import** (Pro) a spreadsheet the user drops in `imports/`, **export** for a CRM into `exports/`.
- **Forget someone**: `forget_person` on the server and `workbook.py remove` in every workbook in `leads/`.

## Rules that always apply

- Only picked leads go into the platform sheets, and only picked leads count. Every find waits in the workbook's To review sheet as a preview until the user keeps it: never try to find a previewed person's profile another way. Approve the same day: the server deletes results 12 hours after each search and expired review rows drop out.
- Scores are suggestions on fit only: role, company, need, signals, and the campaign's disqualifiers (a match scores 1 or 2 and says which rule). 6 or more fits; a reason for 5 or less starts with `wrong fit:` or `not enough to judge:`, a disqualifier match with `rules out:`. LinkedIn and Instagram score the person; Reddit scores the post, not the poster: the problem it describes and what the poster asks for. The rubric per platform: `references/scoring.md`. Never score on age, gender, nationality, ethnicity, religion, health, family status or photos.
- No private message, DM or email to a lead who hasn't engaged with the user or written to them. If the user asks for one, explain the method and suggest a comment instead.
- Comments never pitch. The offer is presented on a 1:1 call, once the lead is interested; never in a message.
- Every draft goes through `check_message` and follows the writing rules in `references/engagement.md`. Never invent results, numbers or deadlines.
- Report the Apify cost a tool returns in one short line.
- The workbook holds personal data: it stays in the user's folder; don't paste it elsewhere.
