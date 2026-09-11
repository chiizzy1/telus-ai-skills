---
name: phrase-match-evaluator
description: Strict Phrase Match evaluator following the TELUS Phrase Match Human Rating Evaluation Guidelines (July 2026). Use when rating whether a user query clearly and completely contains the intent of an advertiser's phrase-match keyword, on a Good / Acceptable / Bad scale. Use when the task shows a Keyword column and a Query column. Part of the TELUS evaluator family. NOT Broad Match (Keyword/Expansion) and NOT Close Variants (Query/Variant); all three share the same three labels and disagree on transliterations, synonyms and abbreviations.
---

# Phrase Match Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root.
- Blank task template: `TELUS-TASKS/task-templates/phrase-match.md`. The live task is `TELUS-TASKS/task.md`.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and say the source was unavailable.

## Source Hierarchy

1. `TELUS-TASKS/phrase match human rating evaluation/phrase match human rating evaluation.pdf` — Phrase Match Human Rating Evaluation Guidelines, July 2026. Searchable extraction: `TELUS-TASKS/phrase-match-extracted/text.md`.
2. The current task UI and any task-specific instructions in it.
3. This skill's reference files.
4. User memory, previous chat, or general judgment.

If the user or a prior answer conflicts with the guideline, follow the guideline.

## Platform Separation

**The columns are the tell.**

| Columns | Task | Skill |
|---|---|---|
| `Keyword` + **`Query`** | **Phrase Match** | this one |
| `Keyword` + `Expansion` | Broad Match | `../broad-match-evaluator/SKILL.md` |
| `Query` + `Variant` | Close Variants | `../close-variants-evaluator/SKILL.md` |

All three use `Good` / `Acceptable` / `Bad` and all three pair two short text strings. They are not interchangeable — read `references/sibling-boundary.md` before your first rating. The three inversions that matter most:

- **Transliterations are Bad here.** Close Variants rates them Good. Broad Match rates them Good.
- **Synonyms can be Good here.** Close Variants rates them Bad.
- **Abbreviation direction is decisive here.** `mcdonalds` → `mcd` is Good; `mcd` → `mcdonalds` is Bad. Neither sibling has this asymmetry.

Phrase Match has no `Excellent`. If the task offers one, you are on Search Ads Relevance or Related Results, not this task.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating.

> **Output goes in the chat response only.** `TELUS-TASKS/task.md` and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, never create scratch files. Present the result in chat using the Output Template below.

---

## The Primary Question

> **Does this user query clearly and completely contain the intent that the advertiser expressed in the phrase-match keyword?**

Everything else is a way of answering that question. Two properties of it decide most ratings:

1. **It is directional.** The keyword is what the advertiser bought; the query is what the user typed. You test whether the *query* contains the *keyword's* intent, never the reverse. `chicken` → `fried chicken` is Good and `fried chicken` → `chicken` is Bad. Same two strings, opposite ratings.
2. **Containment is not similarity.** Two terms can be closely related and still fail, because the query drops something the advertiser paid for. Losing specificity is the single most common Bad.

## The Decision Procedure

Run these in order. The first one that fires decides. Full worked reasoning in `references/decision-procedure.md`; the complete example bank is `references/examples.md`.

**Step 1 — Confirm direction.** Identify which string is the keyword and which is the query. If the task template was filled in the wrong way round, everything below inverts. Say so rather than rating.

**Step 2 — Token containment.** Do all of the keyword's content tokens appear in the query as *whole words*, allowing inflection, plural, possessive and typo?

- **Yes** → Step 3.
- **No** → Step 4.

> Token, not character. `apple` → `apple bee` contains the token; `apple` → `applebees` does not, and the guideline rates it **Bad** with the note *"Loses the phrase 'apple' from being included in the query."* One space changes the rating. Apply this literally even though it feels orthographic.

**Step 3 — Sense check.** The tokens are there. What did the query do to them?

- Kept the keyword's sense and added detail, location, attribute, timing or proximity → **Good**.
- Rebound the token to a different entity or sense — a brand absorbing a common word → **Acceptable**. The intent *is* contained, but the advertiser may be surprised. (`church` → `churchs chicken`, `apple` → `apple bee`, `beach` → `palm beach outlets`, `apple` → `caramel apple`.)
- Query is a typo of the keyword → **Acceptable**, not Good. But a typo that lands on a real, distinct word is **Bad** (`hotel` → `hostel`).

> **Before Steps 4 and 5: is either string a brand name?** If so, jump to Step 6 — it overrides both. `raising canes` → `canes` drops a token and would fail Step 4 as a removal, but the guideline rates it **Good** because it is a system-recognized brand abbreviation.

**Step 4 — Removed, or replaced?** A keyword token is missing from the query. Which of the two happened decides the band.

- **Removed, nothing in its place** — the query is the keyword minus a modifier and is strictly broader → **Bad**, always. Intent Loss has no Acceptable band. (`sushi restaurant` → `restaurant`, `24 hour pharmacy` → `pharmacy`, `womens hair cut` → `hair cut`, `waterfront dining` → `dining`.)
- **Replaced by a different word** → Step 5.

> This distinction is load-bearing and easy to miss. `coffee shop free wifi` → `coffee shop with wifi` drops `free`, yet the guideline rates it **Acceptable** — *"keyword specified free wifi, but query is likely for the same."* A removal broadens the query; a replacement leaves it equally specific and only changes the wording. Ask whether the query would now match things the keyword excluded.

**Step 5 — Substitution quality.** The query uses different words. Are they equivalent?

- Clear, direct synonym at the **same level of generality** → **Good**. (`auto repair` → `car repair`, `coffee shop` → `coffee house`, `gas pump` → `petrol pump`.)
- Related, but with an interpretive gap → **Acceptable**. (`fitness studio` → `fitness center`, `attorney` → `lawyer`, `vegan food` → `plant based food`, `luxury hotel` → `5 star hotel`.)
- Different level of generality — a hyponym or hypernym expressed in different words → **Bad**. (`sandwich` → `turkey club`, `breakfast` → `pancakes`, `fruit` → `apple`, `thai food` → `pad thai`, `coffee` → `espresso`, `starbucks` → `coffee shop`, `sushi restaurant` → `japanese restaurant`.)
- Different intent, competing brand, or transliteration → **Bad**.

**Step 6 — Brand head/variant asymmetry.** Applies to brand names only, and **overrides Steps 4 and 5** — check it first whenever either string names a brand.

| Direction | Rating | Example |
|---|---|---|
| Head form → variant | **Good** | `mcdonalds` → `mcd`, `starbucks` → `starbux`, `raising canes` → `canes` |
| Variant → head form | **Bad** | `mcd` → `mcdonalds`, `starbux` → `starbucks` |
| Variant → different variant | **Bad** | `mcd` → `mickey d's` |
| Variant → same variant + modifier | **Good** | `mcd` → `mcd near me`, `mcd` → `epic mcd` |
| Brand → unclear reference | **Bad** | `starbucks` → `starbys`, `mcdonalds` → `mike d` |
| Same brand, different business line | **Bad** | `mcd auto services` → `mcd apparel` |

**Step 7 — When still in doubt.** The guideline's own tie-breaker:

> Lean toward Good only when containment is clear and complete. Use Acceptable when intent is likely preserved but uncertain. **Default to Bad when containment is not clear.**

## Two Places The Guideline Contradicts Itself

Both are resolved in `references/resolved-tensions.md`. Read it — an agent that applies the literal text of either passage will produce wrong ratings on common pairs.

1. **The substring baseline.** Page 2 says a keyword appearing as a complete substring in the query is *"automatically considered good."* Four of the guideline's own Acceptable examples are substring matches, and one Bad example is. Operative rule: token-level containment sets a **floor of Acceptable**, and earns Good only when the sense is preserved.
2. **Abbreviation direction.** Page 2 rates `lux hotels` → `luxury hotel` **Good** as "abbreviation to full form." Pages 5–6 rate variant → head form **Bad**. Operative rule: the head/variant asymmetry is defined over **brand names**; generic descriptors are not brands. Flag any pair that turns on this.

## Research

This task is far lighter on research than the maps families. Most pairs are decidable from the two strings and ordinary language knowledge. Look something up when, and only when:

- A term might be a brand you do not recognise (`daves hot chicken`, `raising canes`, `buw`). Whether a string is a brand changes which step applies.
- A category term's scope is genuinely unclear in the market (the guideline's own `luxury hotel` note cites a definition covering "5-star and above").
- A non-English string needs translation or transliteration identification.

Do not research your way into a rating the text does not support, and never claim a lookup you did not run.

## Output Template

One block per pair, in task order. No preamble, no summary table unless asked.

```
Pair N — <keyword> → <query>
Rating: <Good | Acceptable | Bad>
<comment>
```

The comment follows `references/comment-style.md`: one or two plain sentences naming the relationship and what it does to the intent. For a Bad rating, name both intents.

## Pre-Submission Audit

Answer in writing before any rating reaches chat:

1. Which string is the keyword and which is the query? Have I tested containment in that direction only?
2. For every Good: are the keyword's tokens present as whole words, or is this a clear same-level synonym?
3. For every Good on a brand pair: is the keyword the head form?
4. For every Acceptable: what specifically is uncertain? "Roughly related" is not an answer.
5. For every Bad: have I named both intents?
6. Did I import a rule from Broad Match or Close Variants? Transliterations, synonyms and abbreviations are where that happens.
7. Did any pair turn on one of the two known contradictions? If so, did I flag it?
