# Phrase Match vs Broad Match vs Close Variants

Three TELUS tasks pair two short strings and grade them `Good` / `Acceptable` / `Bad`. They are different rubrics and they disagree on the most common patterns. Carrying one into another produces confident wrong answers, and because the labels match, nothing in the output looks wrong.

## Identify the task before rating

| Columns | Task |
|---|---|
| `Keyword` + `Query` | **Phrase Match** |
| `Keyword` + `Expansion` | Broad Match |
| `Query` + `Variant` | Close Variants |

If the interface offers `Excellent`, none of the three is right — that is Search Ads Relevance or Related Results.

## Where they invert

| Pattern | Phrase Match | Broad Match | Close Variants |
|---|---|---|---|
| Transliteration (`mcdonalds` → `麦当劳`) | **Bad** | Good | **Good** |
| Translation | Bad | **Good** | **Bad** |
| Clear synonym (`coffee shop` → `coffee house`) | **Good** | Acceptable | **Bad** |
| Loose synonym (`attorney` → `lawyer`) | **Acceptable** | Acceptable | Bad |
| Abbreviation, head → variant (`mcdonalds` → `mcd`) | **Good** | Good | Good |
| Abbreviation, variant → head (`mcd` → `mcdonalds`) | **Bad** | Good | Good |
| Token reordering | Good | Good | Good |
| Typo in the second string | **Acceptable** | Good | Acceptable |
| Adding specificity (`chicken` → `fried chicken`) | **Good** | Acceptable | Bad |
| Dropping specificity (`fried chicken` → `chicken`) | **Bad** | Bad | Bad |
| Former app name | n/a | Good | **Bad** |
| Competing brands | Bad | Bad | Bad |

Rows in bold are the ones most likely to be answered from the wrong rubric.

## The three that will actually catch you

**1. Transliterations.** Close Variants states outright that transliterations *are* close variants and should be rated Good when they sound the same phonetically across scripts. Phrase Match states outright that they are Bad *"even if meaning equivalent across languages,"* using the same McDonald's example. If you have rated Close Variants recently, this is the rule your instinct will get wrong.

**2. Synonyms.** Close Variants rule 5 is *"Think APPEARANCE + MEANING + INTENT"* — synonyms that mean the same but look different are Bad there, with `baby games` → `infant games` as the stated example. Phrase Match has no appearance requirement at all: it tests intent containment only, so `coffee shop` → `coffee house` is Good.

**3. Direction of abbreviation.** Neither sibling cares which of the two strings is the fuller form. Phrase Match makes it decisive, because the keyword is a purchase and the query is a search. Ask which string the advertiser bought before rating any brand pair.

## Why Phrase Match is structurally stricter

Broad Match asks whether the advertiser's intent *covers* the expansion — a containment test with slack in it. Close Variants asks whether two queries *resemble* each other in form and meaning. Phrase Match asks whether the query **clearly and completely contains** the keyword's intent, and its own tie-breaker is *"default to Bad when containment is not clear."*

That last clause has no equivalent in either sibling. When a Phrase Match pair feels borderline, the guideline has already told you which way to fall.
