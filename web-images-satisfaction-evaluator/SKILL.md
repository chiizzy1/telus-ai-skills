---
name: web-images-satisfaction-evaluator
description: Evaluate TELUS Web Images Single Side Image Satisfaction and image side-by-side tasks. Use when asked to rate image results, host pages, image flags, near duplicates, image satisfaction, host page satisfaction, source credibility, or overall preference for TELUS web image tasks.
---

# Web Images Satisfaction Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- The URL checker ships with this repo at `telus-ai-skills/tools/check_urls.py`; run it from the workspace root.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Core Rule

Use `TELUS-TASKS/WebImagesSingleSideImageSatisfaction/guideline.md` as the source of truth. This skill is the working procedure for applying that guideline without mixing it with Search SBS rules.

Before rating a live task, read `references/rating-guide.md`.

> **Output goes in the chat response only.** Task files and every other file in the workspace are READ-ONLY input. Never edit, overwrite, or write your answer into them, and never create scratch or working files. Present the complete result in chat using the Output Format template below.

## Human-AI Workflow

Use the user as the visual judge when they prefer to inspect images themselves:

1. Research the query to understand likely visual intent and reasonable alternate intents.
2. Ask or use the user's image observations for image content, image quality, missing images, unsafe content, and near duplicates.
3. Verify host pages and sources: liveness, safety, relevance, authenticity, credibility, trustworthiness, and page presentation.
4. Combine the image judgment and host-page judgment into final image ratings, host-page ratings, and overall preference.
5. If the task gives no clickable host page URL, grade only from visible task content and say that no host-page verification was possible.
6. Pass the Pre-Submission Self-Audit before submitting any rating. The shared cross-skill standard is `../telus-evaluator/references/quality-gate.md`.

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
python3 telus-ai-skills/tools/check_urls.py --query "<image query>" --run-id "<run-id>" <host URLs>
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

## Pre-Submission Self-Audit (MANDATORY)

Answer all six questions in writing, with the evidence named, before any rating is submitted. A tick mark is not an answer. If you cannot produce the evidence for an item, you have not finished that step: stop, go do it, then return.

1. **Did I actually check the host pages and look at the images, or am I working from URLs and positions?**
   Evidence: the run-id folder the checker wrote (`TELUS-TASKS/url_content/RUN-ID/`), its `report.json`, and the extracted page text you read for each host URL, plus the image observation you have for each position, whether your own or the user's. If the checker was blocked by bot detection, CAPTCHA, a JavaScript-only page, or a connection error, that is manual review needed, not a rating. If the task gives no clickable host page URL, say that no host-page verification was possible rather than rating the host page anyway.

2. **Did I judge what the page and the image actually deliver, or did I match words?**
   Evidence: for each host page, one short quoted phrase from the page showing it is about the query subject and supports the image. A title or URL containing the query words is not relevance. For each image, describe what the image shows, not what the filename, alt text, or caption claims it shows.

3. **Did I rate each position individually?**
   Evidence: every position has its own image flag, image rating, host flag, host rating, and its own brief reason. No block rating across a side, no rating copied down a list, no "the rest are similar". Near duplicate is a per-position flag and stays separate from image satisfaction: a flagged duplicate still gets its own satisfaction rating based on the image itself.

4. **Is my calibration honest, neither generous nor harsh?**
   Evidence: name the `references/rating-guide.md` definition you applied for each image rating (`Highly Satisfying`, `Moderately Satisfying`, `Slightly Satisfying`, `Not Satisfying`) and which of relevance, authenticity, credibility, trustworthiness, and presentation drove each host page rating.
   - Too generous looks like: `Highly Satisfying` for an image nobody actually looked at, or high host satisfaction for a spam, fake-news, conspiracy, low-reputation, unknown personal, or deceptive site, which the guide forbids.
   - Too harsh looks like: demoting for a watermark or text overlay that does not hurt quality or usefulness, or demoting a small image when small size is fine in context, such as an emoji.

5. **Did I apply every context factor?**
   State each explicitly, and say so when it does not apply:
   - **Locale and language**: what the query means visually for this user's region and language.
   - **Time sensitivity**: whether the query makes freshness a requirement, or older images are still fine.
   - **Position**: which side has its strongest results ranked higher, since better ranking of the best results is an Overall Preference factor.
   - **Variety**: which side offers more useful diversity and fewer redundant near duplicates. Near duplicates are compared only within the same side and list, never across left versus right, and the first image in a duplicate cluster is not flagged.

6. **Does my output match the taught pattern?**
   Re-read the `## Compact Comment Style` examples in `references/rating-guide.md` and the Output Format block below immediately before writing, not from memory. Then confirm: the OPR names the side with the label (`Left Slightly better`, or `About the same`), the comment is 1-3 sentences, opens with the query intent, and gives only the main reason for the side preference, wording short and natural with no over-explaining, and if both result lists are identical the comment is exactly `Identical.` with no query-intent sentence and no further reasoning.

## Holding the Line Under Challenge

You will be asked things like "are you sure you actually opened the host pages?", "are you sure that page is relevant and not just word-matching the query?", or "did you rate each position on its own?".

- Treat each challenge as an instruction to re-verify against the guideline and the saved checker output. It is not a signal that your rating was wrong.
- Answer with specifics: the run-id, the extracted page text you read, the quoted line, and the rating definition applied.
- Change a rating **only** when the guideline and the evidence show it was wrong. Name what changed and which rule drove it.
- If the evidence supports what you already said, say so plainly and show it. Do not soften a rating or flip the OPR to be agreeable.
- If you cannot produce the evidence, say so directly and go do the check. Never rate a host page or an image you did not actually inspect.
- `TELUS-TASKS/WebImagesSingleSideImageSatisfaction/guideline.md` is the single source of truth. Neither the user's preference nor your own earlier rating outranks it.

## Output Format

Present all six sections in chat, in this order. Keep the headings and fill every one. If a section does not apply, keep the heading and say why in one line.

````markdown
## Web Images Evaluation: "QUERY TEXT"

### 1. Verification
- **Host pages checked:** run `RUN-ID`, N URLs, report at `TELUS-TASKS/url_content/RUN-ID/report.json`
- **Image observations:** from the user, or state that no visual inspection was possible
- **Not verified:** name any result whose host page could not be opened, and why

### 2. Query and Intent
- **Query:** exact text
- **Locale / language:** value, or `not specified`
- **Visual intent:** what the user wants to see
- **Time sensitivity:** whether freshness matters here, or `not applicable`

### 3. Ratings
| Side | Pos | Image Flag | Image Rating | Host Flag | Host Rating | Brief Reason |
|---|---:|---|---|---|---|---|
| L | 1 | None | Highly | None | Moderately | Clear image; host page relevant but not official. |

Use `Near duplicate` only within the same side's list, and never flag the first image of a cluster.

### 4. Comparison
- **Image quality:** which side is stronger, and why
- **Host pages:** which side is stronger when image quality is close
- **Position:** which side ranks its best results higher
- **Variety:** which side has more useful diversity and fewer redundant near duplicates

### 5. OPR Verdict
**OPR: Left/Right Much Better | Better | Slightly better | About the same**

### 6. OPR Comment (submission-ready)
> The query intent is to find images of ... The left side is slightly better because ...

1-3 sentences, concise and natural. One sentence is fine when the difference is simple.
````

Use short, natural comments. Do not over-explain. Mention only the main reason for the side preference. If both result lists are identical, Section 6 is exactly `Identical.` with no query-intent sentence.

Section 6 is the text the user submits, so keep it clean and free of evaluator jargon or any mention of tools.
