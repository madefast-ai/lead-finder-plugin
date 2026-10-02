---
name: offer-builder
description: Build or revise the user's offer through an interview - exactly what it includes and how long each part runs, the price and payment terms, proof and guarantee, an anchor (a real bigger version), what to offer after a no (payment plan or feature downsell), bonuses and real limits - then check it with the value equation. Use when the user types /leads:offer-builder, sets up Lead Finder, has no saved offer, or wants to change what they sell, their price, inclusions, proof or guarantee.
user-invocable: true
---

# Offer builder

The offer is built **once** with an interview and saved on the Lead Finder server (the user's own business data), so every lead's offer starts from it and the user never has to explain their business again. In Cowork it's mirrored to `offer.md`. It's shown only to leads who are already talking with the user and interested: Lead Finder never pitches strangers, so there's nothing here for a first message.

The method comes from Alex Hormozi's *$100M Offers* (the offer and the value equation) and *$100M Money Models* (anchor, payment plan, feature downsell).

Tools: `build_offer` (the steps, what's saved, what's missing, a value check), `save_offer` (save after every answer), `get_offer` (the offer plus Markdown for `offer.md`), `list_offers`, `delete_offer`.

## How to run it

1. Call `build_offer`. If an offer exists, show its name and the value check, then continue with the first step that has missing fields. A second offer (another product or segment) gets a new name.
2. Work in the order below, **one question at a time**, in plain words. Skip what's already saved; ask only for what's missing. Save each answer with `save_offer` right away (only the fields you have).
3. At the end: the value check, said plainly, then the Markdown. In Cowork, write it to `offer.md` (replace the file; it's a mirror).

## The interview

1. **What exists.** The offers they sell today: what's in each, the prices, any guarantee, real client results. Note it; it saves questions later.
2. **The buyer and the result.** Who buys (company type, size, the role that signs) and the result they want, in their words: what would they say after it worked?
3. **Problems and solutions.** Every obstacle between them and the result, in the order they meet it (before, during, after). For each: how it's solved and how it's delivered (done for them, with them, a tool, a template).
4. **What's included.** Exactly what they get, part by part, and how long each part runs or how often ("store rebuild, 6 weeks", "weekly 1:1 call for 90 days"). How long the whole thing runs. The part that matters most to buyers gets named in every presentation of the offer; ask which one it is.
5. **Price and terms.** The price, how it's charged (one-off, monthly, per project) and when they pay ("50% upfront, 50% at launch").
6. **Proof and guarantee.** Real results with numbers and who they were for. If there are none, save none and say so plainly: it's the gap, and a real guarantee is the next best thing. A guarantee only if it's really given, written "if not X in Y time, we will Z" (unconditional, conditional, anti-guarantee or performance-based).
7. **Speed and effort.** What happens quickly, and roughly when (`first_win`). What they don't have to do or work out themselves (`effort_removed`). Never promise income or a result by a date.
8. **The anchor.** A real, bigger version shown first on a call, so the main offer looks reasonable. The simplest one is the same offer for longer or with more support, at its own price. It must be real: if someone says yes, the user delivers it.
9. **After a no.** On a call, the first question is "Is it the total, or paying it all at once?"
   - **Option A, paying at once:** the same offer split into payments (the amounts).
   - **Option B, the total:** fewer parts for less. Remove the parts that take the most of the user's time; never the same thing cheaper. Its price.
   - **Fallback:** the smallest paid option if it's still no.
10. **Bonuses and real limits.** Each bonus answers one objection: *not worth it*, *won't work for me*, *too hard*, *no time*. Limits and deadlines only if real ("3 new clients a month", a real start date). Check a limit is one the user will actually keep.
11. **Name, next step and sender.** A name (MAGIC: a reason why, the audience, the goal, a time frame, a container word like Sprint, Rebuild, Programme). What they ask for when someone's interested (a 30-minute scoping call). Who signs, the languages and formality.

## Value check

Value = (dream outcome × likelihood of success) / (time delay × effort and sacrifice). `build_offer` and `save_offer` rate each part strong, medium or weak. Say plainly what's weak and what would fix it:
- **Dream outcome:** is the result stated, or only the features?
- **Likelihood:** proof, the guarantee, a process matched to their situation. No testimonials? Say it's the gap and lean on the guarantee. Never invent results.
- **Time delay:** what happens quickly. Never a time to a result or an income by a date.
- **Effort:** what they don't have to work out alone.

## Keep it consistent

When one part changes (price, what's included, the guarantee, the anchor), update every related part in the same turn: the anchor's price, Option A's payments, Option B, the fallback, and `offer.md`. List what changed.

## On the call (when the user asks)

Anchor first, then the main offer, then stop talking. After a no: "Is it the total, or paying it all at once?" → Option A or Option B → the fallback. Never lower the price of the same thing; add a bonus that answers their objection, change how they pay, or remove parts.

## Copy rules (every output and every reply)

- Plain, concrete wording. Name the specific behaviour, number or scenario.
- No em or en dashes. No "not A, but B", "not because A, but because B" or "No A, no B, just C" patterns. No idioms or figurative expressions, no buzzwords.
- Write about the audience as "they".
- Never invent credentials, results, testimonials, timeframes, limits, bonus values or emotional states. State credentials plainly.
- Replies to the user: short, what changed and why, one next step at most.
