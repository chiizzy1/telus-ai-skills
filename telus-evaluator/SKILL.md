---
name: telus-evaluator
description: Router and source-of-truth controller for TELUS task work. Use when Codex is asked to rate, audit, verify, or structure TELUS tasks; when task type is unclear; when working from TELUS-TASKS/task.md, TELUS-TASKS PDFs, or TELUS guideline folders; or when deciding which TELUS task-specific evaluator skill/rubric should apply.
---

# TELUS Evaluator

## Core Rule

Use TELUS rules only for TELUS tasks. Keep TELUS separate from Handshake, Outlier, and Data Annotation Tech.

Before routing a task, read `references/task-router.md`.

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
7. Keep the answer short, plain, and evidence-based.

## Task Type Map

- Search SBS, Search Satisfaction, side-by-side web search, OPR, or `HS/S/SS/NS`: use `search-sbs-evaluator`.
- TELUS AI Assistant, Bot Reply Validation, Apple assistant Human Evaluation, or Accuracy/Relevancy/Compliance/Fluency/Safety/Overall Quality: use `telus-bot-reply-validator`.
- Text Response Evaluation, text-message transcript pass/reject, transcript summary, best reply, or transcript MCQ: use `text-response-evaluator`.
- Web Images Single Side Image Satisfaction, image side-by-side, image flags, host page flags, near duplicates, or image OPR: use `web-images-satisfaction-evaluator`.
- Search Ads Relevance, iOS App Store ad relevance, ad-to-query grading, or Excellent/Good/Acceptable/Bad ad ratings: use `search-ads-relevance`.
- Close Variants, query-variant similarity, spelling/abbreviation/transliteration/synonym evaluation, or Good/Acceptable/Bad variant ratings: use `close-variants-evaluator`.

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
- Output kept concise and natural.
