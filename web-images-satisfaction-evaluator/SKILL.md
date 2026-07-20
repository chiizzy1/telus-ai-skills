---
name: web-images-satisfaction-evaluator
description: Evaluate TELUS Web Images Single Side Image Satisfaction and image side-by-side tasks. Use when asked to rate image results, host pages, image flags, near duplicates, image satisfaction, host page satisfaction, source credibility, or overall preference for TELUS web image tasks.
---

# Web Images Satisfaction Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Core Rule

Use `TELUS-TASKS/WebImagesSingleSideImageSatisfaction/guideline.md` as the source of truth. This skill is the working procedure for applying that guideline without mixing it with Search SBS rules.

Before rating a live task, read `references/rating-guide.md`.

## Human-AI Workflow

Use the user as the visual judge when they prefer to inspect images themselves:

1. Research the query to understand likely visual intent and reasonable alternate intents.
2. Ask or use the user's image observations for image content, image quality, missing images, unsafe content, and near duplicates.
3. Verify host pages and sources: liveness, safety, relevance, authenticity, credibility, trustworthiness, and page presentation.
4. Combine the image judgment and host-page judgment into final image ratings, host-page ratings, and overall preference.
5. If the task gives no clickable host page URL, grade only from visible task content and say that no host-page verification was possible.

## Rating Scales

Do not use Search SBS `HS/S/SS/NS` labels for this task type.

Image satisfaction:

- `Highly Satisfying`
- `Moderately Satisfying`
- `Slightly Satisfying`
- `Not Satisfying`

Image flags:

- `Did not load`
- `Unsafe`
- `Near duplicate`
- `None`

Host page flags:

- `Did not load`
- `Unsafe`
- `None`

Host page satisfaction:

- Use the task UI's host-page satisfaction labels. If the UI uses the same four-level scale, apply `Highly`, `Moderately`, `Slightly`, and `Not` based on relevance, authenticity, credibility, trustworthiness, and presentation. Otherwise use the labels the UI shows and map by severity, keeping the same order from most to least satisfying.

Overall preference (OPR):

The UI groups the options by side. `About the same` appears in both groups and means the same thing either way.

LEFT:

- `Much Better`
- `Better`
- `Slightly better`
- `About the same`

RIGHT:

- `Slightly better`
- `Better`
- `Much Better`
- `About the same`

State the side with the label when you report the rating, for example `Left Slightly better` or `About the same`.

Never import the Search SBS scale or its `HS/S/SS/NS` grades into this task.

## Host Page Verification

For every host page URL, verify the exact page when possible. Use the repo checker when useful:

```bash
python3 TELUS-TASKS/scripts/check_urls.py --query "<image query>" --run-id "<run-id>" <host URLs>
```

The script writes its report to `TELUS-TASKS/url_content/<run-id>/report.json`, alongside the extracted page text for each URL. Inspect both. If the checker fails because of bot-blocking, CAPTCHA, JavaScript-only pages, or connection issues, treat it as manual-review needed, not an automatic grade. If normal/manual access confirms the host page does not load, flag `Did not load`.

## Overall Preference

Prefer the side with:

1. Better image satisfaction, with image quality weighted more than host-page quality.
2. Better host pages when image quality is similar.
3. Better ranking of the best results.
4. More useful diversity and fewer redundant near duplicates.
5. Fewer `Did not load` or `Unsafe` results.

If both result lists are identical, choose `About the same` and comment exactly `Identical.` This overrides the standard comment template below. Do not add a query-intent sentence or any further reasoning.

If the difference is unclear or balanced, choose `About the same` and use the standard comment template.

## Output Format

Keep output compact unless the user asks for detailed reasoning:

```markdown
| Side | Pos | Image Flag | Image Rating | Host Flag | Host Rating | Brief Reason |
|---|---:|---|---|---|---|---|
| L | 1 | None | Highly | None | Moderately | Clear image; host page is relevant but not official. |

OPR: Left Slightly better

The query intent is to find images of ... The left side is slightly better because ...
```

Use short, natural comments. Do not over-explain. Mention only the main reason for the side preference.
