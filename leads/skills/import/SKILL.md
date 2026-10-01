---
name: import
description: Import a CSV or Excel file of leads (a CRM export, a list from a colleague, an older sheet) into a Lead Finder workbook. Use when the user types /leads:import or drops a leads file in the folder.
user-invocable: true
---

Run the **Import a spreadsheet** workflow of the `lead-finder` skill (read its SKILL.md, `references/workflows.md` and `references/workbook.md`).

Look in `imports/` if the user didn't name a file. Ask whether to add to an existing campaign workbook or start a new campaign. Report added, updated and skipped rows.
