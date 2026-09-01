# The Close Variants Boundary

Use with `../SKILL.md`. This file exists because Broad Match and Close Variants are the two most confusable tasks in the TELUS set, and confusing them produces wrong answers on the most common category in each.

Read it before rating if you have ever worked a Close Variants task, and read it again if a rating feels obvious.

## Contents

- [Why they collide](#why-they-collide)
- [Where the two rubrics invert](#where-the-two-rubrics-invert)
- [Where they agree](#where-they-agree)
- [Telling the tasks apart](#telling-the-tasks-apart)

## Why they collide

They share almost every surface feature:

- Both pair two short search terms and rate the relationship.
- Both use the labels **Good, Acceptable, Bad**.
- Both ship App Store and web search research links.
- Both name their categories with the same words: spell correction, space, reordering, transliteration, singular/plural, abbreviation, addition or removal of words, former app name, translation.

And they ask different questions. Close Variants asks whether the two terms **resemble each other** in appearance, meaning and intent. Broad Match asks whether the advertiser's keyword intent **covers** the user's query intent. Resemblance and coverage diverge, so the ratings diverge.

## Where the two rubrics invert

Nine cases. In each, applying the Close Variants rule to a Broad Match task gives the wrong answer.

| Case | Close Variants | Broad Match |
|---|---|---|
| **Translation** (`Banking` → `Bankwesen`) | **Bad.** "Translations are NOT close variants", stated as an always-rule | **Good.** Category 9 |
| **Former app name** (`Twitter` → `X`) | **Bad.** "Former app names are always Bad" | **Good.** Category 8 |
| **Synonyms** (`fitness` → `Workout`) | **Bad.** "Synonyms are always Bad", they fail the appearance test | **Acceptable.** Category 4 |
| **Spell correction** (`utube` → `youtube`) | **Acceptable.** A spelling mistake is a minor appearance issue | **Good.** Category 1 |
| **Adding or removing "free"** (`Free games` → `games`) | **Bad.** Adding "free" changes intent | **Good.** Category 7 |
| **Country added** (`mcdonalds` → `mcdonalds austria`) | **Acceptable only if the locale matches**, otherwise Bad | **Good.** Category 7, no locale condition |
| **Qualifier added** (`strategy` → `strategy game`) | **Acceptable.** An implied word that does not change intent | **Good.** Category 7 |
| **Brand narrowed to parent** (`scanner pro` → `scanner app`) | **Bad.** Intent broadened to a different meaning | **Acceptable.** Category 3 |
| **Two different apps** (`adidas` → `Nike`) | **Bad.** Research showing different apps settles it | **Acceptable.** Competitors, category 1 |

The pattern behind all nine: **Broad Match is more permissive than Close Variants, on purpose.** An ad only has to be appropriate for the query. A close variant has to be nearly the same string. Anything Close Variants rejects for looking different can still pass here on intent.

Three of these, translation, former app name and synonyms, are *always Bad* in Close Variants and *never Bad* here. They are also common. That is why this is the most dangerous confusion in the set.

## Where they agree

Five operations rate the same in both, so instinct is safe here and nowhere else:

- Space added or removed (`tiktok` → `tik tok`) — Good in both
- Reordering that preserves meaning (`google earth` → `earth google`) — Good in both
- Transliteration (`Douyin` → `抖音`) — Good in both
- Well-known abbreviation (`instagram` → `ig`) — Good in both
- Singular against plural (`racing game` → `racing games`) — Good in both

Both also reject a pair whose intents genuinely differ, though they get there by different routes.

## Telling the tasks apart

| | Broad Match | Close Variants |
|---|---|---|
| The two fields are called | **Keyword** and **Expansion** | **Query** and **Variant** |
| The pair represents | what an advertiser bought, and what a user typed | an original query and a variant of it |
| The task asks | does the keyword's intent cover the query's | does the variant resemble the query |
| Guideline | `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf` | `TELUS-TASKS/Close Variants/Telus - Close Variants.pdf` |

**"Keyword" and "Expansion" are the tell.** If the task names those two columns, it is Broad Match, and the Close Variants always-rules do not apply. If it says Query and Variant, stop reading this skill and use `../close-variants-evaluator/SKILL.md`.

If the labels are ambiguous, one pair settles it. A translation pair rated Good is Broad Match; the same pair is Bad under Close Variants.
