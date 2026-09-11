# Comment Style

Use with `../SKILL.md`. The model to match is the Notes column of the guideline's own rating tables — short, flat, and about the relationship rather than about your process.

## The formula

One sentence, two at most.

1. **Name the relationship.** What the query did to the keyword: added an attribute, dropped a modifier, substituted a synonym, rebound the token to a brand, reordered tokens, introduced a typo.
2. **Say what that does to the intent.** Contained, contained but surprising, or lost — and for Bad, what each intent actually is.

## By rating

**Good** — usually one clause is enough.

> Same category with an added attribute.
> Same service, adds proximity.
> Clear synonym, the intent is unchanged.
> The brand is preserved and the query adds geographic intent.

**Acceptable** — say what the uncertainty is. Vagueness here is the most common weak comment.

> The full intent of the keyword is contained, but the query names a restaurant brand and the advertiser may be surprised to match.
> Likely a typo with the same intent.
> Studio implies a smaller specialized business and center implies a larger general one, so equivalence is uncertain.

**Bad** — name **both** intents. "Different intents" on its own tells a reviewer nothing.

> Loses the cuisine specificity the advertiser bought.
> Different intent: the keyword is a delivery service and the query is about cooking at home.
> The keyword is an abbreviation and the query is the full brand name, which is the direction the guideline rates Bad.

## Rules

- Write in English regardless of market.
- Quote the strings as they appear; do not silently correct a typo in the keyword.
- Name the specificity that was lost, not just that something was lost.
- When a pair turns on one of the two documented contradictions, say which rule you applied and why in one extra line. See `resolved-tensions.md`.
- Never describe your process. `Checked whether the token appears in the query` is not a comment.

## Anti-patterns

| Don't | Do |
|---|---|
| `Semantically divergent intents with low containment.` | `Different intent: the keyword is a haircut service and the query is about hair removal.` |
| `Different intents.` | `The keyword targets a barber shop and the query is for a hair salon, which serves a different market.` |
| `Not a good match.` | `Loses the time-availability requirement in the keyword.` |
| `The substring rule applies so this is Good.` | `The keyword appears as a whole word and the sense is unchanged.` |
| `Probably fine.` | `Likely a typo with the same intent.` |
