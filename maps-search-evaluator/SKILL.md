---
name: maps-search-evaluator
description: Evaluate TELUS Maps Search Evaluation tasks. Use when rating map search results for Relevance, Name/Category Accuracy, Address Accuracy, and Pin Accuracy; when the task shows a query, viewport, user location, and result pins on a map; or when the task mentions Search 2.0, Search Relevance, navigational result, PERMANENT_CLOSURE, or viewport age (fresh/stale).
---

# TELUS Maps Search Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Blank task template: `TELUS-TASKS/task-templates/maps-search-evaluation.md`. Every TELUS task type has one there; the live task the user is working on is `TELUS-TASKS/task.md`.
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
- **And the reverse: never apply these rules to another TELUS family.** POI Evaluation,
  Related Results, SBS and Ads Relevance have their own guidelines with their own
  numbering, and a shared dimension name does **not** mean a shared scale. Two measured
  divergences, both of which produced wrong answers when Maps rules were applied to a POI
  Evaluation task:

  | Question | Maps Search | POI Evaluation |
  |---|---|---|
  | Overly broad category | `Correct` (§6.3.1) | **`Approximate`** (§9.1) — a band Maps lacks |
  | Official website vs claimed social account disagree | peers; prefer the more recent | **website wins** (§10.1.1.2) |

  POI Evaluation also rates **Hours**, a dimension Maps Search does not have at all.
  If the task in front of you is a single listing with no query, stop and use
  `../poi-evaluation-evaluator/SKILL.md` — it carries POI's own scales, and its
  `references/maps-vs-poi.md` maps every divergence between the two families.

> **Output goes in the chat response only.** Task files and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, and never create scratch or working files. Present the complete result in chat using the Output Template below.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating. It governs evidence honesty, individual rating, calibration, and holding the line under challenge.

## Mandatory Recon Gate

**Run this before rating anything. A rating produced without it is not submittable.**

```bash
python3 telus-ai-skills/maps-search-evaluator/scripts/maps_recon.py <task>.json
```

Build the task file from the result cards — see `scripts/task.example.json`. The script runs Phases 0–3 in one pass: it derives location intent, reverse-geocodes every pin, sweeps the real-world candidate set, ranks everything from the intent, and batches the page fetches through `check_urls.py`. It writes an evidence bundle and prints a **RUN ID**.

**Your output must quote that RUN ID and the Phase 3 ranking table.** If you cannot quote them, you did not do the research — go and do it. This is not a style preference: research skipped silently is the single most common failure on this task type, and it is invisible in a finished-looking rating.

The script **refuses** rather than guessing when an input that changes the rating is missing:

| Refuses when | Because |
|---|---|
| `user_in_viewport` is null on a FRESH viewport | inside-vs-outside inverts the whole rating; only the Show All frame settles it |
| `explicit_location` set without `intent_coords` | candidates must be ranked from the stated place, not from the user |
| a BUSINESS result has no `url` and no `url_unavailable` reason | Phase 1 is **per result**. A brand locator index does not stand in — a chain delists a closed store silently, so absence there is no signal at all |

`references/research-workflow.md` carries the full detail — the fallback ladder for blocked sources, and how to read a reverse-geocode result. Read it when the script reports something you cannot interpret.

**If you change `maps_recon.py`, run `scripts/test_maps_recon.py` before using it.** It takes under a second and covers the logic that has broken before: bot walls counting as reads, the rebrand check keying on text it did not own, and the viewport fallback measuring the wrong set. **Do not fix the script in the middle of a rating** — note the defect, finish the task, fix it after.

### Four rules the script cannot enforce for you

1. **Read the saved page, never the status code.** A `200` on a parked or hijacked domain is evidence of nothing. A real case: a coffee shop's apparent official domain now serves gambling spam, and an agent cited it as confirming the menu.
2. **A search snippet is not proof.** Directory prose like "serves breakfast and lunch" does not establish what a business actually offers. Open the menu.
3. **Cite nothing you did not open.** Every URL in an evidence line must appear in this run's `report.json` and have been read. Claiming a check you did not perform is the critical failure in the quality gate.
4. **Batch your own lookups.** The script parallelises its fetches; it cannot parallelise yours. When it finishes, the open questions — is this result trading, does it actually sell the queried product, what is the official name — are independent of each other. Fire them **together in one message**, then read the answers back together. Searching one at a time and thinking in between has been the single largest time cost on real tasks. Full list of what is ever left open: `references/research-workflow.md` → *Batch your own lookups*.

### Location intent — the first thing decided, and the most often wrong

The script computes this, but you must be able to defend it. Work top-down, stop at the first match:

1. **The query names a place** — a locality, full address, street or named POI → that place is the intent. **Ignore the user location and the viewport entirely**; both distance columns become irrelevant.
2. **The query says "near me" / "my location"** → user location, ignoring the viewport even when FRESH.
3. **Otherwise** → the decision table in `references/user-intent.md`.

Rule 1 is the commonest way a Maps rating goes wrong: demoting an exact-match result for sitting far from a user the query never referred to. The guideline lists it as a "common wrong answer" in its own right.

### Decided cases outrank your reasoning

Before forming any view on relevance, look the query/result **shape** up in `references/decided-cases.md`. The guideline has already ruled on the common ones, and those rulings are not open to re-argument.

The failure this prevents: building a plausible case from first principles and letting it override a worked example that already considered — and rejected — the exact argument. `[costco]` returning "Costco Gasoline" is **Bad**, and the guideline says so *while acknowledging* that the two share an address and a brand name. "Same address", "same brand", and "it's inside the thing they asked for" are all explicitly overruled defences.

If you find yourself explaining why a decided case should not apply here, stop. That reasoning is the error.

> **Searching the source needs care.** `TELUS-TASKS/maps-extracted/text.md` uses non-breaking spaces, so `grep "Rate Bad"` returns **zero hits** despite seven Bad rulings. Use the normalising recipe in `decided-cases.md`.

### US addresses — check USPS before demoting

On a US task, a result address that disagrees with the operator's official website is
**not** by itself a fault. USPS routinely recognises both forms. When the difference is
the **locality, postal code, cardinal direction (E/W/N/S) or street type (Blvd/St, Rd/Dr)**,
you must check USPS and rate on what it returns for the *result* address — not on the
website. In the guideline's own five worked cases, **three rate `Correct` despite
contradicting the official site.**

Any other kind of difference is `Incorrect` + component, with no USPS check needed. Full
rules, the component matrix and the US addressing systems: `references/us-address-verification.md`.

### Category fit for product and service queries

`[breakfast]`, `[salads]`, `[bubble tea]` name a thing to buy, not a business type. The guideline puts an **affirmative burden** on you: confirm the result offers it *in a meaningful way*.

- Establish it from a **menu or service listing**, not a description.
- If the queried thing is incidental to what the business does — a coffee bar selling drinks and pastries for `[breakfast]`, a steakhouse with one salad for `[salads]` — that is a **partial fit**. Demote on `User Intent`; do not rate it `Excellent`.
- If the menu cannot be reached, say so and rate the partial fit. The burden is on confirmation, so unconfirmed does not mean full credit.

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
| **Show All screenshot** | The tool's Show All button | Ask for it — it settles user-vs-viewport for every result at once |
| **Per-result pin screenshot** | Zoomed, satellite or hybrid layer | Ask for it — Pin Accuracy cannot be judged without seeing the map |

Measure distance from the **outer edge of the user viewport**, not from the device icon. The device icon only helps you find the viewport and has no rating significance. A pin's **tip** marks the location; the head is only an indicator.

## Working From Screenshots

You cannot see the rating tool. When Pin Accuracy is requested, the user supplies screenshots and those images **are** the tool's map layer — the surface the guideline requires the pin to be reconciled against. Judge them; do not ask the user to pre-judge them for you.

- Judge the **tip**. Apply the real tests: on the listed result's rooftop for `Perfect`; inside the property boundary, same side of the street, same block for `Approximate`; the first property to either side, same street name, same side, same block for `Next Door`; outside the result's property and its neighbours for `Wrong`.
- A usable frame is **satellite or hybrid**, zoomed enough to show the result's building and its immediate neighbours on both sides. The vector layer renders no rooftops, so pin accuracy cannot be judged from it at all.
- **A screenshot carries no scale.** Distance always comes from the coordinates via `../tools/maps_distance.py`, never from eyeballing an image.
- You see one frame and cannot zoom, pan, or switch layers. If the frame is ambiguous, wrongly zoomed, or vector-only, **ask for another** — do not guess, and do not fall back to `Can't Verify` when a better frame would settle it.
- Say in the evidence line that the pin was judged from a screenshot. Never phrase it so it reads as though you explored the map yourself.

**When the user corrects you.** A correction about *what is in the frame* — that is a car park not a rooftop, those are two separate buildings — wins immediately: they can zoom and switch layers, you only have the image you were sent. A disagreement about *the rating* is re-checked against the guideline first and changes only if the guideline supports it. The quality gate's "do not be agreeable" rule applies in full to the second case and not at all to the first.

Information in the pop-up box (phone, URL, coordinates) is for research only. Rate only the information in the result itself. **Never call a business.**

## Missing Evidence

- If research cannot settle whether a business is closed, assume it could exist and rate Name, Address, and Pin as `Can't Verify` — unless there is an obvious data issue such as a missing mandatory address component or a pin in the ocean, which stays rateable.
- Never claim you checked a page or map that you did not check.
- Search snippets alone are not proof.
- State the limitation in the output rather than inventing a rating.
- Some results appear normal or greyed out with **no rating fields**. No rating is required for them. This is expected and is not a technical issue or a reason to release.

## The Rating State Machine

Work these in order. Each step says what to do next, including when to stop.

**Run the Mandatory Recon Gate first.** Its output feeds steps 5, 9, 11 and 12 — do not start rating and research as you go.

**Query level — once per task**

1. **Confirm the platform and task.** TELUS Maps Search Evaluation, not Handshake, Outlier, or another TELUS family. If it is not Maps, stop and route via `../telus-evaluator/SKILL.md`.
   **A task header naming a different family is enough to stop** — "POI Evaluation
   Assessment", "Related Results", "Close Variants". Do not proceed on the assumption
   that the rubrics overlap, and do not rate while asking for the right guideline.
2. **Determine the task type.** Search Relevance rates relevance only. Search 2.0 also rates Name and Category Accuracy, Address Accuracy, and Pin Accuracy.
3. **Inventory the fields the UI actually requests.** For any result you may be asked for all ratings, some, one, or none. Rate only what is shown. Never invent a rating for a field the UI does not offer.
4. **Read the query inputs.** Query, locale, user location, viewport, viewport age — per the table above.
5. **Classify the query and determine location intent** — workflow **Phase 0**. Query type and the full viewport/user-location decision table are in `references/user-intent.md`. Explicit location in the query overrides viewport and user location. "Near me" uses user location and ignores the viewport even when fresh. If the query has **no maps intent**, every result is rated `Bad`.
6. **Answer the query-level navigational question once.** "Is there a navigational result for this query?" — `Yes` when exactly one real-world result could completely satisfy the intent; `No` when more than one could. Answer it **before** looking at results, and answer it even when the task shows no results at all.

**Result level — repeat for every result**

7. **Check unexpected language or script first.** Judge the result **name/title** only, not the address details beneath it. Expected = language/script of the test locale, the query, the result region, any combination of those, or an official brand/chain name used in that market. Missing or added diacritics are not an unexpected-language issue.
8. **If unexpected language applies → select the checkbox and STOP this result.** Every other field becomes unavailable. Do not rate relevance or any data dimension. Move to the next result.
9. **Research closure and actual existence** — workflow **Phases 1 and 4**. Always research the real-world state regardless of what the status field shows. Batch this: collect the pop-up URL from every result and run `../tools/check_urls.py` once, in parallel, before reading any of them. Where a pop-up carries no URL, guess the chain's official locator page — a 404 there is positive evidence of closure. Aggregator listings persist for years after a store closes and prove nothing on their own. Treat a temporary closure as open when the business announces it on its own webpage or managed social account — there is no time limit on this. Distinguish genuinely closed/non-existent from a result whose name or address is merely wrong; the latter is a data-accuracy problem, not a closure.
10. **Apply the closed/non-existent checkbox only when the evidence supports it.** It applies to business/POI results only, never to address-type results. Use it for closed/non-existent entities, randomly moving entities such as an unscheduled food truck, and non-recurring past events with no remaining maps intent. **If you check it, only relevance remains rateable** — do not produce Name, Address, or Pin ratings. When the status shows `PERMANENT_CLOSURE`, the relevance rating depends on whether the result is expected or unexpected; follow `references/result-level-issues.md`.
11. **Rate relevance, independently of data accuracy** — workflow **Phase 3**. **First look the shape up in `references/decided-cases.md` and apply the ruling verbatim.** Only when no decided case matches do you reason from the general rules. Always assume the result exists and its displayed data is correct, even when research proved otherwise. Closure alone is never grounds for `Bad`. Rate against the real world: build the full candidate set from the location intent and rank it, counting only open candidates. If a better result exists but is not shown, demote the shown results accordingly; if a result **is** the closest that exists, do not demote it for distance at all. Ignore result order and never demote for duplication. Any rating of `Good` or below requires a demotion checkbox and a comment.
12. **Rate each requested data dimension independently — Search 2.0 only, and only if step 10 did not gate them.** Name and Category Accuracy, Address Accuracy, Pin Accuracy. Each is judged on its own evidence; a pin can be correct while the address is wrong. Reverse-geocode every pin first (workflow **Phase 2**) to establish which parcel it sits on, then decide rooftop-vs-parcel on the supplied frame. If Pin Accuracy is `Perfect`, answer the follow-up "Does the available evidence indicate the result's precise location?" with `Yes` or `No`.
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

**`references/comment-examples.md` carries the required form, with a worked example per trigger. Re-read it immediately before writing, not from memory.** The shape is two plain sentences: open with `The query is …` naming the intent, then say what the result does and why it was demoted. Name a competing result by its name or street, never by a distance figure.

- State the user intent you concluded.
- **When you found something wrong, give the corrected value and a direct source link.** Shorten long URLs.
- Be short and specific; write in English regardless of test locale.
- Never include PII — no names, contact details, account numbers, or private data.

**Links attach to corrections, not to demotions.** A relevance demotion on distance or intent needs no link — nothing is factually wrong, so there is nothing to source. A wrong name, a wrong address component or a wrong category does: give the corrected value and where it came from. `Incorrect – Other Issue` requires links in every case.

**One deliberate divergence from the guideline.** The contract also says to *name the guideline section behind the demotion*. We do not — a section number in a pasted comment reads as machine output and slows the reviewer down without telling them anything the checkbox has not already said. Every other item on the contract's comment checklist is followed. This is the single line to reverse if a reviewer asks for citations.

Full trigger list in `references/rating-contract.md`.

## Release Survey

Summarised here because it is a hard gate; `references/rating-contract.md` is authoritative.

Release only when a technical or other issue genuinely prevents rating: `Adult Content`, `Technical Issue`, `Not Enough Time Allocated`, `Other`.

Do **not** release because the rating is hard, because the query looks unrelated to maps (rate all results `Bad`), because the query or results are outside your market, because the query returned no results (still answer the navigational question and submit), or because the query is in a foreign language (research or translate it).

## Pre-Submission Audit

State each of these in the output before presenting ratings. **If the recon RUN ID and Phase 3 ranking table are not in the output, stop — the task is not ready to submit.**

1. Recon gate run; RUN ID and candidate ranking quoted.
2. Every URL cited in an evidence line was fetched in that run and read.
3. Task type identified and requested dimensions inventoried.
4. Query classified and location intent determined.
5. Navigational question answered exactly once.
6. Every result evaluated independently.
7. Unexpected-language and closure gates checked before any rating.
8. Relevance separated from data accuracy.
9. Decided-case lookup done; the matching case named in the evidence line, or "no decided case matches" stated.
10. Category fit for a product/service query confirmed from a menu, not a description.
11. Exact rating labels used.
12. Every `Good`-or-lower relevance rating carries a demotion checkbox and a comment.
13. Every non-`Correct`/non-`Perfect` data rating carries a comment.
14. Pin ratings drawn from the full five-level scale.
15. Missing or unusable evidence disclosed.
16. No rating invented for a hidden or unavailable field.
17. TELUS quality gate passed.

## Output Template

This section defines the **structure**. `references/output-style.md` defines how the prose inside it is written — evidence lines that carry one clause per dimension with the numbers included, the candidate ranking table behind any distance call, and the closing commentary that defends a counterintuitive rating, names the trap, or hands a frame question back to the rater. Read it alongside this template.

The template is **conditional**. Render only what the task actually offered:

- Search Relevance task → omit the Name/Category, Address, and Pin lines entirely.
- A dimension the UI did not request → omit that line.
- `Unexpected language or script` checked → render the issue line and nothing else for that result.
- `Closed or does not exist` checked → render relevance, then `Data dimensions: gated by closure checkbox` in place of the three data lines.
- Pin not rated `Perfect` → omit the precise-location follow-up.
- Result shown with no rating fields → one line saying so; no ratings.

Never render a line with a guess, a dash, or "N/A" where a gate or the UI removed the field. State the gate instead — an omission a reviewer can see is the point.

Two formatting rules make the output usable rather than merely correct:

- **Put every task-facing comment in backticks.** It gets pasted into the rating tool verbatim, so it must be selectable as one block with no surrounding prose.
- **Drop a line entirely when it does not apply.** No `Checkbox: none`, no `Comment: n/a`, no dashes. A result rated `Excellent` has no checkbox line and no comment line at all.

**Header, once per task:**

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
```

**Then one block per result.** The heading carries the name **and** the address, so a result is identifiable without scrolling back to the task. Field order is fixed: Relevance, Name Accuracy, Address Accuracy, Pin Accuracy, Checkbox, Comment, Evidence. The precise-location follow-up slots in directly after Pin Accuracy on the rare tasks that ask for it.

**Search 2.0, everything clean.** No checkbox line and no comment line, because nothing is demoted and every data rating is `Correct` or `Perfect`:

```
**Result 1: M·A·C — 1544 Travis Blvd, Fairfield**
- Relevance: **Excellent**
- Name Accuracy: **Correct**
- Address Accuracy: **Correct**
- Pin Accuracy: **Perfect**
- Evidence: MAC counter/listing at 1544 Travis Blvd is supported by accessible listings; pin is on the supplied hybrid rooftop view, but exact position inside the shared retail building is not pinned down.
```

**The precise-location follow-up is conditional — usually absent.** §9.1.1.1 says that after a `Perfect` pin you *may* be required to answer *"Does the available evidence indicate the result's precise location?"*. It does not render on every task. Include the line **only when the task actually presents that question**, and omit it otherwise, exactly as with any other field the UI did not offer. When it is present it is its own bullet, never appended to the Pin line:

```
- Pin Accuracy: **Perfect**
- Precise location evidence?: **No**
```

Answer `No` when the rooftop is right but the position under it is not established — a unit inside a shared retail building, for instance. Answer `Yes` when the evidence pins the exact spot. Not knowing *which building* is a different problem: that is `Can't Verify` on the pin itself, not a `No` here.

**Search 2.0 with a demotion and a data fault:**

```
**Result 2: 7-Eleven — 834 E Fremont Ave, Sunnyvale**
- Relevance: **Navigational**
- Name Accuracy: **Correct**
- Address Accuracy: **Incorrect** — Street Number
- Pin Accuracy: **Perfect**
- Comment: `User intent is the 7-Eleven on Fremont Ave in Sunnyvale. The result shows 834 E Fremont Ave but the official store locator lists 836; 834 is a separate parcel occupied by a dry cleaner. Correct address: 836 E Fremont Ave, Sunnyvale, CA 94087.`
- Evidence: official store locator; street imagery of the storefront at 836; aerial imagery places the pin on the 7-Eleven rooftop.
```

**Search Relevance task — the three data lines and the follow-up are absent entirely:**

```
**Result 3: M·A·C — 1200 Broadway Plz, Walnut Creek**
- Relevance: **Good**
- Checkbox: **Distance/Prominence issue**
- Comment: `The query is for a MAC Cosmetics location near the user; this result satisfies the chain intent but is farther than the closer Fairfield result.`
- Evidence: distance user to pin computed at 21.4 km via maps_distance.py; two closer M·A·C locations exist.
```

**When a gate fires, say so instead of rating:**

```
**Result 4: Buffalo Exchange — 1318 14th St NW, Washington DC**
- Result-level issue: **Business/POI is closed or does not exist** — checked
- Relevance: **Acceptable**
- Checkbox: **User Intent issue**
- Data dimensions: gated by the closure checkbox, not rated.
- Comment: `User intent is a vintage clothing store near the user in Washington DC. This result is permanently closed and open alternatives sit within 1 km, so it is an unexpected closure and demotes two steps from Excellent.`
- Evidence: chain locator omits the branch; local press reports permanent closure; recent street imagery shows the unit vacant.

**Result 5: ဈေးကွက် — 1875 S Bascom Ave, Campbell**
- Result-level issue: **Result name/title is in unexpected language or script** — checked. Rating complete; no further fields are available.
```

**Close with:**

```
**Pre-Submission Audit**: [confirm the 13 points]
```

## References

Load these deliberately rather than all at once.

**Always read, every task:**

| Reference | Covers |
|---|---|
| `scripts/maps_recon.py` | The recon gate itself. Run it before rating; quote its RUN ID and ranking table. Task file format in `scripts/task.example.json` |
| `scripts/test_maps_recon.py` | Regression tests for the gate — no network, runs in under a second. **Run after any edit to `maps_recon.py`.** Every case in it is a bug that shipped once |
| `references/decided-cases.md` | Cases the guideline has already ruled on, verbatim. Look the shape up **before** forming a view on relevance — these outrank your reasoning |
| `references/research-workflow.md` | Manual fallback and interpretation — phase detail, the fallback ladder when a source blocks you, how to read a reverse-geocode |
| `references/rating-contract.md` | Every exact label, checkbox, and field-hiding rule. The authority — no label exists unless it appears here |
| `references/user-intent.md` | Query types, explicit vs implicit location, the viewport/user-location decision table, "near me" |

**Read when the situation calls for it:**

| Reference | Read it when |
|---|---|
| `references/query-family-playbook.md` | Always — go straight to the branch matching this query family (Chapters 10–11) |
| `references/comment-examples.md` | Any comment is required — a relevance rating of `Good` or below, or any data rating that is not `Correct` / `Perfect` |
| `references/output-style.md` | Writing the chat response — evidence lines, candidate tables, and the commentary that defends a call, names the trap, or hands a frame question back |
| `references/result-level-issues.md` | Unexpected language applies, or anything about closure or `PERMANENT_CLOSURE` |
| `references/research-evidence.md` | Deciding what proves a rating, or evidence has run out |
| `references/relevance.md` | Working out a relevance demotion — connection types, prominence, distance, viewport, rural areas, transit, parking, service-level mismatch |
| `references/name-category-accuracy.md` | Name/Category is requested — name sources, misspelling severity, location modifiers, category rules |
| `references/address-accuracy.md` | Address is requested — components, result-type expectations, features without addresses |
| `references/us-address-verification.md` | **Any US address rating.** The USPS gate, city/postal/cardinal/street-type rules, DPV and ZIP+4, the two validation flowcharts, and the Utah/Queens/Milwaukee/County addressing systems |
| `references/unsupported-locales.md` | The task country has no guideline of its own — address format discovery, diacritics, cadastral maps for pins, prominence in an unfamiliar market |
| `references/pin-accuracy.md` | Pin is requested — rooftops, property boundaries, campus, entrance polygons, transit, parking, shared spaces |
| `references/calibration-examples.md` | Only when a call is genuinely borderline and you want a worked case to check against |

**Tool:** `../tools/maps_distance.py` computes straight-line distance between coordinates. It informs a rating; it never decides one.

Full extracted source for lookups: `TELUS-TASKS/maps-extracted/text.md` (14,038 lines, 367 images). It is a search aid — a rendered PDF page always outranks it.
