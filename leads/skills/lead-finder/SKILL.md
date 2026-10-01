---
name: lead-finder
description: Lead Finder's working method in a folder on the user's computer. Use whenever the user wants to find leads or prospects (LinkedIn, Reddit, Instagram), keep or pick leads, save them to their lead workbook, research a lead, draft outreach or follow-ups, update a lead's status, see follow-ups due, import or export a leads spreadsheet, check saved topics, or remove a person. Works with the Lead Finder connector (tools such as my_account, search_linkedin_people, get_results).
---

# Lead Finder

Lead Finder finds B2B leads through the user's own Apify account. The **server** keeps search results for 12 hours only. **Everything else lives in the user's folder**: what they sell, campaigns, saved topics, templates, and one workbook per campaign with every lead, status, follow-up, note and draft. You do the file work; the connector does the searching.

Never send anything and never use the user's social accounts. The user contacts people themselves.

## Before anything else

1. Call `my_account`, then `get_offer`: the user's offer is saved on the server. Never ask them to explain their business again when it exists. If the tool doesn't exist, the connector isn't connected: tell the user to open the plugin's Connectors tab (or Customize → Connectors → Add custom connector with `https://leadfinder.madefast.dev/mcp`) and sign in, then stop.
2. Handle what it says: waiting for approval (searches won't run yet; setup still works), no Apify token (the account page, or `set_api_key` if they paste it), terms to accept (the link it gives). Say **Basic** and **Pro**, never free and paid.
3. Find the Lead Finder folder: the working folder if it has `offer.md` and `leads/`; otherwise ask where it is, or run the setup workflow.

## The folder

Read `references/folder.md` for the layout and the formats of `offer.md`, campaign files, `topics.md` and templates. In short:

```
offer.md                a mirror of the saved offer (the server keeps the original)
campaigns/<slug>.md     one ideal-customer segment for the offer, the angle, the searches that work
topics.md               saved phrases to check on demand, per platform
templates/*.md          message templates (starter pack + the user's own + ones from other tools)
offers/<lead-key>.md    offer cards for individual leads
leads/<slug>.xlsx       the workbook of that campaign
imports/  exports/      files in and out
```

## The workbook

One `.xlsx` per campaign with sheets **LinkedIn**, **Companies**, **Reddit**, **Instagram** (the source of truth) and **Summary**, **Follow-ups**, **Pipeline** (rebuilt automatically, never edit them). Always change it through the script, so merges never lose the user's work:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/lead-finder/scripts/workbook.py" <command> leads/<slug>.xlsx ...
```

If `${CLAUDE_PLUGIN_ROOT}` isn't set, find `workbook.py` in this skill's `scripts/` folder. If openpyxl is missing, `pip install openpyxl`. Commands, columns and statuses: `references/workbook.md`. Close the file in Excel first if the script says it can't write.

## Workflows

Details for each are in `references/workflows.md`. Load it when you run one.

- **Set up** (first time, or `/leads:setup`): folders, README, starter templates, the offer (the `offer-builder` skill, once), a first campaign, an empty workbook.
- **Find leads**: read `offer.md` and the campaign; choose the warmest source that fits (posts and questions before cold lists); run the search; show a compact table scored 1-10 with a one-line reason; ask which to keep; `pick_leads` (and `exclude_leads` for clear misfits); `get_results`; add your scores to those rows; `workbook.py merge`. Tell the user the quota line from the result.
- **Research** the leads the user will contact: `research_lead` / `research_company`, then `get_results` and merge again (research columns fill in; the user's columns stay).
- **Offer for one lead** (`/leads:offer`): the `offer` skill. `tailor_offer` → offer card and message for the platform → `check_offer` → save to the row and `offers/` → `record_offer`, so nothing repeats.
- **Draft** from a template: pick a template with the user (ask, don't choose for them), write one draft per lead into `draft_first_message` with `workbook.py update`, run `check_offer` on it. Follow `references/outreach.md` every time.
- **Log what happened**: "I sent it", "she replied", "not interested" → `workbook.py update KEY status=...` (contacted sets a follow-up in 4 days).
- **Follow-ups** (`/leads:follow-ups`): `workbook.py due --days 1`, draft the next message for each, update after the user sends.
- **Topics**: check the phrases in `topics.md` only when the user asks; results go through the same pick step.
- **Import** a spreadsheet the user drops in `imports/`, **export** for a CRM into `exports/`.
- **Forget someone**: `forget_person` on the server and `workbook.py remove` in every workbook in `leads/`.

## Rules that always apply

- Only picked leads go into the workbook. Excluded ones stay out (the user can see them again with `get_results` state excluded, until the 12 hours pass).
- Save picked leads to the workbook in the same session: the server deletes results 12 hours after each search.
- Scores are suggestions on fit only: role, company, need, signals. Never score on age, gender, nationality, ethnicity, religion, health, family status or photos.
- Every first message says where the details came from and how to opt out (see `references/outreach.md`). Set `data_source_note_sent=yes` when a draft includes it.
- Cold email needs prior consent in some countries (for example Romania and Germany): prefer LinkedIn there, and warn before drafting an email.
- Report the Apify cost a tool returns in one short line.
- The workbook holds personal data: it stays in the user's folder; don't paste it elsewhere.
