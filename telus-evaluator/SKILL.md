---
name: telus-evaluator
description: Router and source-of-truth controller for TELUS task work. Use when asked to rate, audit, verify, or structure TELUS tasks; when task type is unclear; when working from TELUS-TASKS/task.md, TELUS-TASKS PDFs, or TELUS guideline folders; or when deciding which TELUS task-specific evaluator skill/rubric should apply.
---

# TELUS Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Core Rule

Use TELUS rules only for TELUS tasks. Keep TELUS separate from Handshake, Outlier, and Data Annotation Tech.

Before routing a task, read `references/task-router.md`.

> **Output goes in the chat response only.** Task files and every other file in the workspace are READ-ONLY input. Never edit, overwrite, or write results into them, and never create scratch or working files. Every task skill defines an output template; present the complete result in chat using it.

## Quality Gate (applies to every TELUS task)

`references/quality-gate.md` is mandatory for all TELUS work, whichever task skill you route to. Read it before submitting any rating. In short:

1. The guideline is the single source of truth, above instinct, prior answers, and what the user seems to want.
2. Never claim a check you did not run. Say plainly what was skipped or blocked.
3. Judge meaning, not word overlap. Text search locates content; it never justifies a rating by itself.
4. Rate every item individually, with its own reason and its own evidence.
5. Calibrate honestly, neither generous nor harsh, and name the rule behind each rating.
6. Apply locale, time sensitivity, position, and variety wherever the task type allows, and say so when one does not apply.
7. Re-read the skill's output examples before writing a comment, and match the pattern they teach.
8. When challenged, re-verify against the guideline and answer with evidence. Change a rating only if the guideline supports it, never to be agreeable.

## One Task Type Per Chat

Handle each TELUS task type in its own chat. Rubrics from different task types compete with each other — `HS/S/SS/NS` leaking into a Maps task, or Search SBS flags into a Bot Reply task, is the most common way a rating goes wrong. A fresh chat per task type keeps the loaded rules clean.

Starting a fresh chat, this is enough:

```text
Follow the official guideline as the single source of truth. Do not be agreeable. Confirm the task
type first, read the full task, and only rate what can be verified from the task content or
accessible pages. Keep comments brief and natural.
```

Then paste the task. This skill routes it to the right evaluator, and that skill carries the rubric.

## Source Hierarchy

1. The current TELUS task UI and matching official TELUS guideline/PDF.
2. The visible task content: query, locale, date, transcript, image, page, response, result set, media, or answer options.
3. The matching TELUS task-specific skill and its reference file.
4. User memory, previous chat, or general judgment.

If the user or a prior answer conflicts with the TELUS guideline, follow the guideline.

## Routing Workflow

1. Confirm the task is TELUS, not Handshake or Outlier.
2. Identify the TELUS task type from the title, UI controls, rating labels, guideline folder, or task.md content.
3. Route to the matching task-specific TELUS skill.
4. Read that skill's `SKILL.md` and required reference file before rating.
5. Apply the task-specific hard gates before choosing scores.
6. Verify facts, pages, URLs, images, or cited sources when the task type requires it.
7. Present the result in chat using the routed skill's output template, filling every section it defines.

## Task Type Map

- Search SBS, Search Satisfaction, side-by-side web search, OPR, or `HS/S/SS/NS`: use `search-sbs-evaluator` (read `../search-sbs-evaluator/SKILL.md`).
- TELUS AI Assistant, Bot Reply Validation, Apple assistant Human Evaluation, or Accuracy/Relevancy/Compliance/Fluency/Safety/Overall Quality: use `telus-bot-reply-validator` (read `../telus-bot-reply-validator/SKILL.md`).
- Text Response Evaluation, text-message transcript pass/reject, transcript summary, best reply, or transcript MCQ: use `text-response-evaluator` (read `../text-response-evaluator/SKILL.md`).
- Web Images Single Side Image Satisfaction, image side-by-side, image flags, host page flags, near duplicates, or image OPR: use `web-images-satisfaction-evaluator` (read `../web-images-satisfaction-evaluator/SKILL.md`).
- Search Ads Relevance, iOS App Store ad relevance, ad-to-query grading, or Excellent/Good/Acceptable/Bad ad ratings: use `search-ads-relevance` (read `../search-ads-relevance/SKILL.md`).
- Close Variants, query-variant similarity, spelling/abbreviation/transliteration/synonym evaluation, or Good/Acceptable/Bad variant ratings: use `close-variants-evaluator` (read `../close-variants-evaluator/SKILL.md`).
- Maps Search Evaluation, Search 2.0, Search Relevance, map search results with pins, Navigational/Excellent/Good/Acceptable/Bad relevance, Name/Category Accuracy, Address Accuracy, Pin Accuracy, viewport age (fresh/stale), PERMANENT_CLOSURE, or result-level distance/prominence demotion: use `maps-search-evaluator` (read `../maps-search-evaluator/SKILL.md`).

## Known TELUS Task Types Without A Dedicated Skill Yet

These are TELUS task families in the workspace, but they do not yet have installed task-specific skills:

- Broad Match: read `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf`.
- Image Themes Rating: read `TELUS-TASKS/Image-Themes-Rating/telus-Image_Themes_Rating.pdf`.

Do not force these into Search SBS, Bot Reply, Text Response, Web Images, Search Ads, or Close Variants. If the user repeatedly needs one of these, create a separate TELUS task skill for it.

## Platform Separation Rules

- Do not use Handshake or Outlier rubrics for TELUS.
- Do not use TELUS rubrics for Handshake or Outlier.
- Do not mix TELUS task scales. `HS/S/SS/NS` belongs to Search SBS only.
- Do not use Search SBS flags for Bot Reply or Text Response tasks.
- Do not use Bot Reply metrics for TI2T, Handshake, or other text tasks.
- Do not be agreeable. Verify against the visible task and the official TELUS guideline.
- Do not rate from snippets, first impressions, or memory when the task requires page/source verification.

## Unsupported Or Unclear Tasks

If the TELUS task type is unclear:

1. Read the visible task title, instructions, labels, and rating controls.
2. Read `TELUS-TASKS/task.md` if the task is stored there.
3. Search only inside `TELUS-TASKS/` for the matching guideline.
4. State plainly if no task-specific skill exists yet.
5. Apply the matching official TELUS guideline directly rather than borrowing another task's rubric.

## Final Checklist

- TELUS platform confirmed.
- Task type identified.
- Correct TELUS skill or official guideline selected.
- Wrong-platform and wrong-task rubrics avoided.
- Current task UI and official guideline used over memory.
- Verification done when required.
- Output presented in chat using the routed skill's template, with every required section filled.
