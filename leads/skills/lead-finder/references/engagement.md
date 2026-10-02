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
5. **offer_sent**: when they're interested (they asked about the work, the price, availability), the user sends their offer (`/leads:offer`).
6. **meeting**, then **won** or **lost**.

Log every touch, theirs and the user's: `workbook.py interact <workbook> <key> --by you|them --channel linkedin|reddit|instagram|email --kind comment|like|connect|reply|message|… [--url <post>] [--note "…"]`. It moves the status along and sets the next touch.

## Writing comments

- React to one specific thing they said, and add something: a point, a short example from the user's own work, or a real question.
- Short: LinkedIn under 80 words, Instagram under 30, Reddit as long as the answer needs (about 180 words at most).
- Never: a pitch, an offer, a price, a link, "DM me", "let's connect to talk business", praise with nothing in it ("Great post!").
- Write like the user writes. Plain words, no buzzwords.
- Run `check_message` (stage `engage`) and fix every error before showing a draft.

## When they write to you

- Answer what they said. Talk about what you do only when they ask.
- One question at a time, about their goal or what's in the way. Their words are what the offer will answer.
- No call request in the first reply unless they asked for one.

## The offer

- Only for leads who are `warm`, `talking` or later, and who've shown interest. Use the `offer` skill.
- Their goal in their words, what's included for them (with durations), the real price and how they pay, one proof point, the guarantee if there is one, one next step.
- The anchor, the payment plan and the feature downsell are for the call.
- After an offer, at most two follow-ups, each adding something new. Then pause or close.

## Platform notes

- LinkedIn: comments on their posts are seen by them and their network; reply to their replies. A connection request after a few comments is natural; keep the note empty or about the conversation.
- Reddit: many subreddits ban self-promotion. A helpful answer is the only engagement; DM only if they asked you to.
- Instagram: comment on their posts and stories' posts; reply when they reply. DM only when they messaged first or invited it.

## Writing rules for every draft

- Plain, concrete wording. Name the specific behaviour, number or scenario.
- No em or en dashes. No "not X, but Y" contrasts. No hype words or filler ("just checking in").
- Never invent results, credentials, deadlines, scarcity or emotional states. Only numbers from the saved offer.
- Refer to the lead's audience as "they".
