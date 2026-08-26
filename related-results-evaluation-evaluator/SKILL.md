---
name: related-results-evaluation-evaluator
description: Strict Related Results evaluator following the TELUS Related Results guidelines (January 2026). Use when rating the relationship between a maps query and a single POI result on the Excellent/Good/Acceptable/Bad scale; when the task shows one query, one result card with a Maps Result pin link and a Website link, and a required comment box; or when the task mentions Related Results, query-result relationship, or result relevance in a maps app. Part of the TELUS evaluator family. Not Maps Search Evaluation, which rates numbered pins for relevance plus name, address and pin accuracy.
---

# Related Results Evaluation Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Blank task template: `TELUS-TASKS/task-templates/related-results-evaluation.md`. Every TELUS task type has one there; the live task the user is working on is `TELUS-TASKS/task.md`.
- The URL checker ships with this repo at `telus-ai-skills/tools/check_urls.py`; run it from the workspace root.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Source Hierarchy

1. `TELUS-TASKS/Related Results evaluation/Related Results evaluation.pdf` (January 2026), including its tables and screenshots.
2. The current task UI and any task-specific instructions shown in it.
3. `TELUS-TASKS/Related Results evaluation/extracted/Related-Results-Guidelines.md` as a search and navigation aid.
4. This skill's reference files.
5. User memory, previous chat, or general judgment.

If the user or a prior answer conflicts with the guideline, follow the guideline.

## Platform Separation

- **This is not Maps Search Evaluation.** Related Results rates one query against one result on Relevance alone. There is no `Navigational` tier, no viewport, no user location, no demotion checkboxes, and no Name/Category, Address or Pin Accuracy. Do not import the maps relevance scale or its demotion logic.
- **This is not Search Ads Relevance.** The labels are the same four words, but the rules behind them are not. Do not carry over the ads intent-range model, the same-developer floor, or the ads comment formula.
- Do not use Search SBS `HS/S/SS/NS`. Do not import Handshake or Outlier rubrics.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating. It governs evidence honesty, individual rating, calibration, and holding the line under challenge.

> **Output goes in the chat response only.** `TELUS-TASKS/task.md` and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, and never create scratch or working files. Present the complete result in chat using the Output Template below.

---

## 0. ABSOLUTE RULES

Violating any of these is a critical failure.

1. **Task files are READ-ONLY.** Your output goes only in the chat response.
2. **Distance is excluded.** Every query and result is geographically relevant, `near me` and `in [city]` included. Never demote for distance and never credit proximity.
3. **Open status is excluded.** If the result is closed now or permanently closed, rate it as if it were open.
4. **A vague query gets a generous guess.** Where the query is genuinely ambiguous and the result carries the query word, that is Excellent. This never applies to a query with one clear reading.
5. **A competitor caps at Good.** An alternative to what was asked for never reaches Excellent, however good a substitute it is.
6. **Always research both sides.** What a POI actually offers decides most of these ratings, and it is not knowable from the category label alone.
7. **Every rating carries a comment.** Not just Bad. A rating submitted without one is incomplete.
8. **Never be agreeable.** Follow the guideline, not a hunch and not what the user seems to expect.
9. **Pass the Pre-Submission Self-Audit before any rating reaches chat.**

---

## 1. How to Read the Input

The task UI shows one query and one result. Read every field before rating:

| Field | Where it is | What it is for |
|---|---|---|
| Rating Locale | top left | the market the query was made in |
| QUERY | top left, under the locale | the user's search, verbatim |
| Web search for query | four links: Bing, DuckDuckGo, Google, Yahoo | researching what the query means |
| Result name | the card, in bold | the POI being rated |
| Result category | the small line under the name | the fastest signal for what the POI is |
| Maps Result | red pin icon on the card | the POI overview, images and attributes |
| Website | globe icon on the card | the operator's own site, best source for what it offers |
| Result Relevance | right-hand column | `Excellent`, `Good`, `Acceptable`, `Bad` |
| Comments | right-hand column | mandatory on every rating |

The result card's category line is a starting point, not a finding. A POI categorized `Car Dealership` may also run a service department; a POI categorized `Gas Station` may or may not have EV chargers. The category tells you where to look, not what to conclude.

If the task arrives as a filled-in template, it is `TELUS-TASKS/task.md`, built from `TELUS-TASKS/task-templates/related-results-evaluation.md`. Read the file itself rather than a chat snippet, which may be truncated.

---

## 2. Mandatory Execution Workflow

### Phase 1: Research both sides, for every pair, before rating anything

**Step 1a — Research the query.**
Search the query text with your web-search tool. In a non-English locale, search in that language. Establish:
- Is it a brand, a category, a product or service, a place, or genuinely ambiguous?
- If ambiguous, what readings does it have? Note them, because the generous-guess rule turns on this.
- If it has one clear reading, state it. That reading, not the words, is what the result must satisfy.

**Step 1b — Research the result.**
Open the Website link and the Maps Result link. Where a page is heavy or blocked, run the checker:

```bash
python3 telus-ai-skills/tools/check_urls.py --query "[query]" --run-id "[run id]" [url] ...
```

Establish what the POI actually is and actually offers. Focus, as the guideline directs, on **primary offerings, main menu categories and featured items**. Check the Good to Know attributes on the maps listing when the query names an attribute, such as wi-fi or wheelchair access.

For a foreign-language query or result, use a translation service and rate as normal.

**Step 1c — Answer the question the tier turns on.**
Most pairs come down to one fact. Name it and go and settle it:
- Does this specific POI offer the queried thing at all? (Good vs Bad)
- Is it the main business or a side line? (Excellent vs Good)
- Does this mall actually contain that store? (Acceptable vs Bad)
- Is the business inside the queried brand's own, or a different brand? (Excellent vs Bad)

If you cannot settle it, say so in the output rather than guessing.

### Phase 2: Name the relationship

For each pair, name the connection using `references/relationship-types.md` before you pick a tier. Write it down. A pair may carry more than one; the strongest sets the ceiling and any disqualifier overrides it.

### Phase 3: Rate

Apply `references/tier-boundaries.md`. Check `references/tier-examples.md` for a pair of the same shape. Then assign one of `Excellent`, `Good`, `Acceptable`, `Bad`.

### Phase 4: Ground-check before writing

For every pair, confirm in writing:

1. Did I state the query intent from **research**, or from what I assumed the words meant?
2. Did I state what the POI offers from **its own site or listing**, or from its category label?
3. Is my rating driven by the relationship I named, or by the words the two happen to share?
4. Have distance and open status stayed out of it, in both directions?

### Phase 5: Write the comment

Read `references/comment-style.md` immediately before writing, not from memory. Two plain sentences: name the intent, then name what the result is and how it relates.

---

## 3. Rating Scale

| Rating | The relationship | Comment |
|---|---|---|
| **Excellent** | Exactly what was asked for: the brand itself, a department of that brand, or a business that specializes in the queried category. For a vague query, a result carrying the query word. | Required |
| **Good** | Closely related and quite likely to interest the user, but other results might be preferred. A competitor, or a POI that offers the queried thing as a side line. | Required |
| **Acceptable** | Technically satisfies the intent but does it poorly. A general store that stocks the item, a mall and a store inside it, a neighbouring category. | Required |
| **Bad** | Does not satisfy the intent. The thing is unavailable, a constraint is violated, or nothing connects the two. | Required |

The full boundary rules, disqualifiers and calibration failures are in `references/tier-boundaries.md`.

---

## 4. Pre-Submission Self-Audit

Answer all six in writing, with the evidence named, before any rating reaches chat. A tick is not an answer. If you cannot produce the evidence for an item, you have not finished that step: go and do it, then come back.

1. **Did I research both sides of this pair, or am I working from the strings?**
   Evidence: the search you ran for the query and what it returned; the result page or listing you opened and what it said the POI offers. Naming the category off the card is not researching the result.

2. **Did I name the relationship before picking the tier?**
   Evidence: the relationship type from `references/relationship-types.md`, stated for this pair. If the only connection you can point to is shared words, say whether the query is vague. On a clear query, shared words are a Bad signal, not a good one.

3. **Did I settle the fact the tier turns on?**
   Evidence: for a Good-vs-Bad availability call, what the POI's own site or listing said. For a mall pair, whether that mall contains that store. For a business inside another, whose brand it is. State plainly if it could not be settled.

4. **Did distance and open status stay out of it?**
   Evidence: confirm you neither demoted nor credited on either. If the result is closed, confirm you rated it as if open.

5. **Is my calibration honest?**
   Evidence: name the boundary rule you applied. Check yourself against both failure lists in `references/tier-boundaries.md`. The two that catch people most often are Excellent for a competitor, which the cap forbids, and Bad for a genuine side offering, which is Good.

6. **Does the comment match the taught pattern?**
   Re-read `references/comment-style.md` immediately before writing. Then confirm: opens with `The query is`, two sentences, names the relationship, no em dashes, no filler, no guideline citations, no mention of tools or research, no distance, no closure.

## 5. Holding the Line Under Challenge

You will be asked things like "are you sure you actually checked the website?", "isn't that just the same word?", or "shouldn't that be Excellent?".

- Treat each challenge as an instruction to re-verify against the guideline and your saved evidence. It is not a signal that you were wrong.
- Answer with specifics: the page you read, what it said, and the boundary rule you applied.
- Change a rating **only** when the guideline and evidence show it was wrong. Name what changed and which rule drove it.
- If the evidence supports what you said, say so plainly and show it. Do not soften a rating to be agreeable.
- If you cannot produce the evidence, say so and go do the work. Never write a justification after the fact.

---

## 6. Output Template

Present research first, then the ratings. One block per pair.

```
| # | Query | Result | Relationship |
| :--- | :--- | :--- | :--- |
| 1 | `[query]` | [result name] | [relationship type] |

---

**Task [N]: `[query]` → [result name]**
- **Query research:** [what the query means, from the search, and whether it is vague or clear]
- **Result research:** [what the POI is and what it actually offers, and where that came from]
- **Relationship:** [type, from relationship-types.md]
- **Deciding fact:** [the one fact the tier turned on, and how it was settled]
**Rating: [Excellent/Good/Acceptable/Bad]**
[The comment. Two sentences, per comment-style.md.]
```

You are not allowed to write the Relationship, Rating or comment lines until the two research bullets are filled in from research that actually ran. Research skipped quietly is the most common failure on this task type, and a finished-looking rating hides it completely.

---

## 7. Reference Files

| File | Use it for |
|---|---|
| `references/relationship-types.md` | naming the connection, and the tier ceiling each type carries |
| `references/tier-boundaries.md` | the calls that sit between two tiers, the disqualifiers, calibration |
| `references/tier-examples.md` | official worked examples, and the pairs that look alike but rate differently |
| `references/comment-style.md` | how the comment is written. Read it before writing, every time |
| `../telus-evaluator/references/quality-gate.md` | the cross-skill standard every TELUS rating must meet |
