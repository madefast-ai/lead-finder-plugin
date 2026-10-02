# Lead Finder for Claude

**Find the people who need what you sell, right inside Claude.**

Tell Claude what you sell. Lead Finder finds people who need it on LinkedIn, Reddit and Instagram and scores each one against your ideal customer. You engage with them in public, by hand: Claude suggests genuine comments on their posts and tracks who engaged back. When someone is interested, Claude creates their offer, with the exact scope and price, from the offer you built once. Your leads stay in a workbook in a folder on your own computer.

Lead Finder never reaches anyone cold and never sends anything for you. You comment, connect and write from your own accounts; Claude drafts, checks and keeps track.

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

## How it works

1. **Find.** Ask for leads in plain words. People who post and comment about the problem come first, because they're the ones you can engage with.
2. **Engage.** Comment on their posts, answer their questions, react, follow. Claude suggests a comment that adds something (never a pitch), and you post it yourself.
3. **Warm.** When they reply, comment on your posts or react, they're warm. Claude checks for you and logs it.
4. **Talk.** When they write to you, you're in a conversation. Claude helps you answer what they said.
5. **Offer.** When they're interested, Claude creates their offer from yours: what's included for them, the price, the timeline. You edit it and send it.

## First run

In Cowork, choose a folder for your leads (an empty one is best), then, in this order:

| Step | Type | What happens |
|---|---|---|
| 1 | `/leads:setup` | Claude asks what you sell, who buys it and your own profile links, then creates the folder, templates, your first campaign and its workbook. |
| 2 | `/leads:offer-builder` | An interview for your exact offer: what's included and for how long, the price and terms, proof, guarantee, a bigger anchor version and what to offer after a no. Done once. |
| 3 | `/leads:find` | Your first search. Every lead comes back scored 1 to 10 with a reason. Keep the ones you like; they go into the workbook. |
| 4 | `/leads:engage` | Today's leads to engage with, each with a post and a suggested comment. You post them yourself and tell Claude. |

## Commands

| Command | Use it to |
|---|---|
| `/leads:setup` | Set up Lead Finder in a new folder. |
| `/leads:offer-builder` | Build or revise your offer (saved on your account). |
| `/leads:find` | Find new leads for a campaign and save the ones you keep. |
| `/leads:engage` | Get today's leads to engage with and a comment for each; log what you did. |
| `/leads:check` | See who engaged back: replies, comments and reactions on your posts, their new posts. |
| `/leads:offer` | Create the offer for a lead who's interested, edit it, and write the message. |
| `/leads:today` | What's due today: who to answer, offers to follow up, who to engage again. |
| `/leads:import` | Bring a CSV or Excel file of leads (a CRM export, an old sheet) into a workbook. |

### Or just ask

- "Find heads of ecommerce at UK fashion brands who posted about their store this month"
- "Who on Reddit is asking for a Shopify agency this month?"
- "Show me the people commenting on this LinkedIn post: [link]"
- "I commented on Olivia's post about drop days"
- "Did anyone engage back this week?"
- "Olivia messaged me, she's asking what a rebuild would cost"
- "Create Olivia's offer, but without the monitoring"
- "Forget this person and never show them again"

## What it can do

**Find**
- LinkedIn people by title, seniority, location, industry and company size, described in plain words.
- Buying signals: LinkedIn posts about the problem, the people commenting on a post, companies hiring for the role you replace, and companies running LinkedIn ads.
- Reddit posts and comments asking for recommendations, by keyword and subreddit.
- Instagram accounts by hashtag or keyword.
- Every lead scored 1 to 10 against your ideal customer, with a one-line reason. People you've already seen stay hidden and never count against your quota again.

**Engage**
- Suggested comments that add something to their post, checked so they never pitch.
- A log of every interaction, yours and theirs, and the next date to engage.
- An activity check: their new posts, and whether they commented on or reacted to your LinkedIn posts or replied where you commented.

**Offer**
- Your offer, built once with an interview: what's included with durations, the price and terms, real proof, the guarantee, an anchor, a payment plan and a feature downsell.
- The offer for one lead: adapted scope, price and timeline, edited with you, saved to your folder, with the message that presents it.
- Remembers what you offered, so follow-ups and offers to colleagues at the same company bring something new.

**Keep**
- An Excel workbook per campaign, one sheet per platform, plus Summary, Next touches and Pipeline sheets that update themselves.
- Eight starter templates (comments, a connection request, a reply, the offer, a follow-up after an offer, a call recap), yours to edit.

## Your folder

`/leads:setup` creates this in the folder you choose. Everything is plain Markdown plus one workbook per campaign, so you can read and edit it all.

```
README.md            what this folder is
offer.md             your offer (a copy of the one saved on your account)
campaigns/           who you target, one file per campaign
topics.md            phrases to check on Reddit and LinkedIn when you ask
offers/              the offer you sent each lead
templates/           your comment, reply and offer templates
leads/               one Excel workbook per campaign
imports/             files to import
exports/             CSV exports
```

Statuses run `new` → `to_engage` → `engaging` → `warm` → `talking` → `offer_sent` → `meeting` → `won` or `lost`, plus `not_interested` and `do_not_contact`. You can edit status, notes and drafts freely; Lead Finder merges new results by person and never overwrites your columns.

## Plans and quota

| | Basic | Pro |
|---|---|---|
| New leads per 7 days | 25 | 200 |
| Every feature above | ✓ | ✓ |
| Ready-made routines | | ✓ |

Only new people found by a search count. Research, activity checks, imports and people you've already seen don't. Pro is available only to Pro members of the Skool community; your account page shows how to get it, your plan and what's left this week. Searches and checks use your own Apify credit on both plans.

## Privacy and your data

- **Search results** are kept on the Lead Finder server for **12 hours**, then deleted. Keep the leads you want before then.
- **The leads you keep** live in your folder, on your computer. You're responsible for them: keep them secure, don't share or sell them, and delete people who ask.
- **People you've already seen** are remembered for a year as coded fingerprints (never names) so they aren't shown or counted again.
- **Removal requests:** tell Claude to forget the person. They're deleted from the server and your workbook and never shown to you again.
- **Your privacy notice:** you collect people's public details, so keep a short privacy notice (a link on your profile or website is enough).
- **Your Apify token** is stored encrypted and used only to run your searches and checks.

Full terms: [Terms of Service](https://leadfinder.madefast.dev/terms), [Privacy Policy](https://leadfinder.madefast.dev/privacy), [GDPR and data processing](https://leadfinder.madefast.dev/gdpr).

## Troubleshooting

| Problem | Fix |
|---|---|
| **Connect** is greyed out | Add the connector by hand (see Install), then reconnect from the plugin's Connectors tab. |
| "Your account is waiting for approval" | We approve new accounts by hand; you'll get an email. Your account page shows the status. |
| "No Apify token" | Add it on your [account page](https://leadfinder.madefast.dev/account). |
| The check doesn't see reactions to my posts | Tell Claude your LinkedIn profile link once (it saves it with your account). |
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
    lead-finder/                    the working method: folder, workbook, workflows, engagement rules,
                                    the workbook script (scripts/workbook.py) and starter templates
    setup/ find/ engage/ check/ offer-builder/ offer/ today/ import/
                                    the /leads:* commands
```

The connector talks to `https://leadfinder.madefast.dev/mcp` and signs you in with OAuth. This repository holds no secrets and no lead data.

## Support

Questions or problems: **hello@madefast.dev**

Lead Finder is built by [Madefast](https://madefast.dev).
