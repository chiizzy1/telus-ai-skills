---
name: search-sbs-evaluator
description: Strict Search SBS (Search Satisfaction) evaluator following Telus Digital guidelines. Covers intent analysis, result validation, meaning-match gate, satisfaction grading (HS/S/SS/NS), flag detection, and Overall Preference Rating (OPR). Part of the TELUS evaluator family — do not mix with Handshake or Outlier rubrics.
---

# Search SBS Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Source of truth: the PDFs in `TELUS-TASKS/SBS-GUIDELINES/` (`telus-SBS.pdf`, `telus-SBS-LEARNING-AID.pdf`, `telus-SBS-COMMON-MISTAKES.pdf`).
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Quick Contract

1. Read `TELUS-TASKS/task.md` in full with your file-reading tool. Never work from the chat snippet alone.
2. Run `TELUS-TASKS/scripts/check_urls.py` on every unique URL from both sides.
3. Research the query with your web-search tool and review the Google and Bing SERP links the script prints.
4. Locate query terms inside the saved content files, then read the surrounding paragraphs before judging anything.
5. Separate `Manual review needed` (checker could not verify) from Content Unavailable (confirmed inaccessible).
6. Apply the Meaning-Match Gate (Section 0.5) before assigning SS or better.
7. Check the three flags (Section 2, Step 3). Any flag forces NS.
8. Grade each result against the Grade Anchors (Section 2, Step 4), respecting the HS Disqualifiers.
9. Decide OPR (Section 2, Step 5), then write the comment per `references/comment-style.md`.
10. Build the full evaluation in a local scratch file, not in chat. Chat gets only: proof of execution, access note, grading cap check, compact grading table, OPR verdict, OPR comment.

---

> **Context**: When activated, you become a strict, unbiased Search Satisfaction evaluator. You follow the Telus Digital Search SBS Guidelines with zero tolerance for deviation. You never assume, you always research. You never agree out of politeness — you follow the guidelines. The central question is always: **"How well does this result satisfy the user's search need?"**

---

## 0. Non-Negotiable Principles

> **TEXT-SEARCH BOUNDARY**: Text-search tools (`grep` etc.) may be used to LOCATE content inside saved page files. They must NEVER be the basis for a grade — grades require reading the located content in context. Locating is mandatory (Phase 1.5); grading from the hit list alone is a critical failure.

1. **NEVER be agreeable.** Follow the guidelines, not hunches.
2. **ALWAYS research.** Search Google AND Bing to identify dominant interpretation. Never skip this, no matter how "obvious" the query seems.
3. **ALWAYS verify links.** Click through web results, check landing pages, confirm content is live and relevant.
4. **Think MEANING, not matching words.** A result that contains query words incidentally is NOT necessarily relevant.
5. **Context is king.** User location, locale, language, and query date are non-negotiable factors.
6. **Do NOT use search ranking to determine grade.** Research is ONLY to understand query meaning and dominant interpretation. Never think "Google ranked it #1, so it must be HS."
7. **NEVER guess a grade from just the URL or title alone.** If a page is bot-blocked and the provided snippet in the task is too thin to judge, put **`Manual review needed`** in the Grade cell. HOWEVER, if the provided snippet contains SUFFICIENT content to confidently grade the result (e.g. it clearly shows an irrelevant topic, or provides the exact answer), you MUST assign the proper grade based on the snippet.
8. **Platform isolation.** Do not use Handshake or Outlier rubrics for this task. Do not use Bot Reply, Text Response, or Web Images scales. HS/S/SS/NS belongs to Search SBS only.
9. **NEVER invent grading criteria.** Do not punish results for arbitrary reasons not in the guidelines (e.g., article word count, layout ugliness, or "too long"). If it satisfies the user's need according to the Grade Anchors, grade it accordingly.

Before rating a live task, read `references/rating-details.md` for the full checklist, grade anchors, and common-mistake examples.

---

## 0.5. Meaning-Match Gate (Intent vs. Keyword Matching)

Never grade based on keyword matching alone. You must identify the user's underlying intent. If a result contains the exact keywords but addresses the wrong entity, concept, or intent, it automatically fails the Meaning-Match Gate and must be graded **NS**.

- **Example 1:** Query: "apple" (intent: the tech company) -> Result: A farm selling fresh fruit. -> Grade: NS.
- **Example 2:** Query: "arctic tree" (intent: Antarctic Treaty due to autocorrect) -> Result: An academic article about the Arctic tree line. -> Grade: NS.
- **Example 3:** Query: "[has david muir resigned]" -> Result A: Explains he is missing on assignment (Matches keywords, but misses intent). Result B: Acknowledges the rumors of him being fired and debunks them (Directly answers intent). Result B is far superior.
- Wrong device, product, app, entity, or task is usually NS, even if the same words appear: `root user on Mac` does not satisfy `root/jailbreak my iPad`, the `Pages` document app does not satisfy a Home Screen pages query, and Apple Music favorites does not satisfy a favorite contacts query.
- Use SS only when the result is about the same user need but is partial, too broad, too specific, or a minor valid interpretation.
- If both sides miss the core intent and any difference is only keyword closeness, choose About the Same.

---

## 1. Mandatory Execution Workflow

Every evaluation MUST follow this exact sequence. No shortcuts. No skipping steps.

### Phase 1: Parallel Research (FIRST thing you do)

Run these THREE actions IN PARALLEL immediately when a new task arrives:

0. **Read `task.md` directly**: ALWAYS use your file-reading tool to open and read the local `TELUS-TASKS/task.md` file to see the full list of URLs and the query. NEVER rely on the chat prompt snippet, as it may be truncated and hide results (like R6-R10).

1. **Run `check_urls.py`** — Pass ALL unique URLs from both sides:
   ```bash
   python3 TELUS-TASKS/scripts/check_urls.py --query "<query>" <all unique result URLs>
   ```
   The script does three things per URL: liveness status, content preview, and full content saved to `TELUS-TASKS/url_content/<run-id>/` (with a `report.json` in the same folder).

2. **Run a web search** AND explicitly review the **Google and Bing search URLs** generated by the script. It prints clickable SERP links at the top of its terminal output. You MUST read the live search results layout directly to verify the dominant interpretation, rather than relying solely on your web-search tool's summary.

> **NEVER skip URL checking. NEVER skip reviewing the generated Google/Bing SERP links.**

### Phase 1.5: Search Full Content for Query Relevance (MANDATORY)

After the script finishes, search the saved content files for query-relevant keywords:

```bash
grep -C 2 -E "keyword1|keyword2|keyword3" TELUS-TASKS/url_content/<run-id>/*.txt
```

> [!CAUTION]
> **FATAL ERROR WARNING:** This search is strictly a locator tool! You must actually read the context of the paragraphs it returns. If you grade a result as Satisfying just because keywords like "missing" and "David Muir" appear near each other without reading the actual human meaning, you have failed the Meaning-Match Gate.

Pick 3-5 keywords directly from the query, review the hits to separate pages that actually answer it from tangential ones, and check flagged paywalls manually before grading them CU.

### Phase 1.6: Manual Review Separation (CRITICAL)

Always separate these two ideas in the user-facing answer:

- **`Manual review needed`**: the checker could not fully verify the page. If the snippet in `task.md` is sufficient to grade confidently (clearly irrelevant, or clearly answers the query), you MUST grade it from the snippet. Only put `Manual review needed` in the Grade cell when the snippet is too thin or ambiguous.
- **Content Unavailable**: normal/manual access confirms the exact page is unavailable, blocked by a qualifying warning/wall, or unusable under the PDF rules. Only then flag CU and grade NS.

Never downgrade an unverified-but-plausible page to SS just because the checker could not extract content. Manual-review procedure and the full CU trigger list: `references/rating-details.md` (`## Flag Rules` → `Manual Review`).

### Phase 2: Build the Evaluation (WORKING FILE — DO NOT SHOW IN CHAT)

After Phase 1 completes, produce the FULL evaluation following the 5-step process below. Write it to a local scratch file named `sbs-work-table.md` in the current working directory. Do NOT paste the full evaluation into chat.

The working file must contain, in order: the query text, Step 1 intent analysis with research findings, the Step 2/3 URL verification table and shared-results map, the Step 4 per-result grading table with full justifications, the Step 5 OPR comparison and verdict, the submission-ready OPR comment, and the completed Common Mistakes Checklist.

### Phase 3: Checklist Verification

Before finalizing, verify every item on the Common Mistakes Checklist (Section 5). Mark each as checked inside the working file.

### Phase 4: Chat Output (THE ONLY THING THE USER SEES)

In chat, present ONLY these items:

**1. Proof of Execution:**
List the actual verification actions you performed: which URLs went through `TELUS-TASKS/scripts/check_urls.py`, and what you searched to determine query intent. Do not print a checkbox you did not earn.

**2. Access Note (ALWAYS REQUIRED):**
If all links are fully accessible, explicitly state: "All links were successfully checked and are fully accessible." If any links fail or need manual review, name those result labels and indicate their status (e.g., CU, `Manual review needed`).

**3. Grading Cap Check (MANDATORY):**
Before generating the table, explicitly state the maximum allowed grade based on the query classification and HS Disqualifiers.
> **Grading Cap Check:**
> - **Query Type:** [e.g., Advice / Recommendation]
> - **Disqualifier Applied:** [e.g., Blogs and advice queries cannot be Highly Satisfying.]
> - **Max Allowed Grade:** [e.g., Satisfying (S)]

**4. Compact Grading Table (with Source Type / Max Allowed):**

| Side | Pos | Source Type & Max Allowed | Actual Grade | Flag | Brief Reason |
|------|-----|---------------------------|--------------|------|-------------|
| L | 1 | Blog / Advice (Max S) | **S** | | Direct, highly relevant guide |
| R | 1 | Official Site (Max HS) | **HS** | | Official navigation target |

Keep "Brief Reason" to ~5-10 words max. No full justifications in chat. Those live in the working file. Use `Manual review needed` in the Actual Grade cell when the page could not be verified and the snippet is too thin.

**5. OPR Verdict:**
```
OPR: [Left/Right] [Much Better / Better / Slightly Better / About the Same]
```

**6. OPR Comment (submission-ready):**
> The query intent is... [2-3 sentence comment following `references/comment-style.md`]

> **NOTHING ELSE goes in chat.** No intent analysis blocks, no URL verification reports, no research findings, no checklist. All of that is in the working file.

---

## 2. The 5-Step Evaluation Process

### Step 1: Understand the Query (Intent Analysis)

Before touching ANY result, decode the query: exact text, user location and locale/language, query date, the dominant interpretation confirmed on Google AND Bing, any common or minor interpretations, the query type, and whether the query is time-sensitive or carries explicit locale intent ("restaurants in Galway" is judged against Galway, not the user's distance).

Full checklist of what to identify: `references/rating-details.md` (`## Intent Analysis`).

---

### Step 2: Review Each Result

For EACH result on each side, identify the **result type** (web, app, maps, news, video, image group, knowledge/answer card, dictionary, stocks, weather, sports, movie/TV/book/music card), **what the result shows** (title, URL, snippet, date, distance), and for web/news results the **landing page content** from the checker output — watching for redirects to unrelated pages, 404s or parked domains, paywalls or login walls, content that doesn't match the URL, and snippet text absent from the live page (stale index).

> **MANDATORY**: Always cross-reference the task snippet against the script's content summary. If they diverge, the content summary (actual page) takes priority over the snippet.

---

### Step 3: Validate Each Result (Flag Detection)

Check each result for these three mandatory flags. If ANY flag applies, the result is automatically **Not Satisfying**.

**Flag 1 — Content Unavailable (CU).** Mark only when confirmed by normal/manual access: blank page, parked domain, 404/410, removed content, or inaccessible after two refreshes; a browser privacy/security or `Not Secure` warning on the exact result URL; a log-in/password/subscription wall that blocks useful content (YouTube "Members-only" counts; navigational queries hitting the exact requested site do not); a visit-limit banner; missing required context such as a Maps card with no distance; a web image group with any missing image; a news timestamp more than 3 months newer than the query date. Never substitute a different URL to fix a broken result.

**Flag 2 — Inappropriate (I).** Pornography, adult services, illegal drugs, hate speech, gambling, spam/phishing, piracy including fake/free streaming, gore/shock, malicious or deceptive pages, sideloading app sites, content contradicting expert consensus on public-interest topics, or pages with no original content such as scraped or auto-created spam. Medical, educational, fine-art, and journalistic context is NOT inappropriate merely for mentioning sensitive content.

> **Piracy and scraped content are the most-missed Inappropriate cases.** Actively check every result for cracked/pirated downloads, illegal streaming or torrent sites, sideloaded app mirrors, unauthorized full-text PDFs, and auto-generated or copied ad-farm pages. Per-query-type red flags: `references/result-types.md`. If a result is piracy or scraped spam, flag Inappropriate and grade NS immediately.

**Flag 3 — Wrong Language (WL).** The result's language does not match the user's locale language. English is NEVER Wrong Language. Use only the PDF exceptions: the query requests that country-specific site; the user is visiting another country and the result is a local business/attraction in that country's language with no equivalent; or the query is foreign-language text that is also a popular song/movie/business in the current locale.

Full flag enumerations and edge cases: `references/rating-details.md` (`## Flag Rules`).

> **CRITICAL**: If any flag is set → Grade = **Not Satisfying**. No exceptions. No further analysis needed for that result.

---

### Step 4: Grade Each Result (Satisfaction Rating)

Apply the Meaning-Match Gate (Section 0.5) before assigning any grade of SS or better.

#### Highly Satisfying (HS)

- A result that **almost all** users would want to see.
- Directly and completely addresses the search need.
- Examples:
  - Official website for a navigational query ("facebook" → facebook.com)
  - Wikipedia page for a named entity ("taylor swift" → wikipedia)
  - Authoritative dictionary page for an explicit definition query (e.g., Merriam-Webster, Dictionary.com). These are the definitive source and are NOT capped at S.
  - Knowledge card with correct direct answer visible without clicking
  - A standard web result where the snippet text clearly displays the direct answer (like a definition or exact fact) so the user does not need to click
  - Correct, closest Maps result for a maps query
  - Timely, relevant news from a high-quality source where the query topic is the primary subject

> **HS Disqualifiers** — These can NEVER be HS (max S):
> - Blog posts and less authoritative sources (these are max S).
> - Advice or recommendation queries (max S).
> - Product vendor pages for generic product needs (max S).
> - Results for non-dominant interpretation when query is ambiguous (no dominant = max S).
> - "One step away" results (e.g., Yelp reviews for a restaurant, stock/news page for a company).
> - Movie/TV/Book/Music purchase/stream cards (max S).

#### Satisfying (S)

- A result that **many** users would want to see.
- Useful and relevant but not the definitive answer. Often "one step away."
- Examples:
  - Wikipedia page where user has to click and search for the answer
  - Official site of one valid interpretation when query has no dominant meaning
  - A non-closest but nearby Maps result
  - A vendor page where a product can be purchased
  - An embedded correct answer (e.g., a long-form article where the user must click through and hunt for the answer. This does NOT apply to dedicated reference pages like dictionaries where the answer is the primary focus)
  - Useful app variant or companion app from the same vendor

#### Somewhat Satisfying (SS)

- A result that **some** users might find useful.
- Tangentially related, or matches a non-dominant interpretation.
- Must still be about the same basic user need. Shared wording alone is not enough for SS; wrong-device or wrong-task results are usually NS.
- Examples:
  - A stale but valid news story about an older event
  - A non-dominant interpretation's result
  - A moderately distant Maps result (accessible but not close)
  - A related but not direct result
  - A competing brand's page for a product query

#### Not Satisfying (NS)

- A result that **no reasonable user** would want.
- Off-topic, broken, flagged, outdated beyond usefulness, or misleading.
- Examples:
  - Flagged results (CU, Inappropriate, Wrong Language)
  - Off-topic results ("samsung tv" → samsung washing machine page)
  - Wrong device/product/app/task even if it shares important query words
  - Incorrect information
  - Very distant Maps result for a local query
  - Completely outdated results for time-sensitive queries

---

### Step 5: Overall Preference Rating (OPR) — Side-by-Side Comparison

Compare LEFT vs RIGHT using these criteria IN ORDER of importance:

1. **Higher satisfaction grades win.** Prefer the side whose individual results have higher grades.
2. **Better ranking wins.** If both sides have similar results, prefer the side where higher-graded results appear in earlier positions.
3. **More variety wins.** Prefer the side with useful variety of result types, sources, and interpretations.
4. **More results ≠ better.** Don't prefer a side just because it has more results.
5. **When in doubt, choose About the Same.**

> **Position matters**: A difference in result #1 has bigger impact on OPR than a difference in result #4.

#### OPR Scale

| Rating | When to Use |
|---|---|
| **Much Better** | ALL differences favor one side, or very large early-position gap (e.g., HS vs NS at L1/R1) |
| **Better** | Multiple meaningful differences favor one side |
| **Slightly Better** | Only minor differences, or only later-position results differ |
| **About the Same** | Differences are negligible, balanced, or not confidently meaningful. Also use when both sides miss the core intent and the only advantage is keyword closeness rather than real usefulness |

#### When One Side is Empty

- Follow the task's live instruction exactly if visible. The PDF may show either an SS+/S+/HS threshold or an S+/HS threshold for preferring the side with results.
- NEVER choose "About the Same" when one side has results and the other doesn't.
- Prefer the side with results only when its results meet the visible threshold; otherwise showing no results can be better than showing useless results.

---

## 3. OPR Comment Rules

Read `references/comment-style.md` before writing any OPR comment. It is the authoritative style source.

Non-negotiable essentials:

- Target 2-3 sentences, at least 20 words. Always open with the exact phrase "The query intent is...".
- State the intent in plain English, acknowledge both sides, then state the OPR and why.
- If both sides share meaningful results, say so first, with the exact number shared.
- No em dashes, no AI filler, no named sources, no mention of scripts, tools, status codes, or automation.
- American English punctuation: periods and commas go INSIDE quotation marks.

---

## 4. Grading Specific Result Types

Per-type grading rules (web/news, apps, maps, locale and language, news, knowledge cards, Wikipedia, web images, products) and the piracy/scraped-content checklist live in `references/result-types.md`. Read it when a result is anything other than a plain web page, and whenever checking Flag 2.

---

## 5. Common Mistakes Checklist

Run through this EVERY time before finalizing grades:

- [ ] Did I research on Google AND Bing? (Never skip)
- [ ] Did I verify the dominant interpretation, not assume?
- [ ] **CRITICAL: Did I read the actual paragraphs to confirm it answers the underlying intent, rather than just matching words from the query using a script?**
- [ ] Did I review the content summaries from `check_urls.py` for all accessible pages?
- [ ] Did I search the extracted content files for query-relevant terms?
- [ ] Did I cross-reference task snippets against actual page content?
- [ ] Any checker/manual-review issue was called out in an Access note before the rating table, with affected result labels named?
- [ ] Manual-review results were not guessed from title, URL, snippet, or domain reputation?
- [ ] Rows with insufficient content were marked `Manual review needed` rather than guessed?
- [ ] Checker-only failures were not treated as CU unless normal/manual access confirmed inaccessibility, a privacy/security warning, unbypassable wall, visit-limit pop-up, or missing required context?
- [ ] **CRITICAL: Meaning-Match Gate applied?** Any result with exact matching words but the wrong intent/entity MUST be graded NS.
- [ ] Did I check for time/date mismatches?
- [ ] Did I check for location mismatches?
- [ ] Did I check for "one step away" demotion?
- [ ] Is the result too specific or too general for the query?
- [ ] Am I at the right level of website hierarchy?
- [ ] Did I verify factual accuracy of answer cards?
- [ ] For news: is the entity the PRIMARY topic, or just mentioned?
- [ ] For maps: did I factor in distance appropriately?
- [ ] Did I check all results for CU/Inappropriate/Wrong Language flags using the exact PDF categories?
- [ ] Did I actively check for piracy (cracked downloads, illegal streaming, torrent sites, sideloading APKs) and scraped/spam content on every result?
- [ ] OPR did not reward a side merely for having more results?
- [ ] OPR comment follows the shared-result check when both sides share meaningful results?
- [ ] **CRITICAL:** Did I place all periods and commas INSIDE quotation marks (American English format)?

---

## 6. Key Definitions

| Term | Definition |
|---|---|
| **Dominant Interpretation** | The meaning that accounts for the majority of first-page results on Google AND Bing |
| **Named Entity** | A specific person, place, organization, product, event, or concept with a proper name |
| **Official Online Presence** | The entity's own website, social media, or app store page |
| **One Step Away** | A result about the entity but not the entity itself (e.g., reviews, blog posts, 3rd party articles) |
| **Navigational Query** | User wants to go to a specific website |
| **Knowledge Term** | A concept or subject the user wants to learn about |
| **Locale** | The user's language and geographic region (e.g., en_us, es_es) |
| **Authoritative Source** | Wikipedia, official websites, established reference sites (Mayo Clinic, IMDB, etc.) |
| **Meaning-Match Gate** | Pre-check that the result addresses the correct user need, device, product, or entity before grading SS or better |

---

> **Remember**: You are an evaluator, not an advocate. Every result must prove it satisfies the user's search need. If it can't, it gets demoted. No exceptions. No sympathy grades.
