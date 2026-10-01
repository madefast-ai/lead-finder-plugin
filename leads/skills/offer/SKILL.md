---
name: offer
description: Write an offer for one lead, adapted to the platform - a LinkedIn note or message, InMail, email, Reddit reply or DM, Instagram DM - from the user's saved offer and the lead's research, without repeating what was already pitched to them or their company. Use when the user types /leads:offer, or picks a lead and wants an offer, a first message or a follow-up for them.
user-invocable: true
---

# An offer for one lead

Start from the saved offer (never ask the user to re-explain their business) and the lead's own words. Use the `lead-finder` skill for the workbook and `references/outreach.md` there for the platform rules.

## Steps

1. **The offer.** `get_offer`. If there's none, run the `offer-builder` skill first (once). If there are several, pick the one for this lead's campaign, or ask.
2. **The lead.** Read their row from the campaign workbook (or use the result id from a recent search). If there's no research (no posts, comments or about), suggest `research_lead` first: it gives the hook. Check the row's status and notes: a follow-up or a reply needs a different stage.
3. **Channel and stage.** Ask which channel if it isn't clear (suggest one: a LinkedIn note to connect, a message if already connected, a Reddit reply if they asked in public, a DM on Instagram; email only where consent allows). Stage: `first_touch`, `after_connect`, `follow_up`, `reply` or `call`.
4. **Brief.** `tailor_offer` with the channel, stage and the lead (link or key, name, role, company, location, signal, research, notes) or `result_id`. It returns the offer parts allowed at this stage, the channel's limits, what was already pitched to them and their company, the email consent rule, and the objection map.
5. **Offer card** (for the user; not sent). Short:
   - **Their goal**, in their words (quote the post or comment).
   - **Their likely objection** (not worth it, won't work for me, too hard, no time) and the evidence.
   - **What answers it**: one proof point, bonus or guarantee from the saved offer.
   - **Lead with**: the first-touch offer, not one already used for them or their company.
   - **Angle**: a few words.
   - **Next step**, and for later which call offer fits.
6. **The message.** Write it to the channel's shape and limits:
   - LinkedIn note: a hook plus a permission question for the first-touch offer. No pitch, no link, no price.
   - LinkedIn message or InMail: their words, one matching proof point, the first-touch offer, one easy A-or-B question.
   - Email: only if consent allows; subject under 7 words; opt-out footer.
   - Reddit reply: a genuinely helpful answer, no offer. Reddit DM only if they asked for help.
   - Instagram DM: friendly, about their post, one small offer and a question.
   Every first message includes where their details came from and how to opt out.
7. **Check.** `check_offer` with the draft (channel, stage, subject, the lead's location). Fix every error and check again. Only then show the card and the message.
8. **Keep it.** When the user is happy: save the message to the workbook row (`draft_first_message` or `draft_follow_up`, plus `offer_angle`, `offer_first`, `offer_channel`, `data_source_note_sent=yes`) and write the card to `offers/<lead-key>.md`. Then `record_offer` (channel, stage, angle, first offer, proof, the lead's link and company) so later offers to them or their colleagues use something different.
9. **After they answer.** Yes → deliver the first-touch offer, then the call (anchor, main offer, stop). No because of price → "the total, or paying it all at once?" → payment plan or feature downsell, never a lower price for the same thing. Silence → a follow-up with a new angle (at most 3).

## Rules

- Only facts from the saved offer and the lead's data. Never invent results, numbers, scarcity or deadlines.
- One idea and one ask per message.
- Nothing is sent from here: the user sends it and then says so (`status=contacted`).
