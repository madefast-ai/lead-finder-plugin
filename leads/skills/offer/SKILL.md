---
name: offer
description: Prepare the offer for one lead who is talking with the user and interested - suggest a short call, then start from the saved offer and adapt what's included, the price and the timeline to them for that call, with the call plan, let the user edit it and save it to offers/. After the call, record what was offered, write the recap and at most two follow-ups. The offer is presented on a 1:1 call, never in a message. Use when the user types /leads:offer, says a lead asked about their work, the price or availability, booked a call, or had one.
user-invocable: true
---

# The offer for one lead

The offer is presented on a 1:1 call, never in a message. Only for leads who are talking with the user and interested: status `talking`, `meeting` or `offered` in the workbook. If the lead is `new`, `to_engage`, `engaging` or `warm`, don't prepare an offer: explain that Lead Finder offers only on a call with people who are already talking with the user, and suggest engaging first (`/leads:engage`) or answering what they wrote.

Start from the saved offer (never ask the user to re-explain their business) and what the lead said. Use the `lead-finder` skill for the workbook and `references/engagement.md` there for the writing rules.

## 1. They're interested: suggest a call

When a lead who's talking asks about the work, the cost or availability, help the user answer what they can and suggest a 30-minute call (template `suggest-a-call`). No price and no offer in writing. Run `check_message` (stage `conversation`) and fix every error. When the call is booked: `workbook.py update <key> status=meeting next_touch=<call date>`.

## 2. Before the call: their offer and the call plan

1. **The offer.** `get_offer`. If there's none, run the `offer-builder` skill first (once). If there are several, pick the one for this lead's campaign, or ask.
2. **The lead and the conversation.** Read their row: the interaction log, notes, research. Ask the user what the lead said if it isn't there: their goal, their question, what's in the way. Their words drive the offer.
3. **Brief.** `tailor_offer` with the lead's status, the channel you're talking on in writing, stage `call` and the lead (link or key, name, role, company, interactions, conversation, notes). It returns the whole saved offer, the objection to expect and what answers it, and what was already offered to them or their company.
4. **Draft their offer and the call plan** and show it (the format is in `references/folder.md`, `offers/<lead-key>.md`):
   - their goal, in their words;
   - what's included for them: the parts that fit, adapted, each with how long it runs;
   - the price and how they pay (the saved price unless the user changes it);
   - timeline: when it starts and what happens first;
   - the one proof point closest to their situation, and the guarantee if there is one;
   - the call plan: their goal first, the anchor, then their offer, then stop; the objection to expect and what answers it; after a no, "Is it the total, or paying it all at once?" → Option A or Option B → the fallback.
5. **Edit with the user.** Ask what to change for this lead: scope, price, timeline, what to leave out. Update the draft until they're happy. If the price changes, keep it consistent (Option A's payments, Option B).
6. **Save** `offers/<lead-key>.md`. Nothing goes to the lead before the call.

## 3. After the call

1. Ask how it went: what they offered (the main offer, Option A or Option B), the price, what the lead said, the next step.
2. `record_offer` (channel, angle, what was offered, the price, the proof, the lead's link and company). Then `workbook.py update <key> status=offered offer_price=<price> offer_file=offers/<file>`, or `won`, `lost`, `not_interested`. Add what was said to the offer file.
3. **The recap.** `tailor_offer` with stage `recap`, then the recap (template `call-recap`): their goal in their words, what was offered or the option they chose, the price, the timeline and the next step with a date. `check_message` (stage `recap`). The user sends it themselves, the same day.

## Follow-up after the call (stage `follow_up`)

When they haven't decided: `tailor_offer` with stage `follow_up` shows what was already offered. One new, useful thing (a relevant result, an answer to a question they raised on the call, a timing detail) and an easy way to say "not now" (template `offer-follow-up`). At most two follow-ups; then pause or close.

## Rules

- The offer and the price are for the call. Before it, in writing: only the answer to what they asked and the call suggestion.
- Only facts from the saved offer and what the lead said. Never invent results, numbers, limits or deadlines.
- One idea and one ask per message.
- Never lower the price of the same thing; change how they pay or remove parts.
- Nothing is sent from here: the user sends it and then says so.
