---
name: import
description: Import a CSV or Excel file of leads (a CRM export, a list from a colleague, an older sheet) into a Lead Finder workbook. Pro only. Use when the user types /leads:import or drops a leads file in the folder.
user-invocable: true
---

Call `my_account` first. If `features.own_leads` is false (the Basic plan), say that importing your own lead lists is a Pro feature, that on Basic Lead Finder works with the people it finds for you, point at the account page (`account_page`, and the `pro` line says how to get Pro), and stop: don't read the file and don't run `workbook.py import`. If `my_account` doesn't exist, the connector isn't connected (see the lead-finder skill) and stop. Say Basic and Pro, never anything else for the plans.

Otherwise run the **Import a spreadsheet** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/workbook.md`).

Look in `imports/` if the user didn't name a file. Ask whether to add to an existing campaign workbook or start a new campaign. Report added, updated and skipped rows.
