# TELUS Task Router

Use this before routing any TELUS task.

## Contents

- [Non-Negotiables](#non-negotiables)
- [Strict Routing Protocol](#strict-routing-protocol)
- [Task Families](#task-families)
- [TELUS Families Without A Dedicated Skill](#telus-families-without-a-dedicated-skill)
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

Signals:

- Side-by-side search results.
- Overall Preference Rating or OPR.
- Result satisfaction labels `HS`, `S`, `SS`, `NS`.
- Search result flags such as Content Unavailable, Inappropriate, or Wrong Language.

Do not route Web Images or Search Ads here unless the task UI is clearly Search SBS.

### Bot Reply Validation / AI Assistant Human Evaluation

Use `telus-bot-reply-validator` (read `../../telus-bot-reply-validator/SKILL.md`).

Signals:

- Apple assistant response validation.
- Metrics: Accuracy, Relevancy, Compliance, Fluency, Safety, Overall Quality.
- Cited Apple resources or region-specific Apple claims.

Do not use Search SBS satisfaction labels here.

### Text Response Evaluation

Use `text-response-evaluator` (read `../../text-response-evaluator/SKILL.md`).

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

Signals:

- Image result rating.
- Image satisfaction and host-page satisfaction.
- Image flags such as Did not load, Unsafe, Near duplicate.
- Host-page flags and image side-by-side preference.

Do not use Search SBS `HS/S/SS/NS` here.

### Search Ads Relevance

Use `search-ads-relevance` (read `../../search-ads-relevance/SKILL.md`).

Signals:

- iOS App Store ad shown against a user search query.
- Ad-to-query relevance grading.
- Rating labels `Excellent`, `Good`, `Acceptable`, `Bad`.
- App Store listing links for the advertised app.

Guideline source: `TELUS-TASKS/SEARCH-ADS-RELEVANCE/guidelines.txt` and `TELUS-TASKS/SEARCH-ADS-RELEVANCE/telus- SEARCH-ADS-RELEVANCE.pdf`.

Do not use Search SBS `HS/S/SS/NS` here.

### Close Variants

Use `close-variants-evaluator` (read `../../close-variants-evaluator/SKILL.md`).

Signals:

- An original query paired with a query variant.
- Spelling, abbreviation, reordering, transliteration, synonym, or language-transformation comparison.
- Rating labels `Good`, `Acceptable`, `Bad`.

Guideline source: `TELUS-TASKS/Close Variants/Telus - Close Variants.pdf`.

Do not confuse this with Search Ads Relevance. Close Variants compares a query to a variant query, not a query to an ad.

### Maps Search Evaluation

Use `maps-search-evaluator` (read `../../maps-search-evaluator/SKILL.md`).

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

## TELUS Families Without A Dedicated Skill

The workspace contains guidelines for these TELUS task types, but no separate installed skill has been built yet:

- Broad Match: `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf`
- Image Themes Rating: `TELUS-TASKS/Image-Themes-Rating/telus-Image_Themes_Rating.pdf`

If one appears, read its official guideline directly and tell the user no dedicated TELUS skill exists yet. Do not force it through a different TELUS skill.

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
