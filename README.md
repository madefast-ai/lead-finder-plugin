# Lead Finder for Claude

**Find the people who need what you sell, right inside Claude.**

Tell Claude what you sell. Lead Finder finds buyers on LinkedIn, Reddit and Instagram, scores each one against your ideal customer, researches the ones you keep, and writes each of them an offer worth answering. Your leads stay in a workbook in a folder on your own computer.

Lead Finder only drafts. It never sends a message, connection request or email for you, and it never uses your social accounts. You review every message and send it yourself.

Website and account: **https://leadfinder.madefast.dev**

---

## What you need

- **A Lead Finder account.** Sign up at [leadfinder.madefast.dev](https://leadfinder.madefast.dev) with your work email. New accounts are approved by us before the first search.
- **An [Apify](https://apify.com) account.** Every search runs on your own Apify account and uses its credit. You paste its API token on your Lead Finder account page once.
- **Claude Desktop with Cowork** for the full experience (the workbook in a folder). Any Claude chat with custom connectors also works, with CSV downloads instead of the workbook.

## Install

### 1. Create your account

1. Go to [leadfinder.madefast.dev](https://leadfinder.madefast.dev) and enter your work email. Type the 6-digit code we email you.
2. Accept the terms and paste your Apify API token (apify.com → Settings → API & Integrations → Personal API tokens).
3. Wait for the approval email. If you were invited, you're approved already.

### 2. Add the plugin to Claude Desktop

1. Open **Customize → Plugins → Add marketplace → Add from a repository**.
2. Enter:
   ```
   madefast-ai/lead-finder-plugin
   ```
3. Install **Lead Finder**.
4. Open the plugin's **Connectors** tab, click **Connect** on **Madefast Lead Finder**, and sign in with the same email.

If Connect stays greyed out, add the connector by hand: **Customize → Connectors → Add custom connector**, name it `Madefast Lead Finder`, URL:
```
https://leadfinder.madefast.dev/mcp
```

### Claude Code

```
/plugin marketplace add madefast-ai/lead-finder-plugin
/plugin install leads@madefast
```
Then run `/mcp`, pick **Madefast Lead Finder** and sign in.

### Any other Claude chat (web, mobile)

**Settings → Connectors → Add custom connector**, name it `Madefast Lead Finder`, URL `https://leadfinder.madefast.dev/mcp`, then **Connect**. Searches, research and offers work the same; the leads you keep come as a CSV download.

## First run

In Cowork, choose a folder for your leads (an empty one is best), then, in this order:

| Step | Type | What happens |
|---|---|---|
| 1 | `/leads:setup` | Claude asks what you sell and who buys it, then creates the folder, templates, your first campaign and its workbook. |
| 2 | `/leads:offer-builder` | Builds your offer with you: the result your buyers want, the problems you solve, real proof and a small first offer. Done once; every message starts from it. |
| 3 | `/leads:find` | Your first search. Every lead comes back scored 1 to 10 with a reason. Keep the ones you like; they go into the workbook. |
| 4 | `/leads:offer` | Pick one lead and get a message shaped for the platform. You copy it and send it yourself. |

## Commands

| Command | Use it to |
|---|---|
| `/leads:setup` | Set up Lead Finder in a new folder. |
| `/leads:offer-builder` | Build or revise your core offer (saved on your account). |
| `/leads:find` | Find new leads for a campaign and save the ones you keep. |
| `/leads:offer` | Write an offer for one lead: LinkedIn note or message, InMail, email, Reddit reply or DM, Instagram DM. |
| `/leads:follow-ups` | See who is due a follow-up and draft the next message for each. |
| `/leads:import` | Bring a CSV or Excel file of leads (a CRM export, an old sheet) into a workbook. |

### Or just ask

You don't need the commands. Plain requests work too:

- "Find heads of ecommerce at UK fashion brands with 50 to 500 people"
- "Who on Reddit is asking for a Shopify agency this month?"
- "Show me the people commenting on this LinkedIn post: [link]"
- "Which companies are hiring a Shopify developer in Germany?"
- "Research Olivia Hart and find her work email"
- "Write Olivia a LinkedIn connection note"
- "Who should I follow up with this week?"
- "Forget this person and never show them again"

## What it can do

**Find**
- LinkedIn people by title, seniority, location, industry and company size, described in plain words.
- Buying signals: LinkedIn posts about the problem, the people commenting on a post, companies hiring for the role you replace, and companies running LinkedIn ads.
- Reddit posts and comments asking for recommendations, by keyword and subreddit.
- Instagram accounts by hashtag or keyword.

**Keep**
- Every lead is scored 1 to 10 against your ideal customer, with a one-line reason.
- People you've already seen stay hidden in later searches and never count against your quota again.
- The leads you keep go into an Excel workbook in your folder, one sheet per platform, plus Summary, Follow-ups and Pipeline sheets that update themselves.

**Research**
- Experience, recent posts, the comments they leave, their company, and a verified work email when you ask for one.

**Write**
- Your offer, built once and saved on your account.
- A tailored offer per lead: their goal in their own words, the objection they're likely to have, and the proof that answers it, shaped for LinkedIn, email, Reddit or Instagram.
- Every draft is checked for length, links, invented numbers, fake urgency, the opt-out line and email consent rules.
- Lead Finder remembers what you pitched, so a colleague at the same company gets a different angle and every follow-up brings something new.
- Eleven starter templates (connection notes, messages, cold emails, follow-ups, Reddit replies and DMs, Instagram DMs) in your folder, yours to edit.

## Your folder

`/leads:setup` creates this in the folder you choose. Everything is plain Markdown plus one workbook per campaign, so you can read and edit it all.

```
README.md            what this folder is
offer.md             your offer (a copy of the one saved on your account)
campaigns/           who you target, one file per campaign
topics.md            phrases to check on Reddit and LinkedIn when you ask
offers/              offer cards for individual leads
templates/           your message templates
leads/               one Excel workbook per campaign
imports/             files to import
exports/             CSV exports
```

In the workbook you can edit status, notes and drafts freely. Lead Finder merges new results by person and never overwrites your columns. Statuses run from `new` and `to_contact` through `contacted`, `replied`, `meeting`, `won` and `lost`, plus `not_interested` and `do_not_contact`.

## Plans and quota

| | Basic | Pro |
|---|---|---|
| New leads per 7 days | 25 | 200 |
| Every feature above | ✓ | ✓ |

Only new people found by a search count. Research, imports and people you've already seen don't. Pro is available only to Pro members of the Skool community; your account page shows how to get it, your plan and what's left this week. Searches use your own Apify credit on both plans.

## Privacy and your data

- **Search results** are kept on the Lead Finder server for **12 hours**, then deleted. Keep the leads you want before then.
- **The leads you keep** live in your folder, on your computer. You're responsible for them: keep them secure, don't share or sell them, and delete people who ask.
- **People you've already seen** are remembered for a year as coded fingerprints (never names) so they aren't shown or counted again.
- **Removal requests:** tell Claude to forget the person. They're deleted from the server and your workbook and never shown to you again.
- **Every first message** should say where you found the person's details and how to opt out. The drafts include this.
- **Your Apify token** is stored encrypted and used only to run your searches.

Full terms: [Terms of Service](https://leadfinder.madefast.dev/terms), [Privacy Policy](https://leadfinder.madefast.dev/privacy), [GDPR and data processing](https://leadfinder.madefast.dev/gdpr).

## Troubleshooting

| Problem | Fix |
|---|---|
| **Connect** is greyed out | Add the connector by hand (see Install), then reconnect from the plugin's Connectors tab. |
| "Your account is waiting for approval" | We approve new accounts by hand; you'll get an email. Your account page shows the status. |
| "No Apify token" | Add it on your [account page](https://leadfinder.madefast.dev/account). |
| A search takes a while | Large searches keep running in the background. Ask Claude to check on it. |
| "Weekly quota used up" | Capacity frees up 7 days after each lead was found. The account page shows when. |
| The workbook isn't created | The workbook needs Cowork with a folder chosen. In other chats, ask for a CSV export. |
| Commands don't appear | Check the plugin is installed and enabled, then start a new Cowork session. |

## Updates

New versions arrive through **Customize → Plugins → Check for updates**, or automatically when sync is on. In Claude Code: `/plugin marketplace update madefast`.

## What's in this repository

```
.claude-plugin/marketplace.json     the marketplace (name: madefast)
leads/
  .claude-plugin/plugin.json        the plugin (name: leads)
  .mcp.json                         the Madefast Lead Finder connector
  skills/
    lead-finder/                    the working method: folder, workbook, workflows, outreach rules,
                                    the workbook script (scripts/workbook.py) and starter templates
    setup/ find/ offer-builder/ offer/ follow-ups/ import/
                                    the /leads:* commands
```

The connector talks to `https://leadfinder.madefast.dev/mcp` and signs you in with OAuth. This repository holds no secrets and no lead data.

## Support

Questions or problems: **hello@madefast.dev**

Lead Finder is built by [Madefast](https://madefast.dev).
