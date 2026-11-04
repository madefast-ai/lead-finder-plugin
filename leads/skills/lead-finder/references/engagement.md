# Engagement

Lead Finder never reaches out cold. The user only writes privately to people who have interacted with them first. Until then, they engage in public, where the lead chooses whether to respond.

## The path

1. **to_engage**: a lead the user wants to warm up (picked from a search, scored).
2. **engaging**: the user interacts in public, by hand, from their own accounts:
   - LinkedIn: a genuine comment on their posts, reactions, later a connection request without a pitch;
   - Reddit: a useful answer in their thread;
   - Instagram: a specific comment on their post, a follow.
   A few touches over one or two weeks, each one adding something. Never a pitch, a link or "DM me".
3. **warm**: they engaged back. They replied to a comment, commented on the user's post, reacted, accepted the connection, followed back.
4. **talking**: a conversation. They messaged the user, asked a question, or asked them to get in touch. Now private messages, DMs and email are fine, and they answer what the lead said.
5. **meeting**: when they're interested (they asked about the work, the cost, availability), the user suggests a short call and they book it. Claude prepares their offer for the call (`/leads:offer`).
6. **offered**: the user presented the offer on the call. Then the recap, at most two follow-ups, and **won** or **lost**.

Log every touch, theirs and the user's: `workbook.py interact <workbook> <key> --by you|them --channel linkedin|reddit|instagram|email --kind comment|like|connect|reply|message|… [--url <post>] [--note "…"]`. It moves the status along and sets the next touch. Log the post link with every touch; on LinkedIn, when you commented, prefer the link to your own comment (Copy link to comment): it lets the check see replies to that comment.

## Writing comments

- Answer what they asked for first. Write down for yourself what the post asks (a recommendation, a fix, how others do it, an opinion; on Reddit it's in the lead's `score_reason`) and put the answer in the first sentence. For a recommendation, give the way to choose (what to look for, what to avoid), never the user's own name.
- React to one specific thing they said, and add something: a point, a short example from the user's own work, or a real question.
- Short: LinkedIn under 80 words, Instagram under 30, Reddit as long as the answer needs (about 180 words at most).
- Never: a pitch, an offer, a price, a link, "DM me", "let's connect to talk business", praise with nothing in it ("Great post!").
- Write like the user writes. Plain words, no buzzwords.
- Run `check_message` (stage `engage`) and fix every error, and the warnings too, before showing a draft.

## When they write to you

- Answer what they said. Talk about what you do only when they ask.
- One question at a time, about their goal or what's in the way. Their words are what the offer will answer.
- No call request in the first reply unless they asked for one.
- When they're interested (they ask about your work, the cost or availability): answer what you can and suggest a 30-minute call (template `suggest-a-call`). No price in writing: `check_message` flags it.

## The offer, on a call

- Only for leads who are talking with the user and interested. Use the `offer` skill once the call is booked.
- The offer is presented on the call, never in a message: their goal in their words, the anchor, then what's included for them (with durations), the real price and how they pay, one proof point, the guarantee if there is one. Then stop.
- After a no: "Is it the total, or paying it all at once?" → the payment plan or the feature downsell → the fallback.
- After the call: the recap the same day (template `call-recap`), then at most two follow-ups, each adding something new. Then pause or close.

## Platform notes

- LinkedIn: comments on their posts are seen by them and their network; reply to their replies. A connection request after a few comments is natural; keep the note empty or about the conversation.
- Reddit: many subreddits ban self-promotion. A helpful answer is the only engagement; DM only if they asked you to.
- Instagram: comment on their posts and stories' posts; reply when they reply. DM only when they messaged first or invited it. The check sees comments and replies on your posts and on posts where you commented (replies need a paid Apify plan), not likes or DMs.

## Writing rules for every draft

- Plain, concrete wording. Name the specific behaviour, number or scenario.
- No em or en dashes. No "not X, but Y" contrasts. No hype words or filler ("just checking in").
- Never invent results, credentials, deadlines, scarcity or emotional states. Only numbers from the saved offer.
- Refer to the lead's audience as "they".
