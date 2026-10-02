---
name: offer
description: Create the offer for one lead who is already talking with the user and interested - start from the saved offer, adapt what's included, the price and the timeline to them, let the user edit it, save it to offers/, then write the message that presents it on the channel they're talking on. Also follow-ups after an offer and call plans. Use when the user types /leads:offer, or says a lead asked about their work, the price or availability.
user-invocable: true
---

# The offer for one lead

Only for leads who have engaged with the user and are interested: status `warm`, `talking`, `offer_sent` or `meeting` in the workbook. If the lead is `new`, `to_engage` or `engaging`, don't write an offer: explain that Lead Finder offers only to people who are already talking with the user, and suggest engaging first (`/leads:engage`).

Start from the saved offer (never ask the user to re-explain their business) and what the lead said. Use the `lead-finder` skill for the workbook and `references/engagement.md` there for the writing rules.

## Steps

1. **The offer.** `get_offer`. If there's none, run the `offer-builder` skill first (once). If there are several, pick the one for this lead's campaign, or ask.
2. **The lead and the conversation.** Read their row: the interaction log, notes, research. Ask the user what the lead said if it isn't there: their goal, their question, what's in the way. Their words drive the offer.
3. **Brief.** `tailor_offer` with the lead's status, the channel they're talking on, the stage (`offer`, `follow_up` or `call`) and the lead (link or key, name, role, company, interactions, conversation, notes). It returns the whole saved offer, the objection to expect and what answers it, and what was already offered to them or their company.
4. **Draft their offer** and show it (the format is in `references/folder.md`, `offers/<lead-key>.md`):
   - their goal, in their words;
   - what's included for them: the parts that fit, adapted, each with how long it runs;
   - the price and how they pay (the saved price unless the user changes it);
   - timeline: when it starts and what happens first;
   - the one proof point closest to their situation, and the guarantee if there is one;
   - the next step;
   - for the call: the anchor, Option A, Option B, the fallback.
5. **Edit with the user.** Ask what to change for this lead: scope, price, timeline, what to leave out. Update the draft until they're happy. If the price changes, keep it consistent (Option A's payments, Option B).
6. **The message.** Write it for the channel they're talking on (template `offer-message`): their goal in their words, what's included for them, the price and how they pay, one proof point, one next step. The anchor and options stay for the call. Run `check_message` (stage `offer`) and fix every error.
7. **Save.** Write `offers/<lead-key>.md` with the offer and the message. The user sends it themselves. When they say they did: `record_offer` (channel, angle, what was offered, the price, the proof, the lead's link and company), then `workbook.py update <key> status=offer_sent offer_price=<price> offer_file=offers/<file>`.

## Follow-up after an offer (stage `follow_up`)

`tailor_offer` with stage `follow_up` shows what was already offered. One new, useful thing (a relevant result, an answer to a likely question, a timing detail) and an easy way to say "not now" (template `offer-follow-up`). At most two follow-ups; then pause or close.

## Call plan (stage `call`)

Their goal, then the anchor, then their offer, then stop. The objection to expect and what answers it. After a no: "Is it the total, or paying it all at once?" → Option A or Option B → the fallback. After the call, a recap (template `call-recap`) and `status=meeting` or `won`.

## Rules

- Only facts from the saved offer and what the lead said. Never invent results, numbers, limits or deadlines.
- One idea and one ask per message.
- Never lower the price of the same thing; change how they pay or remove parts.
- Nothing is sent from here: the user sends it and then says so.
