# Web Images Rating Guide

Use this guide together with `TELUS-TASKS/WebImagesSingleSideImageSatisfaction/guideline.md`, which is the source of truth.

## Query Intent

- Research the query before rating.
- Identify the main visual need and any reasonable alternate visual intents.
- For broad or ambiguous queries, accept images that satisfy a reasonable intent.
- Ignore very unlikely interpretations unless the task context strongly supports them.

## Image Flags

`Did not load`: the image is missing or not loading in the task.

`Unsafe`: use for pornography/nudity, violence/gore, hate or discrimination, medically explicit content, recreational/illegal/prescription/OTC drug depiction, profane text, local-custom violations, or other upsetting content. Context matters: medical, educational, fine-art, or journalistic context is not automatically unsafe unless the guideline category applies.

`Near duplicate`: flag only when the image is a near duplicate of an image that appears higher in the same side/list. Do not compare duplicates across left vs right. The first image in a duplicate cluster is not flagged; lower-ranked duplicates are flagged.

Near duplicates include identical images, crops/full versions, mirrored/rotated/resized versions, minor color/filter/background changes, or minor watermark/logo/text/border differences.

## Image Satisfaction

`Highly Satisfying`: directly matches the query or a reasonable intent, excellent quality, clear, useful, and visually strong.

`Moderately Satisfying`: relevant and decent quality; mostly or fully addresses the query, but is not especially strong, beautiful, complete, or inspiring.

`Slightly Satisfying`: connected to the query but has major issues, satisfies only a weak/minor intent, misses an important part of a specific query, or has poor quality/cropping/resolution.

`Not Satisfying`: unrelated or virtually useless for the query.

For duplicate images, still assign image satisfaction based on the image itself; the duplicate flag is separate.

Text overlay:

- Fine when the query seeks text, memes, fonts, or text-based visuals.
- Demote when the query seeks an entity/product/concept and the text overlay does not help.

Watermarks/effects:

- Do not demote if they do not hurt image quality or usefulness.
- Demote when they distract, obscure the subject, or reduce usefulness.

Image size:

- Judge size/resolution in context. A small emoji can be fine; a low-resolution wallpaper is weak.

## Host Page Flags

`Did not load`: host page is unavailable or will not load.

`Unsafe`: host page contains inappropriate or harmful content, especially content inappropriate for children or harmful to adults. Medical pages can be safe unless they include gory or addictive-drug content.

## Host Page Satisfaction

Rate the host page by:

- Relevance: the page is about the entity/query and supports the image.
- Authenticity: the page presents the subject honestly without misleading context.
- Credibility: official site, well-known source, government, university/research institution, reputable organization, credible physical business, or externally validated site.
- Trustworthiness: accurate, reliable, verifiable information; avoid giving high host satisfaction to spam, fake-news, conspiracy, low-reputation, unknown personal, or deceptive sites.
- Presentation: clean, readable, easy to navigate, and not cluttered or misleading.

When credibility is uncertain, search the domain or use `site:<domain>` and look for reputable references, a Wikipedia entry, reviews, official ownership, or clear business/institution identity.

## Overall Side Preference

Image quality is the most important factor. Host-page quality is secondary but still matters.

Prefer:

- Good image + good host page over good image + bad host page.
- Good image + good host page over bad image + good host page.
- Good image + bad host page over bad image + good host page, because image quality has higher priority.

Also consider ranking, diversity, duplicates, freshness for time-sensitive queries, and fewer unsafe/did-not-load results.

Choose `About the Same` if the sides are identical, balanced, or the difference is not clear. If identical, comment exactly: `Identical.`

## Compact Comment Style

Use simple, natural wording:

`The query intent is to find images of [subject]. The left side is better because it has clearer, more relevant images and fewer weak host pages.`

`The query intent is to find images of [subject]. Both sides have similar image quality and host pages, so neither side has a clear advantage.`
