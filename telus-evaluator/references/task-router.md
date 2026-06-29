# TELUS Task Router

Use this before routing any TELUS task.

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

Use `search-sbs-evaluator`.

Signals:

- Side-by-side search results.
- Overall Preference Rating or OPR.
- Result satisfaction labels `HS`, `S`, `SS`, `NS`.
- Search result flags such as Content Unavailable, Inappropriate, or Wrong Language.

Do not route Web Images or Search Ads here unless the task UI is clearly Search SBS.

### Bot Reply Validation / AI Assistant Human Evaluation

Use `telus-bot-reply-validator`.

Signals:

- Apple assistant response validation.
- Metrics: Accuracy, Relevancy, Compliance, Fluency, Safety, Overall Quality.
- Cited Apple resources or region-specific Apple claims.

Do not use Search SBS satisfaction labels here.

### Text Response Evaluation

Use `text-response-evaluator`.

Signals:

- Text-message transcript.
- Transcript summary.
- Pass/Reject transcript decision.
- Rejection reasons such as emojis, spelling mistake, repetition, participant name, incoherent text, impossible text conversation, or rhyming.
- Best reply to the final text.
- Multiple-choice question about the transcript.

Judge response options only after transcript pass/reject rules are applied.

### Web Images Satisfaction

Use `web-images-satisfaction-evaluator`.

Signals:

- Image result rating.
- Image satisfaction and host-page satisfaction.
- Image flags such as Did not load, Unsafe, Near duplicate.
- Host-page flags and image side-by-side preference.

Do not use Search SBS `HS/S/SS/NS` here.

## TELUS Families Without A Dedicated Skill

The workspace contains guidelines for these TELUS task types, but no separate installed skill has been built yet:

- Broad Match: `TELUS-TASKS/BROAD-MATCH/telus-Broad_Match.pdf`
- Search Ads Relevance: `TELUS-TASKS/SEARCH-ADS-RELEVANCE/guidelines.txt` and `TELUS-TASKS/SEARCH-ADS-RELEVANCE/telus- SEARCH-ADS-RELEVANCE.pdf`
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
