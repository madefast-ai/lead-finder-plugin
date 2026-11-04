# Lead Finder for Claude

**Find the people who need what you sell, right inside Claude.**

Tell Claude what you sell. Lead Finder finds people who need it on LinkedIn, Reddit and Instagram and scores each one against your ideal customer. You engage with them in public, by hand: Claude suggests genuine comments on their posts and tracks who engaged back. When someone is interested, you book a call, and Claude prepares their offer for it, with the exact scope and price, from the offer you built once. Your leads stay in a workbook in a folder on your own computer.

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

1. Open **More → Customize → Plugins**, click **+ Add** and choose **Add marketplace → Add from a repository**.
2. Enter:
   ```
   madefast-ai/lead-finder-plugin
   ```
3. Install **Lead Finder**.
4. Open the plugin's **Connectors** tab, click **Connect** on **Madefast Lead Finder**, and sign in with the same email.

If Connect stays greyed out, add the connector by hand: **More → Customize → Connectors**, add a custom connector named `Madefast Lead Finder` with the URL:
```
https://leadfinder.madefast.dev/mcp
```

### Claude Code

```
/plugin marketplace add madefast-ai/lead-finder-plugin
/plugin install leads@leadfinder
```
Then run `/mcp`, pick **Madefast Lead Finder** and sign in.

### Any other Claude chat (web, mobile)

**Settings → Connectors → Add custom connector**, name it `Madefast Lead Finder`, URL `https://leadfinder.madefast.dev/mcp`, then **Connect**. Searches, research and offers work the same; the leads you keep come as a CSV download.

## How it works

1. **Find.** Ask for leads in plain words. People who post and comment about the problem come first, because they're the ones you can engage with.
2. **Engage.** Comment on their posts, answer their questions, react, follow. Claude suggests a comment that adds something (never a pitch), and you post it yourself.
3. **Warm.** When they reply, comment on your posts or react, they're warm. Claude checks for you and logs it.
4. **Talk.** When they write to you, you're in a conversation. Claude helps you answer what they said.
5. **Call.** When they're interested, suggest a short call. Claude prepares their offer from yours (what's included for them, the price, the timeline) and the plan for the call. You present it on the call, and Claude writes the recap afterwards.

## First run

In Claude Desktop, switch the box to **Cowork**, click **Project or folder** and add a folder for your leads (**Add folder**; an empty one is best), then, in this order:

| Step | Type | What happens |
|---|---|---|
| 1 | `/leads:setup` | Claude asks what you sell, who buys it, which platforms to search and what each one needs, and when Reddit is one of them, which subreddits to approve (Claude checks they are active and reads their rules), what rules a lead out, and your own profile links, then creates the folder, templates, your first campaign and its workbook. |
| 2 | `/leads:offer-builder` | An interview for your exact offer: what's included and for how long, the price and terms, proof, guarantee, a bigger anchor version and what to offer after a no. Done once. |
| 3 | `/leads:find` | Your first search. Every lead comes back scored 1 to 10 with a reason and waits in your workbook's To review sheet. Mark the ones you like keep; they go into the platform's sheet with their links. |
| 4 | `/leads:engage` | Today's leads to engage with, each with a post and a suggested comment. You post them yourself and tell Claude. |

## Commands

| Command | Use it to |
|---|---|
| `/leads:setup` | Set up Lead Finder in a new folder. |
| `/leads:update` | Change a campaign: add or remove a platform, change what it looks for there, the rules that rule a lead out, and re-check your approved subreddits. |
| `/leads:offer-builder` | Build or revise your offer (saved on your account). |
| `/leads:find` | Finds new leads for a campaign 15 at a time, each platform by its own method, scores them from 1 to 10 into your workbook's To review sheet, saves the ones you keep, and asks to pause the sources that give fewer than 3 good leads a week. |
| `/leads:find-linkedin` | LinkedIn leads by role and company. |
| `/leads:find-reddit` | The new posts of the last 24 hours in the subreddits you approved, read by Claude for the ones where someone describes a problem you solve. No keywords. |
| `/leads:find-instagram` | Instagram accounts whose bio contains your bio words, each bio checked against what a good bio shows. |
| `/leads:engage` | Get today's leads to engage with and a comment for each; log what you did. |
| `/leads:check` | See who engaged back: replies to your comments, comments on your posts and comments where you engaged on LinkedIn, Reddit and Instagram, reactions to your posts on LinkedIn, and their new posts. |
| `/leads:offer` | For a lead who's interested: suggest a call, prepare their offer for it, then the recap and follow-ups. |
| `/leads:today` | What's due today: who to answer, calls to prepare, follow-ups after a call, who to engage again. |
| `/leads:problems` | The problems that came up most in the Reddit posts Claude read for a campaign in the last 30 days, in the posters' own words, with what they asked for: material for your own posts and for comments on LinkedIn and Instagram. No names or links. |
| `/leads:import` | Bring a CSV or Excel file of leads (a CRM export, an old sheet) into a workbook. Pro only. |

### Or just ask

- "Find heads of ecommerce at UK fashion brands who posted about their store this month"
- "Who on Reddit is asking for a Shopify agency right now?"
- "Show me the people commenting on this LinkedIn post: [link]"
- "I commented on Olivia's post about drop days"
- "Did anyone engage back this week?"
- "Olivia messaged me, she's asking what a rebuild would cost"
- "Olivia booked a call for Thursday. Prepare her offer, without the monitoring"
- "I offered Olivia the rebuild on the call, write the recap"
- "Forget this person and never show them again"

## What it can do

**Find**
- Only the platforms you chose for a campaign, each with its own method: LinkedIn by role and company, Reddit by the problems in your customers' own words, Instagram by what's in the bio. Your disqualifiers are applied to every score.
- A command per platform, each with its own method, or `/leads:find` for all of them. Every find waits in the workbook's To review sheet, without links, until you mark it keep or skip; only kept leads are saved and counted, and expired ones drop out after 12 hours. Searches run 15 at a time. Every run is counted per source (subreddit, bio word, LinkedIn search) in the workbook's Sources sheet, and a source that gives fewer than 3 good leads from 10 or more results in a week is paused or retired, with your yes.
- LinkedIn people by title, seniority, location, industry and company size, described in plain words.
- Buying signals: LinkedIn posts about the problem, the people commenting on a post, companies hiring for the role you replace, and companies running LinkedIn ads.
- Reddit: every day, the new posts of the last 24 hours in subreddits you approved after Claude checked they are active (members, weekly visitors, weekly contributions, newest post) and read their rules on promotion and private messages. Claude reads them and picks the ones where someone describes a problem you solve, no keywords; a keyword search of the last 48 hours when you ask for a phrase.
- Instagram accounts whose bio contains your bio words (a web search of Instagram profiles, then each profile read in full; accounts whose bio has none of the words are left out), and posts from the last 72 hours by hashtag or keyword.
- Every lead scored 1 to 10 against your ideal customer, with a one-line reason: 6 or more fits, and a lower score says whether it's a wrong fit or there wasn't enough to judge. On Reddit the score is about the post: the problem it describes and what the poster asks for. People you've kept stay hidden for a year and never count twice; results are previews until you keep someone, and only the people you keep count.

**Engage**
- Suggested comments that add something to their post, checked so they never pitch.
- A log of every interaction, yours and theirs, and the next date to engage.
- An activity check: their new posts, and whether they commented on your posts, replied to your comments or commented where you did on LinkedIn, Reddit and Instagram, or reacted to your posts on LinkedIn.

**Offer**
- Your offer, built once with an interview: what's included with durations, the price and terms, real proof, the guarantee, an anchor, a payment plan and a feature downsell.
- The offer for one lead, for your call with them: adapted scope, price and timeline, and the call plan (the anchor, then their offer, and what to suggest after a no), edited with you and saved to your folder. The offer and the price never go in a message before the call.
- After the call: the recap, and at most two follow-ups if they haven't decided.
- Remembers what you offered, so follow-ups and offers to colleagues at the same company bring something new.

**Keep**
- An Excel workbook per campaign, one sheet per platform, a To review sheet for the finds waiting for your decision, a Sources sheet with how each source did, a Problems sheet with the problem, the ask and a short phrase of every fitting Reddit post (no usernames, titles or links), plus Summary, Next touches and Pipeline sheets that update themselves.
- Eight starter templates (comments, a connection request, a reply, suggesting a call, a call recap, a follow-up after the call), yours to edit.

## Your folder

`/leads:setup` creates this in the folder you choose. Everything is plain Markdown plus one workbook per campaign, so you can read and edit it all.

```
README.md            what this folder is
offer.md             your offer (a copy of the one saved on your account)
campaigns/           who you target, one file per campaign: the platforms to search, what each looks for, what rules a lead out
topics.md            phrases to check on Reddit and LinkedIn when you ask
offers/              the offer and call plan for each lead you have a call with
templates/           your comment, reply and recap templates
leads/               one Excel workbook per campaign
problems/            the roundups of what came up most on Reddit, for your own content
imports/             files to import
exports/             CSV exports
```

Statuses run `new` → `to_engage` → `engaging` → `warm` → `talking` → `meeting` → `offered` → `won` or `lost`, plus `not_interested` and `do_not_contact`. You can edit status, notes and drafts freely; Lead Finder merges new results by person and never overwrites your columns.

## Plans and quota

| | Basic | Pro |
|---|---|---|
| New leads per 7 days | 25 | 200 |
| Find, engage, check and offer for the leads it finds | ✓ | ✓ |
| Your own lead lists (import, research, checks, offers) | | ✓ |
| Saved offers, one per product or segment | 1 | Unlimited |
| Ready-made playbooks | | ✓ |

Only the people you keep count. Looking through results, research, activity checks, imports and people you've already kept don't. You can set a weekly limit per platform on your account page or by asking Claude. Importing your own lists, and research, checks and offers for people Lead Finder didn't find for you, are Pro features. One Lead Finder account per Apify token on every plan: a token saved on one account can't be added to another until it's removed there. Pro is available only to Pro members of the Skool community; your account page shows how to get it, your plan and what's left this week. Searches and checks use your own Apify credit on both plans.

## Privacy and your data

- **Search results** are kept on the Lead Finder server for **12 hours**, then deleted. Keep the leads you want before then.
- **The leads you keep** live in your folder, on your computer. You're responsible for them: keep them secure, don't share or sell them, and delete people who ask.
- **People you've kept** are remembered for a year as coded fingerprints (never names) so they aren't shown or counted again, and, on Basic, to tell which people Lead Finder found for you.
- **Removal requests:** tell Claude to forget the person. They're deleted from the server and your workbook and never shown to you again.
- **Your privacy notice:** you collect people's public details, so keep a short privacy notice (a link on your profile or website is enough).
- **Your Apify token** is stored encrypted (with a keyed fingerprint so it stays on one account) and used only to run your searches and checks.

Full terms: [Terms of Service](https://leadfinder.madefast.dev/terms), [Privacy Policy](https://leadfinder.madefast.dev/privacy), [GDPR and data processing](https://leadfinder.madefast.dev/gdpr).

## Troubleshooting

| Problem | Fix |
|---|---|
| **Connect** is greyed out | Add the connector by hand (see Install), then reconnect from the plugin's Connectors tab. |
| "Your account is waiting for approval" | We approve new accounts by hand; you'll get an email. Your account page shows the status. |
| "No Apify token" | Add it on your [account page](https://leadfinder.madefast.dev/account). |
| The check doesn't see comments on my posts or replies to my comments | Tell Claude your LinkedIn profile link, your Reddit username and your Instagram handle once (it saves them with your account). The check needs them to see comments and reactions on your own posts, and replies to your comments on Reddit and Instagram. |
| A search takes a while | Large searches keep running in the background. Ask Claude to check on it. |
| "Weekly quota used up" | Capacity frees up 7 days after each lead was kept. The account page shows when, and where you can raise a platform's weekly limit. |
| The workbook isn't created | The workbook needs Cowork with your folder chosen under **Project or folder**. In other chats, ask for a CSV export. |
| Commands don't appear | Check the plugin is installed and enabled, then start a new Cowork session. |

## Updates

New versions arrive when you update the plugin from **Plugins** in Claude Desktop (More → Customize → Plugins), or automatically when sync is on. In Claude Code: `/plugin marketplace update leadfinder`.

## What's in this repository

```
.claude-plugin/marketplace.json     the marketplace (name: leadfinder)
leads/
  .claude-plugin/plugin.json        the plugin (name: leads)
  .mcp.json                         the Madefast Lead Finder connector
  skills/
    lead-finder/                    the working method: folder, workbook, workflows, engagement rules,
                                    the workbook script (scripts/workbook.py) and starter templates
    setup/ update/ find/ find-linkedin/ find-reddit/ find-instagram/ engage/ check/ offer-builder/ offer/ today/ problems/ import/
                                    the /leads:* commands
```

This repository is also the plugin marketplace (`.claude-plugin/marketplace.json`, named `leadfinder`). The connector talks to `https://leadfinder.madefast.dev/mcp` and signs you in with OAuth. This repository holds no secrets and no lead data.

## Support

Questions or problems: **hello@madefast.dev**

Lead Finder is built by [Madefast](https://madefast.dev).
