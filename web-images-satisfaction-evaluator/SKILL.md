---
name: web-images-satisfaction-evaluator
description: Evaluate TELUS Web Images Single Side Image Satisfaction and image side-by-side tasks. Use when Codex is asked to rate image results, host pages, image flags, near duplicates, image satisfaction, host page satisfaction, source credibility, or overall preference for TELUS web image tasks.
---

# Web Images Satisfaction Evaluator

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

- Use the task UI's host-page satisfaction labels. If the UI uses the same four-level scale, apply `Highly`, `Moderately`, `Slightly`, and `Not` based on relevance, authenticity, credibility, trustworthiness, and presentation.

## Host Page Verification

For every host page URL, verify the exact page when possible. Use the repo checker when useful:

```powershell
python TELUS-TASKS/scripts/check_urls.py --query "<image query>" --run-id "<run-id>" <host URLs>
```

Inspect the generated `report.json` and extracted text. If the checker fails because of bot-blocking, CAPTCHA, JavaScript-only pages, or connection issues, treat it as manual-review needed, not an automatic grade. If normal/manual access confirms the host page does not load, flag `Did not load`.

## Overall Preference

Prefer the side with:

1. Better image satisfaction, with image quality weighted more than host-page quality.
2. Better host pages when image quality is similar.
3. Better ranking of the best results.
4. More useful diversity and fewer redundant near duplicates.
5. Fewer `Did not load` or `Unsafe` results.

If both lists are identical, choose `About the Same` and comment `Identical.`

If the difference is unclear or balanced, choose `About the Same`.

## Output Format

Keep output compact unless the user asks for detailed reasoning:

```markdown
| Side | Pos | Image Flag | Image Rating | Host Flag | Host Rating | Brief Reason |
|---|---:|---|---|---|---|---|
| L | 1 | None | Highly | None | Moderately | Clear image; host page is relevant but not official. |

OPR: Left Slightly Better

The query intent is to find images of ... The left side is slightly better because ...
```

Use short, natural comments. Do not over-explain. Mention only the main reason for the side preference.
