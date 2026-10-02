---
name: lead-finder
description: Lead Finder's working method in a folder on the user's computer. Use whenever the user wants to find leads or prospects (LinkedIn, Reddit, Instagram), keep or pick leads, save them to their lead workbook, research a lead, engage with leads (comments, reactions), log an interaction ("I commented on…", "she replied"), check who engaged back, answer a lead who wrote to them, create an offer for a lead, see what's due today, import or export a leads spreadsheet, check saved topics, or remove a person. Works with the Lead Finder connector (tools such as my_account, search_linkedin_people, get_results, check_lead_activity).
---

# Lead Finder

Lead Finder finds B2B leads through the user's own Apify account and helps turn them into conversations. The **server** keeps search results for 12 hours only. **Everything else lives in the user's folder**: what they sell, campaigns, saved topics, templates, the offers sent, and one workbook per campaign with every lead's status, interaction log, notes and drafts. You do the file work; the connector does the searching.

**Never reach someone who hasn't interacted with the user.** The user engages in public first (genuine comments, reactions, a connection request without a pitch); private messages, DMs and email only once the lead has engaged back or written; the offer only once they're interested. Never send anything and never use the user's social accounts: the user does every interaction themselves, and tells you so you can log it. Details: `references/engagement.md`.

## Before anything else

1. Call `my_account`, then `get_offer`: the user's offer is saved on the server. Never ask them to explain their business again when it exists. If the tool doesn't exist, the connector isn't connected: tell the user to open the plugin's Connectors tab (or Customize → Connectors → Add custom connector with `https://leadfinder.madefast.dev/mcp`) and sign in, then stop.
2. Handle what it says: waiting for approval (searches won't run yet; setup still works), no Apify token (the account page, or `set_api_key` if they paste it), terms to accept (the link it gives), no `my_profiles` (ask for their LinkedIn link, Reddit username, Instagram handle: `set_my_profiles`). Say **Basic** and **Pro**, never free and paid.
3. Find the Lead Finder folder: the working folder if it has `offer.md` and `leads/`; otherwise ask where it is, or run the setup workflow.

## The folder

Read `references/folder.md` for the layout and the formats of `offer.md`, campaign files, `topics.md`, templates and `offers/`. In short:

```
offer.md                a mirror of the saved offer (the server keeps the original)
campaigns/<slug>.md     one ideal-customer segment, where they talk, the searches that work
topics.md               saved phrases to check on demand, per platform
templates/*.md          comment, reply and offer templates
offers/<lead-key>.md    the offer for one lead, as sent
leads/<slug>.xlsx       the workbook of that campaign
imports/  exports/      files in and out
```

## The workbook

One `.xlsx` per campaign with sheets **LinkedIn**, **Companies**, **Reddit**, **Instagram** (the source of truth) and **Summary**, **Next touches**, **Pipeline** (rebuilt automatically, never edit them). Always change it through the script:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py" <command> leads/<slug>.xlsx ...
```

If `${CLAUDE_PLUGIN_ROOT}` isn't set, find `workbook.py` in this skill's `scripts/` folder. If openpyxl is missing, `pip install openpyxl`. Statuses: new → to_engage → engaging → warm → talking → offer_sent → meeting → won / lost (plus not_interested, do_not_contact). Commands and columns: `references/workbook.md`. Close the file in Excel first if the script says it can't write.

## Workflows

Details for each are in `references/workflows.md`. Load it when you run one.

- **Set up** (first time, or `/leads:setup`): folders, README, starter templates, the user's profiles, the offer (the `offer-builder` skill, once), a first campaign, an empty workbook.
- **Find leads** (`/leads:find`): the warmest source that fits (people posting and commenting first), a compact table scored 1-10, the user picks, `pick_leads`, `get_results`, merge, status `to_engage`.
- **Research**: `research_lead` / `research_company` for leads the user wants to engage: their posts and comments are what to engage with.
- **Engage** (`/leads:engage`): today's leads to engage, a genuine comment suggested per lead (`check_message` stage engage), logged with `interact --by you` once the user posted it.
- **Check who engaged back** (`/leads:check`): `check_lead_activity`, log what they did (`interact --by them`: they become warm), suggest the next comment, ask about messages the check can't see.
- **Answer a lead who wrote**: log it (`--kind message`: talking), help the user reply (template `reply-to-message`), note their goal.
- **Offer for one lead** (`/leads:offer`): the `offer` skill, for warm or talking leads only: their offer in `offers/`, edited with the user, then the message, `record_offer`, `status=offer_sent`.
- **Today** (`/leads:today`): what's due: answers, offer follow-ups, engagement, calls.
- **Topics**: check the phrases in `topics.md` only when the user asks; results go through the same pick step.
- **Import** a spreadsheet the user drops in `imports/`, **export** for a CRM into `exports/`.
- **Forget someone**: `forget_person` on the server and `workbook.py remove` in every workbook in `leads/`.

## Rules that always apply

- Only picked leads go into the workbook. Save them in the same session: the server deletes results 12 hours after each search.
- Scores are suggestions on fit only: role, company, need, signals. Never score on age, gender, nationality, ethnicity, religion, health, family status or photos.
- No private message, DM or email to a lead who hasn't engaged with the user or written to them. If the user asks for one, explain the method and suggest a comment instead.
- Comments never pitch. The offer comes only when the lead is interested.
- Every draft goes through `check_message` and follows the writing rules in `references/engagement.md`. Never invent results, numbers or deadlines.
- Report the Apify cost a tool returns in one short line.
- The workbook holds personal data: it stays in the user's folder; don't paste it elsewhere.
