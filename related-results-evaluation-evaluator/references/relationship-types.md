# Query-Result Relationship Types

Use with `../SKILL.md`. The guideline lists the ways a query and a result can be connected. Naming the relationship is the step that decides the tier, so do it before you reach for a rating.

A pair can carry more than one relationship at once. When it does, the strongest connection sets the ceiling and any disqualifier still overrides it.

## Contents

- [The types](#the-types)
- [Lexical similarity, the one that traps people](#lexical-similarity-the-one-that-traps-people)
- [Inside another business](#inside-another-business)
- [How a type becomes a tier](#how-a-type-becomes-a-tier)

## The types

| Type | What it means | Example |
|---|---|---|
| **Exact match** | The result is what the user asked for. | `[kfc chicago]` → KFC |
| **Alternative** | Same or very similar goods, services, atmosphere and experience. A competitor. | `[Peet's Coffee]` → Starbucks |
| **Belongs to category** | The query is a business or service category; the result is in it. | `[gas station]` → Shell |
| **Found at** | The query is a product or service; the result is known for offering it. | `[pizza]` → Pizza Hut |
| **Contains or is contained by** | A mall and a store inside it, in either direction. | `[ontario mills]` → UNIQLO Ontario Mills |
| **Same brand** | The result carries the same branding as the queried business. | `[Costco]` → Costco Gas |
| **Used with** | The two share a function and are commonly used together. The link must be simple, obvious and widely known. | `[airport]` → Hotel |
| **Lexical similarity** | The two share words. Only counts when the query is vague. | `[bear]` → Bears BBQ Place |
| **No relationship** | Nothing connects them. | `[chase bank]` → Autozone |

## Lexical similarity, the one that traps people

Shared words are evidence of a relationship **only when the query is vague or ambiguous**. That is the whole of the exception.

- Query is vague, result carries the word → **Excellent**. `[willow]` → The Willow - A Blooming Collective. `[holiday]` → Holiday Inn.
- Query has clear intent, result merely shares a word → **Bad**. `[dog park]` → Dog grooming. `[dry cleaning]` → Dry Creek Vineyards. `[cvs near me]` → CV Capital Funding.

The test is whether the query has one obvious reading. `[willow]` could be a tree, a name, a person, a bar. `[dog park]` could not be anything but a park for dogs, so the shared word buys the result nothing.

## Inside another business

Two results can sit at the same address and land at opposite ends of the scale. Brand is what separates them.

- **Same brand, specialized department or service** → **Excellent**. `[Walmart]` → Walmart Vision Center. `[Costco]` → Costco Pharmacy.
- **Different brand, does not satisfy the intent** → **Bad**. `[Safeway]` → the Starbucks inside the Safeway.

## How a type becomes a tier

| Relationship | Ceiling | Note |
|---|---|---|
| Exact match | Excellent | |
| Same brand, department or service inside | Excellent | |
| Belongs to category, result specializes in it | Excellent | |
| Found at, the result is known for it | Excellent | |
| Lexical similarity on a **vague** query | Excellent | Vague queries only |
| Alternative / competitor | **Good** | Hard cap. An alternative never rates Excellent |
| Found at, but a secondary or minor offering | Good | |
| Belongs to category, result is a general store | Acceptable | Sells it, does not specialize in it |
| Contains or is contained by (mall and store) | Acceptable | Either direction |
| Used with | Acceptable | |
| Neighbouring category, exact item not offered | Acceptable | `[sushi]` → Ramen Nagi |
| Lexical similarity on a **clear** query | Bad | |
| Product or service genuinely unavailable | Bad | |
| No relationship | Bad | |
