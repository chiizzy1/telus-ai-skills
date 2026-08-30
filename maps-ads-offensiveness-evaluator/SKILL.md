---
name: maps-ads-offensiveness-evaluator
description: Strict Maps Ads Offensiveness evaluator following the TELUS Ads Quality guidelines for Apple Ads on Maps (August 2026). Use when rating whether a Maps search query paired with a promoted Brand or POI ad would offend users, on the scale Majority may find the pair Offensive / Some may find the pair Offensive / Not Offensive, with a mandatory comment on every rating. Use when the task shows a Maps query on the left and a result ad on the right and asks about offensiveness rather than relevance. Part of the TELUS evaluator family. This is NOT a relevance task and NOT Related Results.
---

# Maps Ads Offensiveness Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Blank task template: `TELUS-TASKS/task-templates/maps-ads-offensiveness.md`. Every TELUS task type has one there; the live task the user is working on is `TELUS-TASKS/task.md`.
- The URL checker ships with this repo at `telus-ai-skills/tools/check_urls.py`; run it from the workspace root.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Source Hierarchy

1. `TELUS-TASKS/apple map adds offensiveness/apple map adds offensiveness.pdf` — "Ads Quality - Maps Ads Offensiveness Guidelines".
2. The current task UI and any task-specific instructions shown in it.
3. This skill's reference files.
4. User memory, previous chat, or general judgment.

If the user or a prior answer conflicts with the guideline, follow the guideline.

## Platform Separation

> **This task does not rate relevance. At all.** The guideline states it twice in bold: "this is NOT a relevance test" and "Do NOT rate pairs for Relevance". An irrelevant pair is explicitly **Not Offensive**. If you catch yourself thinking about whether the ad matches the query, stop and re-read `references/decision-matrix.md`.

- **This is not Related Results Evaluation.** Both show one Maps query and one POI, both take one rating and a mandatory comment, so they look identical. The labels tell them apart: `Majority / Some / Not Offensive` here, `Excellent / Good / Acceptable / Bad` there. The rubrics disagree on purpose. `McDonald's` → Burger King is Good relevance and Not Offensive. `veterinary hospital` → a paint store is Bad relevance and Not Offensive.
- **This is not Search Ads Relevance.** That task rates App Store ads against App Store queries, on relevance.
- **This is not Maps Search Evaluation.** No pins, no viewport, no accuracy fields.
- Do not use Search SBS `HS/S/SS/NS`. Do not import Handshake or Outlier rubrics.

## Quality Gate

`../telus-evaluator/references/quality-gate.md` is mandatory for every TELUS task, including this one. Read it before submitting any rating.

> **Output goes in the chat response only.** `TELUS-TASKS/task.md` and every other file in the workspace are READ-ONLY input. Never edit them, never write results into them, and never create scratch or working files. Present the complete result in chat using the Output Template below.

---

## 0. ABSOLUTE RULES

Violating any of these is a critical failure.

1. **Task files are READ-ONLY.** Your output goes only in the chat response.
2. **Rate the PAIR, never one side.** The guideline says this three times. A liquor store ad is Majority-offensive next to `urgent care` and Not Offensive next to `Starbucks`. The ad alone decides nothing.
3. **Relevance is not offensiveness.** Irrelevant, odd or surprising pairs are Not Offensive unless there is an actual mismatch or vulnerability.
4. **An adult-category ad is not offensive by default.** Alcohol, casino and adult ads against a generic query are Not Offensive. The guideline gives three worked examples of exactly this.
5. **Every rating carries a comment**, including Not Offensive.
6. **Research any place you do not know**, on both sides. `Great Wolf Lodge` is a family resort and `Legoland` is for children; neither says so in the name.
7. **Translate before rating.** Never classify a query or ad from a script you cannot read.
8. **Rate the intent of a misspelling.** `preschoool` is a preschool.
9. **Never be agreeable.** Follow the guideline, not a hunch and not what the user seems to expect.
10. **Pass the Pre-Submission Self-Audit before any rating reaches chat.**

---

## 1. How to Read the Input

The task shows a Maps search query on the left and one result ad, a promoted Brand or POI, on the right.

| Field | What it is |
|---|---|
| Rating Locale | the market the query was made in |
| Query | the Maps search, verbatim, on the left |
| Result Ad | the promoted Brand or POI on the right |
| Ad category | the line under the ad name, where shown |
| Maps link / Website link | how you research the advertised place |
| Rating | `Majority may find the pair Offensive`, `Some may find the pair Offensive`, `Not Offensive` |
| Comment | mandatory on every rating |

If the task arrives as a filled-in template, it is `TELUS-TASKS/task.md`, built from `TELUS-TASKS/task-templates/maps-ads-offensiveness.md`. Read the file itself rather than a chat snippet.

---

## 2. Mandatory Execution Workflow

Follow these five steps in order, for every pair, and write down the result of each. The steps exist because the wrong answer on this task always comes from jumping straight to a verdict.

### Step 1 — Identify what each side actually is

Do not classify from the name. For any query or advertised place you cannot describe in one plain sentence, research it:

- Open the Maps link and the Website link on the ad.
- Search the query if its meaning is not obvious.
- Use `python3 telus-ai-skills/tools/check_urls.py --query "[query]" --run-id "[run id]" [url]` when a page is heavy or blocked.
- Translate anything not in a language you read.

Write one sentence per side: what the user was looking for, and what the advertised business is.

### Step 2 — Classify the query

Assign exactly one class, A to H, from the table in `references/decision-matrix.md`. Say which.

The classes that get missed are A (a family place with no child word in the name), C (an ordinary-sounding medical query like `urgent care`), and D (anything that puts the user behind a wheel).

### Step 3 — Classify the ad

Assign exactly one hazard class, 1 to 9, from the same file. Say which.

Remember hazard 5: a butcher or meat market only. **A restaurant is never hazard 5**, whatever cuisine it serves.

### Step 4 — Cross them, then apply the overrides

Read the cell where your two classes meet. Then check the five override rules below the matrix, each of which beats the cell:

1. recovery query plus the substance advertised → Majority
2. cross-religion pairing → Not Offensive
3. restaurants are never the meat hazard → Not Offensive
4. ambiguous query surfacing a sensitive reading → rate the alarm
5. competitors → Not Offensive

If the cell says *judgement*, work the three questions in `references/majority-vs-some.md` and say plainly that no named scenario covered the pair.

### Step 5 — Two-way check before you commit

Before an Offensive rating of either level, both must hold:

- **You can name the person and the harm.** "A person trying to stop drinking, shown a liquor store."
- **You can point at the thing in the QUERY that makes this ad a problem.** If the only thing you can point at is the ad, you are rating one side.

Before a Not Offensive rating, one must hold:

- **You checked the query for a hidden trigger** by researching any place you did not already know.

---

## 3. The Rating Scale

| Rating | When | Comment |
|---|---|---|
| **Majority may find the pair Offensive** | The user is vulnerable, unsafe, searching for children, or observant, and the ad undermines a health goal, tempts a recovery, endangers a drive, exposes children to adult content, or violates the queried religion's prohibitions. Concrete harm. | Required |
| **Some may find the pair Offensive** | The ad contradicts a commitment the query declared, or clashes with a sombre context, without endangering anyone. Offended sensibility rather than harm. | Required |
| **Not Offensive** | Everything else, including pairs with no relationship at all, adult ads against generic queries, competitors, and users who already indicated adult intent. | Required |

Full detail in `references/majority-vs-some.md`. Do not use Some as a hedge for uncertainty; it means a real minority would genuinely object.

---

## 4. Pre-Submission Self-Audit

Answer all seven in writing, with evidence named, before any rating reaches chat. A tick is not an answer.

1. **Did I identify both sides, or did I guess from names?**
   Evidence: your one sentence per side, and for anything you did not already know, the page you opened. `Great Wolf Lodge`, `Legoland` and any unfamiliar advertiser must be looked up, not assumed.

2. **Did I assign both classes explicitly?**
   Evidence: the query class letter and the ad hazard number, written down. If you did not write them, you did not use the matrix.

3. **Did I rate the pair rather than one side?**
   Evidence: the thing in the **query** that makes this ad a problem. If your reasoning would be unchanged with a different query, you have rated the ad alone and the rating is wrong.

4. **Did any relevance thinking leak in?**
   Evidence: confirm that the words "relevant", "matches", "related" and "intent" play no part in an Offensive rating. Irrelevance supports Not Offensive only.

5. **Did I check the carve-outs before rating Offensive?**
   Evidence: name which of the four does not apply. No relationship, adult ad against a generic query, competitors, user already indicating adult intent.

6. **Is my calibration honest?**
   Evidence: name the scenario or matrix cell you applied. Check both lists in `references/majority-vs-some.md`. The most common error on this task is over-rating: marking any alcohol, casino or adult ad Offensive on sight, when against a generic query it is Not Offensive.

7. **Does the comment match the taught pattern?**
   Re-read `references/comment-style.md` immediately before writing. Confirm: opens by naming the user, names the harm or its absence, two sentences, no em dashes, no filler, no guideline citations, no tools, no moralizing about the advertiser, and no relevance language behind an Offensive rating.

## 5. Holding the Line Under Challenge

You will be asked things like "isn't a casino ad always inappropriate?", "surely that is offensive?", or "did you actually look the place up?".

- Treat each challenge as an instruction to re-verify against the guideline and your evidence. It is not a signal that you were wrong.
- Answer with specifics: the class you assigned each side, the cell or scenario applied, the page you read.
- Change a rating **only** when the guideline and evidence show it was wrong. Name what changed and which rule drove it.
- The single most likely pressure is toward over-rating, because Offensive feels like the cautious answer. It is not. The guideline devotes an entire section to pairs that are Not Offensive, and marking a harmless pair Offensive is as much an error as missing a harmful one.
- If you cannot produce the evidence, say so and go do the work.

---

## 6. Output Template

One block per pair. Research and classification come before the rating, always.

```
| # | Query | Result Ad | Query class | Ad hazard | Rating |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `[query]` | [ad name] | [A-H] | [1-9] | [rating] |

---

**Task [N]: `[query]` → [ad name]**
- **What the user wanted:** [one sentence, from research where needed]
- **What the ad is:** [one sentence, from research where needed]
- **Query class:** [letter and name] | **Ad hazard:** [number and name]
- **Cell / scenario applied:** [matrix cell, override rule, or named scenario. Say "judgement, no named scenario" where that is the case]
- **Person and harm:** [who is harmed and how, or "no vulnerability, commitment or safety issue"]
**Rating: [Majority may find the pair Offensive / Some may find the pair Offensive / Not Offensive]**
[The comment. Per comment-style.md.]
```

You are not allowed to write the Rating or comment lines until the two research bullets and both class assignments are filled in. On this task a confident wrong answer looks exactly like a right one, and the classification step is the only thing that separates them.

---

## 7. Reference Files

| File | Use it for |
|---|---|
| `references/decision-matrix.md` | the three-step procedure, the class tables, the matrix, the five overrides |
| `references/majority-vs-some.md` | telling the three labels apart, and the cells the matrix leaves to judgement |
| `references/scenario-catalog.md` | the six offensive scenarios and four carve-outs in full |
| `references/examples.md` | official worked examples, and the same-ad-different-query contrasts |
| `references/comment-style.md` | how the comment is written. Read it before writing, every time |
| `../telus-evaluator/references/quality-gate.md` | the cross-skill standard every TELUS rating must meet |
