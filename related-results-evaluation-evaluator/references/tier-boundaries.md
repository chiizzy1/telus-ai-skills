# Tier Boundaries

Use with `../SKILL.md`. `relationship-types.md` says what connects the pair; this file settles the calls that sit on a line between two tiers. Every rule here comes from the guideline, not from judgment.

## Contents

- [The three standing assumptions](#the-three-standing-assumptions)
- [Excellent or Good](#excellent-or-good)
- [Good or Acceptable](#good-or-acceptable)
- [Acceptable or Bad](#acceptable-or-bad)
- [The disqualifiers](#the-disqualifiers)
- [Calibration failures to watch for](#calibration-failures-to-watch-for)

## The three standing assumptions

These apply to every pair, before any tier is considered. They are not tiebreakers; they remove three factors from the rating entirely.

1. **Distance never counts.** `in chicago`, `near me` and every other location word is already satisfied. Treat the pair as geographically relevant and never demote for distance, and never credit for proximity.
2. **Open status never counts.** If research shows the result is closed now, seasonally closed, or permanently closed, rate it as if it were open. Closure is not a demotion here.
3. **A vague query gets a generous guess.** If the query has several possible meanings and the result carries the query word, that is Excellent. This applies only where the query is genuinely ambiguous.

Assumption 3 is the only one that can raise a rating. The first two can only stop you lowering one.

## Excellent or Good

The line is **is this the thing, or an alternative to the thing**.

- The result is the brand asked for, a department of that brand, or a business that specializes in the queried category → **Excellent**.
- The result competes with what was asked for, offering similar goods in a similar setting → **Good**. This is a hard cap: a competitor never reaches Excellent however good a substitute it is.
- The result offers the queried item as a **main** offering → Excellent. As a **side** offering → Good.

`[golf store]` → Golf Galaxy is Excellent because golf is the whole business. `[ice cream]` → McDonald's is Good because ice cream is a side line at a burger chain.

## Good or Acceptable

The line is **does it really offer this, or does it merely stock it**.

- Offers the queried thing as a recognized part of what it does → **Good**. `[chicken wings]` → Pizza Hut. `[matcha]` → Boba Guys. A gas station that also has EV charging, for `[ev station]`.
- A general store that carries the item among thousands of others → **Acceptable**. `[motor oil]` → Target. `[mattresses]` → Costco.
- A specialist store that carries the queried category but is not dedicated to it → **Acceptable**. `[golf store]` → Dick's Sporting Goods.

Research decides this one. Whether a Chevron has EV chargers, or a boba shop makes matcha, is a fact about that POI, not a guess from the category name.

## Acceptable or Bad

The line is **would the user be unsurprised, or would they be frustrated**.

- Same broad field, exact item not offered, user would understand why it appeared → **Acceptable**. `[sushi]` → Ramen Nagi, both Japanese. `[coffee]` → Boba Works, both drinks.
- A mall for a store query, or a store for a mall query, where the store really is in that mall → **Acceptable**.
- The queried product or service is not available at the result at all → **Bad**. `[motor oil]` → Macy's.
- The mall does **not** contain the queried store → **Bad**. `[uniqlo]` → The Mall at Short Hills.
- The result violates a stated constraint in the query → **Bad**. See disqualifiers.

`[sushi]` → Ramen Nagi is Acceptable and `[sushi]` → Haidilao Hotpot is Bad. Both fail to serve sushi. The difference is that ramen sits in the same cuisine a sushi seeker is already browsing, while hotpot reads as a different meal altogether.

## The disqualifiers

Each of these forces **Bad** no matter how much else the pair shares.

| Disqualifier | Example |
|---|---|
| The queried product or service is genuinely unavailable there | `[ev station]` → a Chevron with no chargers |
| Shared words, unrelated intent | `[dog park]` → Lazy Dog Restaurant |
| A dietary constraint in the query is violated | `[vegan restaurant]` → McDonald's |
| A service tier in the query is violated | `[fast food]` → Alexander's Steakhouse |
| A meal or daypart in the query is not served | `[dinner]` → Starbucks |
| A different brand operating inside the queried business | `[safeway]` → the Starbucks inside it |
| The mall does not contain the queried store | `[uniqlo]` → The Mall at Short Hills |
| Nothing connects them | `[chase bank]` → Autozone |

## Calibration failures to watch for

**Too generous**

- Excellent for a competitor. The cap is Good, always.
- Excellent for shared words when the query had one clear meaning.
- Good for a general store that merely stocks the item. That is Acceptable.
- Acceptable for a result where the queried thing is not available at all. That is Bad.

**Too harsh**

- Bad for a secondary offering that really is sold there. `[ice cream]` → McDonald's is Good.
- Bad for a neighbouring category the user would not be surprised by. `[sushi]` → Ramen Nagi is Acceptable.
- Bad for a closed or permanently closed POI. Closure is not rateable here.
- Bad because the result is far away, or Acceptable held down by distance. Distance is not rateable here.
- Acceptable for a vague query whose word the result carries. That is Excellent.
