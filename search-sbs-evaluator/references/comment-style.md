# Search SBS — OPR Comment Style

Use with `../SKILL.md`. This file is the authoritative source for how the submission-ready OPR comment is written.

> [!CAUTION]
> **PUNCTUATION RULE:** Always use American English formatting. You MUST place all periods and commas INSIDE the quotation marks (e.g., "like this," not "like this",).

## Contents

- [Golden Rule: Brief, Precise, Human](#golden-rule-brief-precise-human)
- [Required Flow](#required-flow)
- [Required Shared-Result Check](#required-shared-result-check)
- [OPR Comment Structure](#opr-comment-structure)
- [Examples](#examples)
- [Anti-Pattern (NEVER do this)](#anti-pattern-never-do-this)
- [Good Pattern (Write like this instead)](#good-pattern-write-like-this-instead)

## Golden Rule: Brief, Precise, Human

- **1-3 sentences.** That's it. Don't write a paragraph when a sentence will do, and don't pad a clear call into three sentences just to fill the range.
- **Write like a human.** Flow naturally. No robotic structure. Avoid highly formulaic or repetitive templates (e.g., "The left side fails to X and only provides Y, while the right side successfully Z, making it better despite W"). Instead, use conversational but professional phrasing (e.g., "The right side is better because it recognizes the misspelling..., while the left side completely misses the mark by...").
- **Do not add unnecessary details.** For example, if a query is a misspelling, you don't need to explain the mechanics of voice-dictation errors. Just state the likely intent.
  - **BAD:** *"The query contains voice-dictation errors for 'Olipop' and 'Poppi' sodas, and the intent is to compare their sugar content. The right side is better because it is fully accessible and features a highly authoritative article that explicitly answers the question by directly comparing the sugar grams of both brands. In contrast, the left side is heavily weighed down by three inaccessible results that require manual review, making it a much poorer experience."*
  - **GOOD:** *"The query intent is likely to compare 'Olipop' and 'Poppi' sodas sugar content. The right side is better because it features a highly authoritative article that explicitly answers the question by directly comparing both brands. In contrast, the left side is bogged down by three inaccessible results that require manual review."*
- **Do not explain flags, 404s, or paywalls in detail.** The grading table already documents the flag. Keep the comment simple and focused on the user experience.
  - **BAD (Robotic & Over-explained):** *"The left side is much better because it provides a fully accessible, highly relevant guide (L2) that directly compares the two brands. In contrast, the right side's only direct comparison result (R5) is blocked by a hard subscription paywall, leaving the user with no accessible answers to their specific question."*
  - **GOOD (User's Phrasing):** *"The left side is much better because it provides an accessible, direct comparison of the two brands, whereas the right side results are less satisfying and it has an R5 result that requires subscription."*
  - **GOOD (No Connective Fluff):** *"The left side is much better because it provides an accessible, direct comparison of the two brands, whereas the right side's only comparison is inaccessible."*
- **Use plain English for intent.** Always phrase it as "The query intent is to [plain user need]." NEVER use technical jargon like "navigational intent", "advice intent", or "local maps intent" in the comment. NEVER use internal evaluator jargon like "entity," "entity confusion," or "classification." Use everyday human words like "typo," "misspelling," or "mix-up" instead.
- **NEVER use em dashes (—).** Use commas, colons, periods, or parentheses.
- **No AI filler words.** No "delve," "moreover," "furthermore," "it's worth noting."
- **Do NOT list individual sources by name.** Say "reputable sources" or "authoritative sources."
- **Do NOT explain flags or 404s in detail.** The grading table already documents that.
- **NEVER mention automated tools in OPR comments.** No "bot-blocked," "script," "check_urls," "403," "status code," or any language that reveals automated verification. Describe issues in human terms (e.g., "inaccessible page" instead of "bot-blocked 403").
- **At least 20 words. Required on TryRating, not a target.** Count before submitting; a short clear call still needs 20 words.
- Explain the choice through what the guideline asks comments to cover: **relevance, diversity and presentation**. In practice that is which side's results are more satisfying, whether one side covers more useful result types or meanings, and whether the best results sit higher.

## Required Flow

1. **State the intent** in one clause using plain English. You MUST ALWAYS start the entire comment with the exact phrase "The query intent is..." — no exceptions.
2. **Acknowledge both sides** — recognize overall quality before differentiating.
3. **State the OPR and why.**

These are the beats the comment must hit, not a sentence count. Combine them freely: when the call is simple, all three fit in one natural sentence, and that is better than stretching it. Use the second and third sentence only when the difference genuinely needs them.

- **One sentence:** *"The query intent is to find the official Nike store, and the right side is better because it leads with the official site while the left side only offers resellers."*
- **Two sentences:** *"The query intent is to compare 'Olipop' and 'Poppi' sodas sugar content. The right side is better because it features an authoritative article that directly compares both brands, while the left side is bogged down by inaccessible results."*

## Required Shared-Result Check

When both sides share one or more meaningful results, the OPR comment must explicitly mention the shared results first, then mention whether the unique results on each side also satisfy the query. 

**CRITICAL RULE - Be Accurate with Shared Results:**
Do not use the clunky and misleading phrase "Both sides share the same results" when only a portion of the results are shared. Instead, state the exact number of shared results for natural accuracy.

If the task UI explicitly labels results with "Same as L#", use the word **"share"**:
- "Both sides share two results, but the left side is better because..."
- "Both sides share three results, but..."

If the two sides simply have identical URLs but they are NOT explicitly grouped or labeled as "Same as" in the task UI, use the phrase **"have similar results"** instead:
- "Both sides have two similar results, but..."

## OPR Comment Structure
Every OPR comment covers these parts, in this order:
1. **State the query intent** ("The query intent is to...").
2. **Acknowledge shared results accurately** (e.g., "Both sides share two results") — only when the sides actually share results.
3. **State which side is better** ("but the [left/right] side is [rating]").
4. **State exactly why the better side is better** ("because...").

Parts, not sentences. Parts 2 through 4 usually read best as a single sentence, and with no shared results the whole comment can be one.

Example pattern:
> `The query intent is to [plain user need]. Both sides share [number] results, but the [left/right] side is [rating] because [exact reason why it is better].`

For About the Same:
> `The query intent is to [plain user need]. Both sides [short fair comparison], so neither side has a clear overall advantage.`

## Examples

> **Example (Super Concise - Stripping Unnecessary Details):**
> The query intent is to find out Pamela Bondi's age. Both sides share two relevant results, but the right side is better because it groups the results with her correct current age at the top (R1, R2, R3), whereas the left side prominently features an outdated article.

> **Example (Explicitly shared via "Same as L1"):**
> The query intent is to know how many layers the dermis has. Both sides share four results, but the left side is slightly better because its unique result, L5, answers the question more clearly than R5.

> **Example (Similar results, identical URLs but NO "Same as" label):**
> The query intent is to find the lyrics to the song Heavenly Choir by The Canton Spirituals. Both sides have two similar results that directly answer the query, but the left side is slightly better because the right side includes a video for a completely different song at R4.

> ❌ The query intent is to find the lyrics to the song Heavenly Choir by The Canton Spirituals. Both sides share the same results, but the left side is slightly better because its unique results provide more helpful lyrics pages, while the right side includes a video for a completely different song at R4.

> The query intent is to find out whether debt consolidation is a smart financial decision. Both sides are about the same because they equally satisfy the user's need with relevant results from reputable financial sources that directly address the question.

> The query intent is Yahoo News and the user most likely wants the main page of headlines from that site. Both sides share two results at the top, but the right side is slightly better because R5 is a fresher and more relevant news result.

> The query intent is to learn how to turn off Speak Screen on an iPhone. Both sides have three similar useful iPhone pages, but the left side is slightly better because its strongest page appears higher, while the right side starts with a less useful voice settings result.

> The query intent is to know when college usually starts in the fall. Both sides share three general results at the top, but the right side is slightly better because its unique result gives a general answer, while the left side's unique result is only for one college.

> The query intent is to get advice on rationing a limited lorazepam supply. Despite both sides providing general lorazepam dosage information, the left side is better because all its results are accessible and relevant, while the right side includes a broken page (R5) and a less relevant result at R1.

## Anti-Pattern (NEVER do this)

> ❌ "Both sides share the same Wikipedia article at position 1 and both have the same broken result at position 4, while the remaining results on each side are articles from specific named sites that all address the question in various ways, so both sides are about the same."

Too long, too mechanical, includes unnecessary result-by-result detail, and spends the comment on evidence already present in the grading table.

> ❌ "The query intent is to find the correct spelling for a specific rainforest (likely Luquillo or Luzon). The left side fails to identify the entity and only provides generic spelling results for the word "rainforest," while the right side successfully recognizes the misspelling and provides authoritative results for Luquillo and Luzon, making it better despite a broken link at R4."

Rejected because it is too robotic and formulaic ("The left side fails to [X] and only provides [Y] while the right side successfully [Z] making it better despite [W]"). It reads like a Mad Libs template.

> ❌ "The query intent is to find out when the 'Arctic Treaty' was signed, since the user's input 'arctic tree' is a clear voice-to-text error. The right side is much better because it provides a perfectly well-rounded response to this ambiguous intent, clarifying that there is no single Arctic Treaty while also covering actual Arctic agreements and the highly likely confusion with the Antarctic Treaty. The left side is a complete failure because it takes the garbled query literally and returns useless results about the Arctic tree line."

Rejected because it sounds overly formal, wordy, and relies on heavy "AI-speak" (e.g., "perfectly well-rounded response", "ambiguous intent"). It over-explains the grading rationale instead of getting straight to the point.

## Good Pattern (Write like this instead)

> ✅ "The query intent is to find the correct spelling of a specific rainforest, likely Luquillo. The right side is better because it recognizes the misspelling and provides authoritative results for the Luquillo and Luzon rainforests, while the left side completely misses the mark by just giving generic dictionary pages for the word 'rainforest.'"

Accepted because it flows naturally, uses conversational phrasing ("misses the mark", "just giving generic..."), and sounds like a human evaluator explaining their reasoning rather than a machine filling out a form.

> ✅ "The query intent is to find a street in Arizona called Bridge Canyon Parkway. Both sides are about the same because they both fail to show the actual street. Instead, they just give random hiking trails and parks that happen to have 'Bridge Canyon' in their names."

Accepted because it uses very simple, natural grammar without overcomplicating the sentence structure or relying on technical jargon.

> ✅ "The query intent is to find out when the Antarctic Treaty was signed. The right side is much better because it provides relevant results, while the left side completely misses the mark by taking the typo literally."

Accepted because it cuts straight to the core of the issue with absolute brevity. It is punchy, direct, and avoids any robotic fluff or over-explanation.

