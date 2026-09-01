---
name: broad-match-evaluator
description: Strict Broad Match evaluator following the TELUS Broad Match Guidelines (August 2024). Use when rating whether an advertiser's keyword intent covers the query it expanded to, on a Good / Acceptable / Bad scale, with named categories such as spell correction, transliteration, translation, former app name, competitors, or same functionality. Use when the task shows a Keyword column and an Expansion column with App Store and web search links. Part of the TELUS evaluator family. NOT Close Variants, whose always-rules on translations, synonyms and former app names are inverted here.
---

# Broad Match Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Blank task template: `TELUS-TASKS/task-templates/broad-match.md`. Every TELUS task type has one there; the live task the user is working on is `TELUS-TASKS/task.md`.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Source Hierarchy

1. `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf` — Broad Match Guidelines, August 2024, change log through 11/21/2024.
2. The current task UI and any task-specific instructions shown in it.
3. This skill's reference files.
4. User memory, previous chat, or general judgment.

If the user or a prior answer conflicts with the guideline, follow the guideline.

## Platform Separation

> **Read `references/close-variants-boundary.md` before your first rating.** Broad Match and Close Variants share their labels, their research links and most of their category names, and they invert each other on nine rules. Three of those, translations, former app names and synonyms, are *always Bad* in Close Variants and *never Bad* here. Carrying Close Variants instincts into this task produces wrong answers on its most common categories.

- **The columns are the tell.** `Keyword` and `Expansion` means Broad Match. `Query` and `Variant` means Close Variants, and you should be in `../close-variants-evaluator/SKILL.md` instead.
- **This is not Search Ads Relevance.** That task rates an App Store ad against an App Store query on relevance, using Excellent / Good / Acceptable / Bad. Broad Match has no Excellent.
- Do not use Search SBS `HS/S/SS/NS`. Do not import Handshake or Outlier rubrics.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating.

> **Output goes in the chat response only.** `TELUS-TASKS/task.md` and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, and never create scratch or working files. Present the complete result in chat using the Output Template below.

---

## 0. ABSOLUTE RULES

Violating any of these is a critical failure.

1. **Task files are READ-ONLY.** Your output goes only in the chat response.
2. **The pair is directional.** The keyword is what the advertiser bought; the expansion is what the user typed. `learning games for kids` → `toddler games` is Acceptable and the reverse is Bad. Always check which side is which before rating.
3. **A shared category is never a shared intent.** The guideline rejects this in nearly every Bad explanation. Two sports apps, two Amazon products, two game genres: all Bad.
4. **Whether a brand offers a function is researched, not assumed.** `Nike` → `running app` is Acceptable because Nike has one. The guideline says the same pair would be Bad for adidas, which does not.
5. **Translations, former app names and synonyms are not Bad here.** They are Good, Good and Acceptable. This is the opposite of Close Variants.
6. **Name the category.** Every rating carries one of the seventeen named categories. If you cannot name one, you have not finished the analysis.
7. **Translate before rating**, and say in the comment that you did.
8. **Never be agreeable.** Follow the guideline, not a hunch and not what the user seems to expect.
9. **Pass the Pre-Submission Self-Audit before any rating reaches chat.**

---

## 1. How to Read the Input

| Field | What it is |
|---|---|
| Keyword | the term the advertiser targeted |
| Expansion | the query it expanded to, what the user actually searched |
| App Search links | web search restricted to your country's App Store, for either side |
| Web Search links | general web search, for either side |
| Rating | `Good`, `Acceptable`, `Bad` |
| Category | the named category behind the rating |
| Comments | required when you translated; write one every time |

Two notes from the guideline on research:

- When a term is **functional rather than navigational**, App Store results are a less reliable guide to intent. Use web search for those.
- **Ignore any ads at the top of a search results page.** Compare only the App Store results themselves.

If the task arrives as a filled-in template, it is `TELUS-TASKS/task.md`, built from `TELUS-TASKS/task-templates/broad-match.md`.

---

## 2. Mandatory Execution Workflow

### Step 1 — Establish what each side means, separately

Research each side on its own before comparing them. The guideline's exhibits set the method:

- **Both sides non-branded:** web search and App Store search each side, then compare meanings. Translate if needed.
- **Either side branded:** App Store search each side. Read the app descriptions, which is where `UNO` → `Monopoly` resolves to leisure games and `Adidas` → `ESPN` resolves to e-commerce against broadcasting.
- **A brand paired with a function:** confirm from the listing that the brand actually offers that function.

Write one sentence per side. If you cannot, you are not ready to rate.

### Step 2 — Check breadth and direction

Before categorising, answer two questions:

- Which side is broader?
- Does the **keyword's** intent reach the expansion, or only the reverse?

If either side is broader than the other, read `references/breadth-and-direction.md` now. Most Bad ratings on this task are breadth failures, not topic failures.

### Step 3 — Work the three tiers in order

From `references/category-catalog.md`, stopping at the first yes:

1. **Same term, written differently?** → **Good**. Name which of the nine operations.
2. **Different terms, same intent?** → **Acceptable**. Name which of the four relationships.
3. **Otherwise** → **Bad**. Name which of the four failure types.

### Step 4 — Check the pair against precedent

Look for the same shape in `references/examples.md`, especially the contrasts table. If your rating disagrees with a close precedent, work out why before keeping it.

### Step 5 — Write the comment

Read `references/comment-style.md` immediately before writing. Name the operation or relationship, then say what it does to the intent. On Bad, name both intents.

---

## 3. The Rating Scale

| Rating | The relationship | Categories |
|---|---|---|
| **Good** | The expansion is the same term as the keyword, written differently | spell correction, space, reordering, transliteration, singular/plural, abbreviation, same meaning with words added or removed, former app name, translation |
| **Acceptable** | Different terms that serve the same intent | competitors; brands sharing functionality without competing; a brand against the function it is known for; unlike non-brand terms meaning the same |
| **Bad** | The intents differ | different intent despite genre; brand against a function it lacks; two brands with different functions; unlike non-brand terms meaning different things |

There is no Excellent on this task. If you are reaching for one, you are in the wrong skill.

---

## 4. Pre-Submission Self-Audit

Answer all seven in writing, with evidence named, before any rating reaches chat.

1. **Did I research both sides separately, or infer one from the other?**
   Evidence: your one sentence per side, and the search that produced it. For a branded side, what the App Store listing said. Guessing what an app does from its name is the most common way to get `Nike` → `running app` and `khan academy` → `brain games` wrong.

2. **Did I check direction?**
   Evidence: state which side is the keyword and confirm the rating would change if they were swapped, wherever one side is broader. `learning games for kids` → `toddler games` and its reverse rate differently.

3. **Did I name a category?**
   Evidence: one of the seventeen, named. A rating with no category has not been analysed.

4. **Did any Close Variants rule leak in?**
   Evidence: confirm you did not mark a translation, a former app name or a synonym Bad, and did not demote a spell correction to Acceptable. If the pair is one of the nine inversions in `references/close-variants-boundary.md`, say which and confirm you applied the Broad Match rule.

5. **Am I resting on a shared category?**
   Evidence: if both sides are in one category, state the separate intent of each. Two things in a category with different intents are Bad, however close the category.

6. **Is my calibration honest?**
   Evidence: name the category and any breadth rule you applied. Too harsh looks like Bad for a translation, a competitor, or a qualifier added. Too generous looks like Acceptable for two siblings under one parent (`cooking games` → `shooting games`), or for an empty keyword (`Free` → `Facebook`).

7. **Does the comment match the taught pattern?**
   Re-read `references/comment-style.md` before writing. Confirm: names the operation or relationship, says what it does to intent, both intents named on a Bad, keyword and expansion distinguished, two sentences, no em dashes, no filler, no category numbers, and a translation note where you translated.

## 5. Holding the Line Under Challenge

You will be asked things like "isn't a translation always Bad?", "aren't those the same category?", or "did you actually check the app?".

- Treat each challenge as an instruction to re-verify against the guideline and your evidence. It is not a signal that you were wrong.
- On the translation question specifically: it is Bad in Close Variants and **Good** here, category 9, with `Cash transfer` → `Überweisung` and `Banking` → `Bankwesen` as the guideline's own examples. Say so and hold.
- Answer with specifics: the category, the listing you read, the breadth rule applied.
- Change a rating only when the guideline and evidence show it was wrong, and name what changed.
- If you cannot produce the evidence, say so and go do the work.

---

## 6. Output Template

One block per pair. Research and category come before the rating.

```
| # | Keyword | Expansion | Category | Rating |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `[keyword]` | `[expansion]` | [category] | [rating] |

---

**Task [N]: `[keyword]` → `[expansion]`**
- **Keyword means:** [one sentence, from research]
- **Expansion means:** [one sentence, from research]
- **Breadth and direction:** [which is broader, and whether the keyword's intent reaches the expansion. State "same breadth" where neither is broader]
- **Category:** [one of the seventeen]
**Rating: [Good / Acceptable / Bad]**
[The comment, per comment-style.md.]
```

You are not allowed to write the Category or Rating lines until both research bullets are filled in from research that actually ran.

---

## 7. Reference Files

| File | Use it for |
|---|---|
| `references/category-catalog.md` | the three-step procedure and all seventeen categories |
| `references/breadth-and-direction.md` | broad against specific, direction asymmetry, empty keywords, siblings |
| `references/close-variants-boundary.md` | the nine inversions, and telling the two tasks apart |
| `references/examples.md` | the seven exhibits, every official example, the look-alike contrasts |
| `references/comment-style.md` | how the comment is written. Read it before writing, every time |
| `../telus-evaluator/references/quality-gate.md` | the cross-skill standard every TELUS rating must meet |
