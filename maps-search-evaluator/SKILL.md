---
name: maps-search-evaluator
description: Evaluate TELUS Maps Search Evaluation tasks. Use when rating map search results for Relevance, Name/Category Accuracy, Address Accuracy, and Pin Accuracy; when the task shows a query, viewport, user location, and result pins on a map; or when the task mentions Search 2.0, Search Relevance, navigational result, PERMANENT_CLOSURE, or viewport age (fresh/stale).
---

# TELUS Maps Search Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and say plainly that the official source was unavailable.

## Source Hierarchy

1. The rendered official PDF page: `TELUS-TASKS/Maps Search Evaluation/telus - Maps Search Evaluation Guidelines.pdf` (March 2025, 278 pages), including its tables, screenshots, and labels.
2. The current task UI and any visible task-specific instructions.
3. `TELUS-TASKS/maps-extracted/text.md` as a search and navigation aid only.
4. This skill's reference files.
5. User memory, previous chat, or general judgment.

The extraction loses table cells, labels, and layout in places. It locates content; it never overrides a rendered page. If the user or a prior answer conflicts with the guideline, follow the guideline.

## Platform Separation

- Maps rules apply to TELUS Maps tasks only. Do not import Handshake or Outlier rubrics.
- Do not use Search SBS `HS/S/SS/NS` labels here. Maps has its own relevance scale.
- Do not borrow another TELUS task's scale, flags, or comment style.

> **Output goes in the chat response only.** Task files and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, and never create scratch or working files. Present the complete result in chat using the Output Template below.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating. It governs evidence honesty, individual rating, calibration, and holding the line under challenge.

## Required Task Inputs

Before rating, read and record every input the task actually provides:

| Input | Where | If missing |
|---|---|---|
| Query | Query header | Cannot rate — release for technical reasons |
| Task type (Search 2.0 / Search Relevance) | Task bar | Infer from which rating fields the UI shows |
| Locale | Query header | Defer to Locale over the Country field if they disagree |
| Viewport age (FRESH green / STALE red) | Query header | Treat the viewport as fresh |
| User Lat,Lng | Query header / blue-white icon | See the location-intent table in `references/user-intent.md` |
| User viewport | Purple box on map | See the location-intent table |
| Result name/title, address, category, status | Result block | Note which fields are absent |

Measure distance from the **outer edge of the user viewport**, not from the device icon. The device icon only helps you find the viewport and has no rating significance. A pin's **tip** marks the location; the head is only an indicator.

Information in the pop-up box (phone, URL, coordinates) is for research only. Rate only the information in the result itself. **Never call a business.**

## Missing Evidence

- If research cannot settle whether a business is closed, assume it could exist and rate Name, Address, and Pin as `Can't Verify` — unless there is an obvious data issue such as a missing mandatory address component or a pin in the ocean, which stays rateable.
- Never claim you checked a page or map that you did not check.
- Search snippets alone are not proof.
- State the limitation in the output rather than inventing a rating.
- Some results appear normal or greyed out with **no rating fields**. No rating is required for them. This is expected and is not a technical issue or a reason to release.

## The Rating State Machine

Work these in order. Each step says what to do next, including when to stop.

**Query level — once per task**

1. **Confirm the platform and task.** TELUS Maps Search Evaluation, not Handshake, Outlier, or another TELUS family. If it is not Maps, stop and route via `../telus-evaluator/SKILL.md`.
2. **Determine the task type.** Search Relevance rates relevance only. Search 2.0 also rates Name and Category Accuracy, Address Accuracy, and Pin Accuracy.
3. **Inventory the fields the UI actually requests.** For any result you may be asked for all ratings, some, one, or none. Rate only what is shown. Never invent a rating for a field the UI does not offer.
4. **Read the query inputs.** Query, locale, user location, viewport, viewport age — per the table above.
5. **Classify the query and determine location intent.** Query type and the full viewport/user-location decision table are in `references/user-intent.md`. Explicit location in the query overrides viewport and user location. "Near me" uses user location and ignores the viewport even when fresh. If the query has **no maps intent**, every result is rated `Bad`.
6. **Answer the query-level navigational question once.** "Is there a navigational result for this query?" — `Yes` when exactly one real-world result could completely satisfy the intent; `No` when more than one could. Answer it **before** looking at results, and answer it even when the task shows no results at all.

**Result level — repeat for every result**

7. **Check unexpected language or script first.** Judge the result **name/title** only, not the address details beneath it. Expected = language/script of the test locale, the query, the result region, any combination of those, or an official brand/chain name used in that market. Missing or added diacritics are not an unexpected-language issue.
8. **If unexpected language applies → select the checkbox and STOP this result.** Every other field becomes unavailable. Do not rate relevance or any data dimension. Move to the next result.
9. **Research closure and actual existence.** Always research the real-world state regardless of what the status field shows. Treat a temporary closure as open when the business announces it on its own webpage or managed social account — there is no time limit on this. Distinguish genuinely closed/non-existent from a result whose name or address is merely wrong; the latter is a data-accuracy problem, not a closure.
10. **Apply the closed/non-existent checkbox only when the evidence supports it.** It applies to business/POI results only, never to address-type results. Use it for closed/non-existent entities, randomly moving entities such as an unscheduled food truck, and non-recurring past events with no remaining maps intent. **If you check it, only relevance remains rateable** — do not produce Name, Address, or Pin ratings. When the status shows `PERMANENT_CLOSURE`, the relevance rating depends on whether the result is expected or unexpected; follow `references/result-level-issues.md`.
11. **Rate relevance, independently of data accuracy.** Always assume the result exists and its displayed data is correct, even when research proved otherwise. Closure alone is never grounds for `Bad`. Rate against the real world: if a better result exists but is not shown, demote the shown results accordingly. Ignore result order and never demote for duplication. Any rating of `Good` or below requires a demotion checkbox and a comment.
12. **Rate each requested data dimension independently — Search 2.0 only, and only if step 10 did not gate them.** Name and Category Accuracy, Address Accuracy, Pin Accuracy. Each is judged on its own evidence; a pin can be correct while the address is wrong. If Pin Accuracy is `Perfect`, answer the follow-up "Does the available evidence indicate the result's precise location?" with `Yes` or `No`.
13. **Write the mandatory comments.** Required for any relevance rating of `Good` or below, and for any data rating that is not `Correct` or `Perfect`.

**Before submitting**

14. **Run the pre-submission audit** (below).
15. **Present the complete result in chat** using the Output Template.

## Rating Scales

**`references/rating-contract.md` is the single authority for every label, checkbox, and field-hiding rule. Always read it before rating.** If a label is not in that file, it is not a UI option — do not use it. The summary below orients you; the contract governs.

**Relevance** — `Navigational` · `Excellent` · `Good` · `Acceptable` · `Bad`
Demotion checkboxes, mandatory at `Good` or below: `User Intent issue`, `Distance/Prominence issue`. How to decide: `references/relevance.md`.

**Name and Category Accuracy** — `n/a` · `Correct` · `Partially Correct` · `Incorrect` · `Can't Verify`
Issue checkboxes: `Name Issue`, `Category Issue`. An incorrect category forces `Incorrect` regardless of the name. How to decide: `references/name-category-accuracy.md`.

**Address Accuracy** — a parent rating of `Correct` · `Correct with Formatting Issue` · `Incorrect` · `Can't Verify`, plus checkboxes under `Incorrect` naming the faulty component(s) and/or the issue (`Address does not exist`, `Language/Script Issue`, `Country-Specific Issue`, `Other Issue`). Those issues are **not** top-level ratings. How to decide: `references/address-accuracy.md`.

**Pin Accuracy** — `Perfect` · `Approximate` · `Next Door` · `Wrong` · `Can't Verify`
There is no `Acceptable` pin rating. A missing pin is `Wrong`; if pins are missing five or more times in a row, release for technical reasons and explain in the comment. `Perfect` triggers the precise-location follow-up. How to decide: `references/pin-accuracy.md`.

## Comment Requirements

- State the user intent you concluded.
- Name the guideline section behind the demotion.
- Give the correct information and its source when you found something wrong; link directly to the evidence, and use a URL shortener for long links.
- Be short and specific.
- Write in English regardless of test locale.
- Never include PII — no names, contact details, account numbers, or private data.

Full trigger list in `references/rating-contract.md`.

## Release Survey

Summarised here because it is a hard gate; `references/rating-contract.md` is authoritative.

Release only when a technical or other issue genuinely prevents rating: `Adult Content`, `Technical Issue`, `Not Enough Time Allocated`, `Other`.

Do **not** release because the rating is hard, because the query looks unrelated to maps (rate all results `Bad`), because the query or results are outside your market, because the query returned no results (still answer the navigational question and submit), or because the query is in a foreign language (research or translate it).

## Pre-Submission Audit

State each of these in the output before presenting ratings:

1. Task type identified and requested dimensions inventoried.
2. Query classified and location intent determined.
3. Navigational question answered exactly once.
4. Every result evaluated independently.
5. Unexpected-language and closure gates checked before any rating.
6. Relevance separated from data accuracy.
7. Exact rating labels used.
8. Every `Good`-or-lower relevance rating carries a demotion checkbox and a comment.
9. Every non-`Correct`/non-`Perfect` data rating carries a comment.
10. Pin ratings drawn from the full five-level scale.
11. Missing or unusable evidence disclosed.
12. No rating invented for a hidden or unavailable field.
13. TELUS quality gate passed.

## Output Template

The template is **conditional**. Render only what the task actually offered:

- Search Relevance task → omit the Name/Category, Address, and Pin lines entirely.
- A dimension the UI did not request → omit that line.
- `Unexpected language or script` checked → render the issue line and nothing else for that result.
- `Closed or does not exist` checked → render relevance, then `Data dimensions: gated by closure checkbox` in place of the three data lines.
- Pin not rated `Perfect` → omit the precise-location follow-up.
- Result shown with no rating fields → one line saying so; no ratings.

Never render a line with a guess, a dash, or "N/A" where a gate or the UI removed the field. State the gate instead — an omission a reviewer can see is the point.

```
**Task Type**: [Search 2.0 / Search Relevance]
**Query**: [the query]
**Query Type**: [address / POI / business / category / product-service / coordinate / emoji / routing / no-maps-intent]
**Locale**: [locale]
**User Location**: [present / missing]
**Viewport**: [fresh / stale / age missing / absent] — [user inside / outside / unknown]
**Location Intent**: [conclusion] — [why]
**Navigational Result?**: [Yes / No] — [why]
**Evidence Limitations**: [none, or what could not be verified]

---

**Result [#]**: [result name/title]
- **Result-Level Issues**: [none / unexpected language — STOP / closed or does not exist]
- **Relevance**: [Navigational / Excellent / Good / Acceptable / Bad] — [demotion checkboxes if Good or below]
- **Name & Category Accuracy**: [label] — [Name Issue / Category Issue if applicable]
- **Address Accuracy**: [label] — [component(s) if Incorrect]
- **Pin Accuracy**: [Perfect / Approximate / Next Door / Wrong / Can't Verify]
  - *Precise location evidence?*: [Yes / No]  ← only when Perfect
- **Comment**: [required if any demotion; intent, guideline section, corrected info + source]
- **Evidence**: [what you actually checked]

[Repeat per result. Omit any line the UI did not request or that a gate made unavailable.]

---

**Pre-Submission Audit**: [confirm the 13 points]
```

## References

Load these deliberately rather than all at once.

**Always read, every task:**

| Reference | Covers |
|---|---|
| `references/rating-contract.md` | Every exact label, checkbox, and field-hiding rule. The authority — no label exists unless it appears here |
| `references/user-intent.md` | Query types, explicit vs implicit location, the viewport/user-location decision table, "near me" |

**Read when the situation calls for it:**

| Reference | Read it when |
|---|---|
| `references/query-family-playbook.md` | Always — go straight to the branch matching this query family (Chapters 10–11) |
| `references/result-level-issues.md` | Unexpected language applies, or anything about closure or `PERMANENT_CLOSURE` |
| `references/research-evidence.md` | Deciding what proves a rating, or evidence has run out |
| `references/relevance.md` | Working out a relevance demotion — connection types, prominence, distance, viewport, rural areas, transit, parking, service-level mismatch |
| `references/name-category-accuracy.md` | Name/Category is requested — name sources, misspelling severity, location modifiers, category rules |
| `references/address-accuracy.md` | Address is requested — components, result-type expectations, features without addresses |
| `references/pin-accuracy.md` | Pin is requested — rooftops, property boundaries, campus, entrance polygons, transit, parking, shared spaces |
| `references/calibration-examples.md` | Only when a call is genuinely borderline and you want a worked case to check against |

**Tool:** `../tools/maps_distance.py` computes straight-line distance between coordinates. It informs a rating; it never decides one.

Full extracted source for lookups: `TELUS-TASKS/maps-extracted/text.md` (14,038 lines, 367 images). It is a search aid — a rendered PDF page always outranks it.
