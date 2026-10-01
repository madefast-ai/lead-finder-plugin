---
name: offer-builder
description: Build or revise the user's core offer once - who it's for, the result, the problems it solves, proof, price, guarantee, bonuses, the small offers that fit a first message, and what's kept for the sales call - then check it with the value equation. Use when the user types /leads:offer-builder, sets up Lead Finder, has no saved offer, or wants to change what they sell, their price, proof, guarantee or offer ladder.
user-invocable: true
---

# Offer builder

The offer is built **once** and saved on the Lead Finder server (the user's own business data), so every tailored message starts from it and the user never has to explain their business again. In Cowork it's mirrored to `offer.md`. The method comes from Alex Hormozi's *$100M Offers* (the Grand Slam Offer) and *$100M Money Models* (which offer goes when).

Tools: `build_offer` (the steps, what's saved, what's missing, a value check), `save_offer` (save after every answer), `get_offer` (the offer plus Markdown for `offer.md`), `list_offers`, `delete_offer`.

## How to run it

1. Call `build_offer`. If an offer exists, show its name and the value check, then continue with the first step that has missing fields. If the user wants a second offer (another segment or product), start one with a new name.
2. Go step by step, **one question at a time**, in plain words. Save each answer with `save_offer` right away (only the fields you have).
3. At the end, show the value check and the Markdown. In Cowork, write it to `offer.md` (replace the file; it's a mirror).
4. When anything changes later (price, proof, guarantee, the first-message offers), update it with `save_offer` and rewrite `offer.md` in the same turn. Say what changed.

## The steps

1. **The buyer and the result.** Who buys (company type, size, the role that signs) and what result they want, in their words. The best dream outcome says how others will see them after.
2. **Problems and solutions.** Every obstacle between them and the result, in the order they meet it (before, during, after). For each: how it's solved and how it's delivered (done for them, with them, a tool, a template). Trim what costs a lot and adds little.
3. **Proof.** Real results with numbers and who they were for. If there are none, save none and say so. Drafts may only use numbers that are saved here.
4. **Speed and effort.** What they get quickly and roughly when (`first_win`), and what they don't have to do or work out (`effort_removed`). Never promise income or a result by a date.
5. **Price and risk.** Price and how it's paid. Raise value before price and never compete on price. A guarantee only if it's really given, written "if not X in Y time, we will Z", one of four types: unconditional, conditional (they do their part), anti-guarantee (all sales final, with a real reason), performance-based (pay on results).
6. **Bonuses, scarcity, urgency.** Each bonus answers one objection: *not worth it*, *won't work for me*, *too hard*, *no time*. Scarcity and urgency only if real: actual capacity ("3 new clients a month"), actual start dates or seasons. Never invent them.
7. **The first-message offer (attraction offer).** Something small and low-risk a stranger can say yes to: a free audit or teardown of their company, a short report, a small paid pilot, a "pay only if it works" promise (only if real), a credit for switching from a competitor they complained about. Then the smallest next step (`call_to_action`).
8. **For the call.** A real, bigger version shown first (anchor); a menu of options (say what they don't need, recommend what they do, ask A or B); a payment plan (same thing, split); a feature downsell (fewer parts for less, removing what takes the most of the user's time; never the same thing cheaper); what continues after (retainer, support).
9. **Name and sender.** A name that works in a subject line (MAGIC: a reason why, the audience, the goal, a time frame, a container word like Sprint, Audit, Blueprint). Who signs, and the outreach languages and formality.

## Value check

Value = (dream outcome × likelihood of success) / (time delay × effort and sacrifice). `build_offer` and `save_offer` rate each part strong, medium or weak from what's saved. Say plainly what's weak and what would fix it: a result stated as the outcome rather than features; proof or a real guarantee for likelihood; a quick first win for time; what they're spared for effort.

## Presenting the offer (when the user asks)

- **Price page:** anchor on the left, main offer on the right, same format; ticks for what's included; on the cheaper option, what the anchor has and it doesn't. The payment plan and the feature downsell on a second page ("Other options"). Load the artifact-design skill first.
- **Offer post:** a hook question naming the outcome; from and to; what happens first and what follows; what they don't have to work out alone; the proof and guarantee; how to apply and the real number of spaces.
- **Call order:** anchor, main offer, stop talking. After a no: "Is it the total amount, or paying it all at once?" All at once → payment plan. The total → feature downsell. Still no → the smallest paid option.
- **Application** (limited spaces): a few questions about their business, where they are now, what they tried, what stops them, the time they can give, and whether they're ready to invest in the next 30 days. The number of spaces must be a real limit.

## Rules

- Never invent credentials, results, testimonials, numbers, timeframes, scarcity, deadlines or bonus values.
- Never discount the same thing to close. Add a bonus that answers their objection, change how they pay, or remove parts.
- Discounts only in exchange for something real (a case study, a testimonial, a referral).
- No hidden terms; every condition is stated up front.
- Plain, concrete wording; name the specific behaviour, number or scenario. No em or en dashes, no "not A, but B" or "no A, no B, just C" patterns, no idioms, no buzzwords. Write about the audience as "they".
