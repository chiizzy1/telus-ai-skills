# Comment Style

Use with `../SKILL.md`. This file is the authoritative source for how a Related Results comment is written.

A comment is mandatory on **every** rating here, not only on Bad. That makes the comment half the deliverable rather than an exception case, so it gets written to a pattern rather than improvised each time.

The comment is pasted verbatim into the rating tool and read by a human reviewer who can see the query and the result already. It has to tell them something the pair does not tell them by itself: what the user wanted, and what this POI actually is.

## Contents

- [The formula](#the-formula)
- [Worked examples by tier](#worked-examples-by-tier)
- [Rules](#rules)
- [Anti-patterns](#anti-patterns)

## The formula

Two plain sentences. Occasionally one, when the pair is simple enough that a second would pad it.

1. **Name the intent**, in the form `The query is …`. Say what the user was after, in everyday words. For a vague query, say that it is vague and name the reading you took.
2. **Say what the result is and how it relates.** Name the connection that decided the tier: it is the same brand, it is a competitor, it sells this as a side line, it is a general store, it is the mall containing it, it has no connection.

The second sentence is where the rating is earned. A comment that describes the result without naming the relationship has not justified anything.

Write in English whatever the rating locale is. Never include personal names, phone numbers or account details, even where they appear on a map label.

## Worked examples by tier

**Excellent, exact match**

> `The query is for KFC. This result is a KFC, so it is exactly what the user asked for.`

**Excellent, category query**

> `The query is for food, with no type specified. Taco Bell serves food, so any user with this query would be satisfied.`

**Excellent, same brand inside the business**

> `The query is for Costco. This is the pharmacy counter operated by Costco inside the store, so it carries the same brand the user asked for.`

**Excellent, vague query**

> `The query is a single word with several possible meanings. This business is named The Willow, so it matches the word the user typed.`

**Good, competitor**

> `The query is for Starbucks. Peet's Coffee is a different coffee chain serving similar drinks in a similar setting, so it is an alternative rather than the place asked for.`

**Good, secondary offering**

> `The query is for ice cream. McDonald's does sell ice cream, but it is a side item at a burger restaurant rather than what the business is known for.`

**Good, service present alongside another**

> `The query is for an EV charging station. This Chevron sells fuel and also has EV chargers on site, so it provides the service as one of two.`

**Acceptable, general store**

> `The query is for motor oil. Target stocks a few kinds of motor oil, but it is a general retailer rather than a car parts store.`

**Acceptable, mall and store**

> `The query is for the Ontario Mills mall. This is a single UNIQLO store inside that mall rather than the mall itself.`

**Acceptable, neighbouring category**

> `The query is for sushi. Ramen Nagi is a Japanese restaurant that does not serve sushi, so it fits the cuisine but not the dish.`

**Bad, not available**

> `The query is for motor oil. Macy's is a clothing and home goods department store that does not sell motor oil at all.`

**Bad, shared word only**

> `The query is for a park where dogs can be walked. Lazy Dog Restaurant shares the word dog but is a restaurant, so it does not meet the intent.`

**Bad, constraint violated**

> `The query is for a vegan restaurant. McDonald's is a fast food chain built around meat, so it does not meet the dietary requirement.`

**Bad, no connection**

> `The query is for a Chase Bank branch. Autozone is a car parts store with no connection to banking.`

## Rules

- **Two sentences.** One if the pair is obvious. Never three unless the pair genuinely needs it.
- **Open with `The query is`.** Every comment. It forces you to state the intent before judging the result, which is the order the rating is supposed to be made in.
- **Name the relationship.** Competitor, side offering, general store, same brand, mall, no connection. That word is what tells the reviewer which rule you applied.
- **Use everyday words.** No evaluator jargon: no "intent alignment", "lexical overlap", "ancillary offering", "high-level category".
- **Never use em dashes.** Commas, colons, periods or parentheses.
- **No AI filler.** No "delve", "moreover", "furthermore", "it is worth noting", "matches the guideline pattern".
- **No guideline references.** No section numbers, no "per the guidelines", no naming the tier definitions.
- **No mention of tools or research.** Not the URL checker, not a search engine, not "I checked". State the fact you found, not how you found it.
- **No links and no figures.** Nothing here needs a source link or a number.
- **Do not restate the obvious.** The reviewer can see both names. Give them the relationship, not a re-reading of the card.

## Anti-patterns

**Justifying with distance.** Distance is excluded from this task by rule, so it cannot support a rating in either direction.

- Wrong: *"The query is for a Starbucks near the user, and this result is too far away to be useful."*
- Right: *"The query is for Starbucks. Peet's Coffee is a different coffee chain serving similar drinks, so it is an alternative rather than the place asked for."*

**Justifying with closure.** Rate as if the POI were open. A comment that leans on it being closed contradicts the rating it is attached to.

- Wrong: *"This location has permanently closed, so it would not help the user."*
- Right: *"The query is for a hardware store. This is an Ace Hardware, so it is exactly the kind of store the user asked for."*

**Describing without relating.** The comment lists what the result is and stops, leaving the reviewer to infer the rating.

- Wrong: *"Boba Guys is a bubble tea shop in San Francisco with several locations."*
- Right: *"The query is for matcha. Boba Guys mainly sells bubble tea but does serve matcha drinks, so it offers the item as a side line."*

**Robotic template.** The same clause structure bolted onto every pair, regardless of what decided it.

- Wrong: *"The result fails to satisfy the user intent and only partially aligns with the query category, making it a poor match for this query."*
- Right: *"The query is for a dog park. Lazy Dog Restaurant shares the word dog but is a restaurant, so it does not meet the intent."*

**Revealing the process.** The reviewer wants the finding, not the method.

- Wrong: *"After checking the Chevron website, I could not find any mention of EV charging."*
- Right: *"The query is for an EV charging station. This Chevron sells fuel only and has no chargers on site."*
