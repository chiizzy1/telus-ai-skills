# Decision Procedure — Worked

The ordered steps are in `../SKILL.md`. This file explains the two tests that carry the most weight and are easiest to apply loosely: the token test and the substitution test.

## The token test

> Do all of the keyword's content tokens appear in the query as whole words?

**Content tokens** are the words that carry the intent. Ignore articles, prepositions and connectives the query adds — `pizza place` → `best place to get pizza` is Good, because `pizza` and `place` are both present and the filler is free.

**What counts as the same token**

| Variation | Counts? | Guideline evidence |
|---|---|---|
| Plural / possessive / inflection | yes | `church` → `church**s** chicken` is Acceptable, not Bad |
| Typo | yes | `daves hot chicken` → `daves **ht** chicken` is Acceptable |
| Reordering | yes | `auto repair` → `repair auto` is Good |
| Buried inside a longer word | **no** | `apple` → `apple**bees**` is Bad |
| Same characters, separate word | yes | `apple` → `apple bee` is Acceptable |

The last two rows are one space apart and rate two bands apart. This is the rubric's sharpest edge and it is orthographic, not semantic. Apply it literally.

**Why the test is worth running first.** It is nearly mechanical, and it partitions the space cleanly: tokens present means Good or Acceptable, and the only remaining question is whether the sense held. Tokens absent means the pair has to earn its rating through synonymy, and most such pairs are Bad.

## The substitution test

Reached only when the tokens are absent. The question is whether the different words are equivalent, and the deciding property is **level of generality**.

**Same level → Good.** Both strings pick out the same set of things.

- `auto repair` → `car repair` — auto and car denote the same vehicles
- `coffee shop` → `coffee house` — two names for one business type
- `gas pump` → `petrol pump` — regional variants of one object

**Same level, fuzzy edges → Acceptable.** The sets mostly overlap but a reasonable person could draw them differently.

- `fitness studio` → `fitness center` — the guideline's note is that studio implies smaller and specialized, center larger and general
- `attorney` → `lawyer` — *"different legal categories however they can be used colloquially similarly"*
- `luxury hotel` → `5 star hotel` — subjective quality vs a formal rating system

**Different level → Bad.** One string picks out a subset or superset of the other, using different words.

- `sandwich` → `turkey club` — a turkey club is one sandwich among many
- `breakfast` → `pancakes`, `fruit` → `apple`, `thai food` → `pad thai` — same shape
- `coffee` → `espresso`, `ice cream` → `frozen yogurt` — sibling categories, not one containing the other

**The distinction that trips people.** `chicken` → `chicken fingers` is **Good** while `sandwich` → `turkey club` is **Bad**, and both look like category-to-specific-item. The difference is that the first keeps the keyword's own word and the second replaces it. Once the keyword's word is gone, narrowing is indistinguishable from changing the subject, and the guideline resolves that against the match.

Put plainly: **narrowing is Good when it is additive and Bad when it is substitutive.**

## Removal versus replacement

A missing keyword token is not automatically Intent Loss. The guideline separates two cases that look identical in a token diff:

| | Query | Rating |
|---|---|---|
| **Removal** — modifier gone, query strictly broader | `coffee shop free wifi` → `coffee shop` | Bad |
| **Replacement** — modifier swapped for another word | `coffee shop free wifi` → `coffee shop with wifi` | **Acceptable** |

The guideline's note on the second: *"Keyword specified free wifi, but query is likely for the same."* The query has not broadened — a coffee shop advertising wifi is almost certainly advertising free wifi — so the advertiser's requirement survives in substance.

The test: **would the query now match things the keyword excluded?** Removal opens the match up; replacement does not. `starbucks cafe` → `starbucks coffee shop`, `wedding photographer` → `wedding photo` and `steak restaraunt` → `steakhouse` are all replacements, all Acceptable.

Replacement then goes to the substitution test, which is where the Bad replacements are caught: `sushi restaurant` → `japanese restaurant` and `starbucks` → `coffee shop` swap a term for a broader one, so they fail on level of generality rather than on removal.

## Specificity loss has no Acceptable band

Every modifier in the keyword is something the advertiser paid to require. A query that drops one is Bad, with no borderline case anywhere in the guideline:

`sushi restaurant` → `restaurant` · `24 hour pharmacy` → `pharmacy` · `womens hair cut` → `hair cut` · `24/7 plumber` → `plumber` · `waterfront dining` → `dining` · `dentist portland oregon` → `dentist` · `fried chicken` → `chicken` · `fine dining` → `dining`

Every one of these is a **removal**. None replaces the dropped modifier with anything.

Geographic, temporal, quality, gender, brand and preparation modifiers all behave identically. If you find yourself reasoning that a dropped modifier was not very important, you have left the rubric — the guideline never grades modifiers by importance.

## Sense rebinding, and why it is Acceptable rather than Good

When a query keeps the keyword's token but attaches it to a different entity, the intent is contained in the literal sense and absent in the practical sense. The guideline resolves this in the advertiser's favour on containment and against them on satisfaction, which is what the Acceptable band is for. Its own explanation:

> Acceptable because intent IS contained, but advertiser might be surprised. In practice, negative keywords would prevent unwanted matches for advertiser.

Recognising the pattern: a common noun that is also a brand (`church`, `apple`, `beach`) followed by a word that fixes it to the brand reading (`chicken`, `bee`, `outlets`).

Note the limit — `apple` → `caramel apple` is also Acceptable, and there is no brand in the query at all. The rebinding is from the tech company to the fruit. So the test is not "did a brand appear" but "did the query fix a different sense of the keyword than the advertiser likely meant."

## When two steps disagree

Later steps do not override earlier ones except where `../SKILL.md` says so — Step 6, the brand asymmetry, is the only override, and it beats both Step 4 and Step 5. `raising canes` → `canes` is the proof: a pure token removal that is nonetheless Good, because the shortened form is a recognized abbreviation of the brand. Whenever either string names a brand, run Step 6 before either of them. Everything else is first-match-wins. If a pair seems to qualify under two steps, you have probably mis-run the token test; re-run it before reasoning further.
