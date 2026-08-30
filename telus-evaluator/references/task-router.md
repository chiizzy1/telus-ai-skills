# TELUS Task Router

Use this before routing any TELUS task.

## Contents

- [Non-Negotiables](#non-negotiables)
- [Strict Routing Protocol](#strict-routing-protocol)
- [Task Families](#task-families)
- [TELUS Families Without A Dedicated Skill](#telus-families-without-a-dedicated-skill)
- [Task Templates](#task-templates)
- [Source Hierarchy](#source-hierarchy)
- [Comment Style](#comment-style)

## Non-Negotiables

- TELUS is its own platform. Do not import Handshake, Outlier, or Data Annotation Tech rules.
- The matching TELUS guideline/PDF is the source of truth.
- The current task UI can add task-specific instructions; follow it unless it conflicts with the guideline.
- Do not be agreeable. If the user guess conflicts with the guideline or evidence, say so.
- Do not rate when required evidence has not been checked.

## Strict Routing Protocol

1. Read the task title and visible instructions.
2. Identify the output controls and rating labels.
3. Match the task to one TELUS family below.
4. Load the matching task-specific skill and reference.
5. Apply that task's hard gates before scoring.
6. Keep the final answer short and practical.

## Task Families

### Search SBS / Search Satisfaction

Use `search-sbs-evaluator` (read `../../search-sbs-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/search-sbs.md`.

Signals:

- Side-by-side search results.
- Overall Preference Rating or OPR.
- Result satisfaction labels `HS`, `S`, `SS`, `NS`.
- Search result flags such as Content Unavailable, Inappropriate, or Wrong Language.

Do not route Web Images or Search Ads here unless the task UI is clearly Search SBS.

### Bot Reply Validation / AI Assistant Human Evaluation

Use `telus-bot-reply-validator` (read `../../telus-bot-reply-validator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/ai-assistant-human-evaluation.md`.

Signals:

- Apple assistant response validation.
- Metrics: Accuracy, Relevancy, Compliance, Fluency, Safety, Overall Quality.
- Cited Apple resources or region-specific Apple claims.

Do not use Search SBS satisfaction labels here.

### Text Response Evaluation

Use `text-response-evaluator` (read `../../text-response-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/text-response-evaluation.md`.

Signals:

- Text-message transcript.
- Transcript summary.
- Pass/Reject transcript decision.
- Rejection reasons such as emojis, spelling mistake, repetition, participant name, incoherent text, impossible text conversation, or rhyming.
- Best reply to the final text.
- Multiple-choice question about the transcript.

Judge response options only after transcript pass/reject rules are applied.

### Web Images Satisfaction

Use `web-images-satisfaction-evaluator` (read `../../web-images-satisfaction-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/web-images-satisfaction.md`.

Signals:

- Image result rating.
- Image satisfaction and host-page satisfaction.
- Image flags such as Did not load, Unsafe, Near duplicate.
- Host-page flags and image side-by-side preference.

Do not use Search SBS `HS/S/SS/NS` here.

### Search Ads Relevance

Use `search-ads-relevance` (read `../../search-ads-relevance/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/search-ads-relevance.md`.

Signals:

- iOS App Store ad shown against a user search query.
- Ad-to-query relevance grading.
- Rating labels `Excellent`, `Good`, `Acceptable`, `Bad`.
- App Store listing links for the advertised app.

Guideline source: `TELUS-TASKS/SEARCH-ADS-RELEVANCE/guidelines.txt` and `TELUS-TASKS/SEARCH-ADS-RELEVANCE/telus- SEARCH-ADS-RELEVANCE.pdf`.

Do not use Search SBS `HS/S/SS/NS` here.

### Close Variants

Use `close-variants-evaluator` (read `../../close-variants-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/close-variants.md`.

Signals:

- An original query paired with a query variant.
- Spelling, abbreviation, reordering, transliteration, synonym, or language-transformation comparison.
- Rating labels `Good`, `Acceptable`, `Bad`.

Guideline source: `TELUS-TASKS/Close Variants/Telus - Close Variants.pdf`.

Do not confuse this with Search Ads Relevance. Close Variants compares a query to a variant query, not a query to an ad.

### Maps Ads Offensiveness

Use `maps-ads-offensiveness-evaluator` (read `../../maps-ads-offensiveness-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/maps-ads-offensiveness.md`.

Signals:

- A Maps search query on the left and a promoted Brand or POI ad on the right.
- Rating labels `Majority may find the pair Offensive`, `Some may find the pair Offensive`, `Not Offensive`.
- A comment required on every rating, including Not Offensive.
- Task titled Ads Quality, or instructions saying the pair is judged on offensiveness rather than relevance.

Guideline source: `TELUS-TASKS/apple map adds offensiveness/apple map adds offensiveness.pdf`.

This is the only TELUS task that does not rate relevance. Its guideline says so twice in bold. An irrelevant pair is Not Offensive.

Do not route this to `related-results-evaluation-evaluator`. Both show one Maps query and one POI with a single rating and a mandatory comment, so the layouts are nearly identical; the rating labels are what separate them. The rubrics genuinely disagree: `McDonald's` with a Burger King ad is Good relevance and Not Offensive, and `veterinary hospital` with a paint store ad is Bad relevance and Not Offensive. Routing one to the other produces confident wrong answers on every pair.

Do not route this to `search-ads-relevance` either. That task rates App Store ads against App Store queries, on relevance.

### Related Results Evaluation

Use `related-results-evaluation-evaluator` (read `../../related-results-evaluation-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/related-results-evaluation.md`.

Signals:

- One query paired with one maps POI result, rated on Relevance alone.
- A result card showing a name, a category line, a Maps Result link with a red pin icon, and a Website link.
- Rating labels `Excellent`, `Good`, `Acceptable`, `Bad`, with a mandatory comment on every rating.
- Four web-search links for the query: Bing, DuckDuckGo, Google, Yahoo.
- No map, no numbered pins, no viewport, no user location.

Guideline source: `TELUS-TASKS/Related Results evaluation/Related Results evaluation.pdf` (extracted: `TELUS-TASKS/Related Results evaluation/extracted/Related-Results-Guidelines.md`).

Do not route this to `maps-search-evaluator`. Both are maps tasks and three of the four labels overlap, but Related Results has no `Navigational` tier, no viewport or user location, no demotion checkboxes, and no Name/Category, Address or Pin Accuracy. If the task shows numbered pins on a map, it is Maps Search Evaluation; if it shows one result card and one Relevance control, it is Related Results.

Do not route this to `search-ads-relevance` either. The four labels are the same words, but that task rates an App Store ad against an App Store query.

Do not confuse this with Maps Ads Offensiveness, which shows the same one-query-one-POI layout but rates offensiveness on a Majority / Some / Not Offensive scale and never rates relevance.

### Maps Search Evaluation

Use `maps-search-evaluator` (read `../../maps-search-evaluator/SKILL.md`).

Task template: `TELUS-TASKS/task-templates/maps-search-evaluation.md`.

Signals:

- Map search results with numbered pins on a map.
- Query with viewport (fresh/stale), user location, and locale.
- Relevance rating scale: `Navigational`, `Excellent`, `Good`, `Acceptable`, `Bad`.
- Demotion checkboxes: User Intent, Distance/Prominence.
- Data accuracy ratings: Name/Category Accuracy, Address Accuracy, Pin Accuracy.
- Task type label "Search 2.0" or "Search Relevance."
- Result status `PERMANENT_CLOSURE`.
- Navigational result question (Yes/No) asked per query.
- Checkboxes for "Result name/title in unexpected language" or "Business/POI is closed or does not exist."

Guideline source: `TELUS-TASKS/Maps Search Evaluation/telus - Maps Search Evaluation Guidelines.pdf` (searchable extraction: `TELUS-TASKS/maps-extracted/text.md`).

Do not use Search SBS `HS/S/SS/NS` labels here. Maps Search Evaluation has its own relevance scale.

Do not confuse this with Related Results Evaluation, which rates a single query-result pair on Relevance alone with no pins, viewport or accuracy fields.

## TELUS Families Without A Dedicated Skill

The workspace contains guidelines for these TELUS task types, but no separate installed skill has been built yet:

- Broad Match: `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf`
- Image Themes Rating: `TELUS-TASKS/Image-Themes-Rating/telus-Image_Themes_Rating.pdf`

If one appears, read its official guideline directly and tell the user no dedicated TELUS skill exists yet. Do not force it through a different TELUS skill.

## Task Templates

Blank templates for every TELUS task type live in `TELUS-TASKS/task-templates/`, one file per type, named after the task. The user fills one into `TELUS-TASKS/task.md`, which is the live working file and is read-only input. Each family above names its template.

## Source Hierarchy

1. Matching TELUS task UI and official guideline/PDF.
2. Task media, query, transcript, URL, result, response, locale, date, and answer options.
3. Matching TELUS task-specific skill reference.
4. User memory or prior chat.

If sources conflict, use the higher source.

## Comment Style

Use plain wording:

- Good: `The response answers the question, but the camera claim is wrong based on Apple's specs page.`
- Good: `This is Search SBS, so use HS/S/SS/NS and OPR. It is not a Web Images task.`
- Bad: `The answer demonstrates strong multimodal rubric alignment.`

For final platform comments, follow the task-specific skill's comment format.
