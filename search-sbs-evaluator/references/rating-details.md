# Search SBS Rating Details

Use this reference before rating a live TELUS Search SBS task. The main `SKILL.md` contains the execution workflow and compact rules; this file contains the guardrails and examples that prevent common grading mistakes.

## Contents

- [Non-Negotiables](#non-negotiables)
- [Intent Analysis](#intent-analysis)
- [Flag Rules](#flag-rules)
- [Grade Anchors](#grade-anchors)
- [Result-Type Examples](#result-type-examples)
- [Common Mistakes Checklist](#common-mistakes-checklist)
- [OPR Rules](#opr-rules)
- [OPR Comment Rules](#opr-comment-rules)
- [Compact Chat Output](#compact-chat-output)

## Non-Negotiables

- Research the query before touching results, even when the query looks obvious.
- Use search research to understand intent, not to copy search ranking into grades.
- Grade meaning and satisfaction, not matching words.
- Apply the Interpretation Gate (`../SKILL.md` Section 0.5) before grading: a result for the dominant interpretation is graded normally; a result for a secondary interpretation (a real, less popular meaning, often a different entity with the same name) is Somewhat Satisfying; a result matching no plausible interpretation, or answering a different question on the wrong device, product, app or task, is Not Satisfying.
- Verify landing-page content for web/news results. Snippets can be stale or misleading.
- Do not grade inaccessible, bot-blocked, JavaScript-empty, CAPTCHA-blocked, or very thin pages from title/URL reputation alone. Manual review must follow the PDF: turn off ad blockers, answer CAPTCHAs when possible, close cookie pop-ups, refresh broken pages twice, and note warnings/log-ins/pop-ups.
- If a page cannot be verified and the task content is empty or too thin to judge, do not assign a grade from guesswork. Put "Manual review needed" in the Grade cell until the user provides the visible page content or confirms access.
- If a page cannot be opened but the snippet is sufficient to grade confidently, grade from the snippet and mark it `⚠ Graded from snippet — page not opened, verify manually` in the Grade cell and the Access note.
- Always tell the user when any checker result was not fully accessible. Add a short Access note before the rating table, naming the affected result labels and separating manual-review needs from confirmed Content Unavailable flags.
- Treat user location, language, locale, and query date as rating inputs. Apply the v2.2.2 query-date rules: an implausible date (`1970-01-01`, a future date) means judge freshness against today and grade normally without flagging; a missing date or location that the grade depends on means Content Unavailable.
- Check flags before satisfaction grading.
- For OPR, compare grades first, then ranking, then useful variety.

## Intent Analysis

Identify these before grading:

- Exact query text.
- User location and locale/language.
- Query date, especially for news, recurring events, "new", "best", "current", weather, sports, prices, and schedules. Note whether it is shown, missing, or implausible.
- Search mode, when shown: general web search or on-device search.
- Dominant interpretation shown by research.
- Common alternate interpretations.
- Query type: navigational, informational, transactional, local/maps, app, news, image, answer/knowledge, product, entertainment.
- Whether the query has explicit locale intent, such as "restaurants in Galway". If so, judge results against the requested locale, not the user's physical distance.

## Flag Rules

On TryRating, if any flag applies, set it and grade the result Not Satisfying (Scenario 37). On Tag, set the flag and submit with no grade; Content Unavailable also needs a comment explaining why. The OPR section labels this flag "Cannot be Judged"; it is the same flag.

Content Unavailable:

- Confirmed normal-user inaccessibility: blank page, parked domain, 404, 410, removed content, country unavailable page, or anything else where the content has been removed or is inaccessible after refreshing twice.
- Browser privacy/security warning for the exact result URL, including a `Not Secure` warning or label in the browser address/search bar. If the warning remains after normal refresh/checking, flag Content Unavailable and grade Not Satisfying. Do not fix the task result by substituting a different official-looking URL.
  - The checker reports two different signals here. `security_warning_detected` means it hit a real certificate or TLS failure and is a strong CU signal. `insecure_http` only means the result URL is plain `http://`, so a browser will label it `Not Secure`; open it yourself and confirm that label before flagging CU on that basis alone.
- Log-in/password/subscription wall that blocks useful content for some users after trying to close or bypass it. Exception: for navigational queries such as `go to facebook.com`, if the result is the exact requested website, do not flag CU just because log-in is required; grade the navigational match.
- Banner or pop-up indicating a limit on number of visits, even if the limit has not yet been reached.
- Required result context missing, such as a Maps card with no distance.
- Query context missing (user location or query date) when the grade depends on it, such as Seattle weather for `what is the weather outside` with no user location. If you are confident the missing context would not change the grade, grade normally without flagging.
- News result whose timestamp is more than 3 months newer than the query date.
- Web image group with any missing image.

Inappropriate:

- Pornography, adult advertising/services, sex toys, illegal drugs, hate speech, gambling, spam/phishing, pirated content including fake/free streaming, gore/shock, malicious/deceptive pages, sideloading app sites, content contradicting expert consensus on public-interest topics, or pages with no original/useful content such as scraped or auto-created spam. Medical, educational, fine-art, or journalistic context is not inappropriate just because it mentions sensitive content.

Wrong Language:

- Result is neither English nor the language of the user locale.
- English results are never Wrong Language.
- Use only the PDF exceptions: the query requests that country-specific site, the user is visiting another country and the result is a local business/attraction in that country language with no equivalent result, or the query is foreign-language text that is also a popular song/movie/business/etc. in the current locale.

Manual Review:

- 403, 429, bot-blocking, JavaScript-only output, empty extraction, checker connection failure, or very thin extracted text means do not guess and does not automatically mean CU. If a page shows a CAPTCHA, the PDF says to answer it and proceed; because automation usually cannot do that, ask for manual inspection unless the task result itself is self-contained and sufficient for its type. If the task content is not enough, mark the table row as "Manual review needed", not Somewhat Satisfying or another guessed grade. If normal/manual access confirms the exact result URL does not open after two refreshes, shows a privacy/security warning, shows a `Not Secure` warning/label in the browser address/search bar, shows an unbypassable log-in/password/subscription wall, shows only an error page, redirects to an unrelated homepage/main page with the requested content missing, or has no usable content for a normal user, flag it Content Unavailable and grade Not Satisfying.
- If the checker reports `manual_review_required` or `automation_result: manual_review_needed`, include an Access note in the final answer even when the task content is enough to grade. Example: `Access note: R5 required manual review because the checker could not fully verify the page. Do not mark CU unless manual access also fails.`
- Do not hide access problems just because they do not change the final OPR. The user must be told which results were not fully accessible through the checker.

## Grade Anchors

Highly Satisfying:

- Almost all users would want it.
- Official site or official app for a clear navigational/app query.
- Correct, direct answer visible without extra work (Scenario 20). This includes a web result whose card content clearly shows the direct answer; confirm it on the page, or mark it snippet-graded if the page cannot be opened.
- Wikipedia or another authoritative source for a dominant named entity.
- Authoritative dictionary page for an explicit definition query (e.g., Merriam-Webster, Dictionary.com), treated as an authoritative reference under Scenario 28, so not capped at Satisfying.
- Maps result for a named place, an exact address, or the closest branch of a named chain. Not a type-of-business query: `thai restaurant` → a nearby Thai restaurant is Satisfying (Scenario 19).
- Timely, highly relevant, high-quality news where the query topic is the primary subject.

Highly Satisfying Disqualifiers:

- Blog posts and less authoritative sources, max Satisfying.
- Advice or recommendation queries, max Satisfying.
- Generic product vendor pages, max Satisfying.
- One-step-away results, max Satisfying.
- Secondary (non-dominant) interpretation results, which are Somewhat Satisfying.
- Ambiguous queries without a clear dominant interpretation.
- Movie/TV/book/music cards that primarily offer purchase/streaming, max Satisfying.

Satisfying:

- Many users would want it, but it is less direct, less complete, or requires more effort.
- One-step-away result such as a review page, blog article, stock/news page for a company query, or Wikipedia page that contains the answer but requires clicking/searching.
- Useful app variant or companion app from the same vendor.
- Correct nearby Maps result that is not closest.
- Product page where the item can be purchased for a specific product query.

Somewhat Satisfying:

- Some users may find it useful, but it is not what most searchers wanted.
- Secondary (non-dominant) interpretation: always Somewhat Satisfying, whatever it would otherwise earn.
- Too specific or too general for the query.
- Stale but still valid news.
- Related entity, competing brand, related video/page, or tangential result.
- Correct but only moderately accessible Maps result.
- Shared wording with no plausible interpretation behind it is not enough; wrong-device or wrong-task results are Not Satisfying.

Not Satisfying:

- Flagged result.
- Off-topic, wrong year/event, misleading, or incorrect. A wrong entity that is a real secondary interpretation is Somewhat Satisfying, not Not Satisfying.
- Wrong device/product/app/task even if it shares important query words, such as Mac root-user help for an iPad jailbreak query.
- Too outdated for the query's time need.
- Very distant local/maps result unless explicit locale makes that distance irrelevant.
- Incidentally matches words but misses intent.

## Result-Type Examples

Apps:

- Query `facebook`, result Facebook iOS app: Highly Satisfying.
- Query `candy crush saga`, result another current Candy Crush game from the same vendor: Satisfying.
- Query is an app name, result is that app's Google Play page: Somewhat Satisfying (Scenario 8). v2.2.2 removed the general assumption that every search is on an Apple device, but Scenario 8 still grades Google Play this way.
- Query `dominos`, result Domino's app that supports ordering: Highly Satisfying.
- Query `dell`, result an internal/partner event app not used by normal customers: not Highly Satisfying; usually Somewhat Satisfying or Not Satisfying depending usefulness.

Maps:

- Named place, exact address, or closest branch of a named chain: Highly Satisfying.
- Type of business (`thai restaurant`, `thai food`), nearby: Satisfying (Scenario 19).
- Grade Maps cards on what is visible; if several Maps results appear, grade on the first one only.
- Correct nearby but not closest business: Satisfying.
- Chain or type of business not nearby but still accessible, perhaps up to an hour's drive: Somewhat Satisfying (Scenario 18).
- Correct but not close, still plausible for the item/service: Somewhat Satisfying.
- Correct but too far for the user's need: Not Satisfying.
- Explicit locale query such as `cars in Galway`: judge match to Galway, not distance from user.
- Missing required result context, such as distance on a Maps card, is CU/Not Satisfying.

News:

- Query asks for current news, result is timely, relevant, and from a high-quality local/national source: Highly Satisfying.
- Entity is merely mentioned but not the primary topic: downgrade, often Not Satisfying.
- Stale but accurate story about an older event when current information is expected: Somewhat Satisfying or Not Satisfying depending query.
- News result timestamp more than 3 months newer than the query date is CU.

Knowledge/Answer:

- Correct answer visible and concise: Highly Satisfying (Scenario 20). This includes a web result whose card content clearly shows the direct answer; confirm it on the page, or mark it `⚠ page not opened, verify manually` if the page cannot be opened.
- Authoritative dictionary pages for definition queries: Highly Satisfying. These are the definitive source and do not require hunting for the answer.
- Answer present but only after opening the page, whether a long article or an official help page: Satisfying (Scenario 21: `instagram.com change pass` → Instagram's official instructions).
- Definition of a related word, not the word asked: Somewhat Satisfying (`fleeting meaning`).
- Incorrect answer or answer to a different question/date: Not Satisfying.
- Always verify factual accuracy with research.

Wikipedia:

- Dominant named entity page: Highly Satisfying.
- Contains the answer but requires effort for a direct question: usually Satisfying.
- Secondary interpretation: Somewhat Satisfying.
- Too specific or too broad: Somewhat Satisfying or Not Satisfying based on usefulness (Scenario 36: `dogs` → the Beagle page is Somewhat Satisfying).

Products:

- Specific product query and official/specific product page, even out of stock: do not automatically penalize for being out of stock.
- Generic product query and out-of-stock product page: lower the grade.
- Vendor pages for recommendation/advice-style product queries are max Satisfying.

Web Images:

- All images correct, clear, focused, representative, and non-duplicate: Highly Satisfying.
- All but 1 or 2 images have every property: Satisfying.
- Up to half of the images have every property: Somewhat Satisfying.
- Any image shows the wrong subject: Not Satisfying. Any image missing: Content Unavailable, graded Not Satisfying.

## Common Mistakes Checklist

Check every item before finalizing:

- [ ] Query was researched on multiple sources or provided search links.
- [ ] Dominant interpretation was verified, not assumed.
- [ ] Query location, language, and date were considered.
- [ ] URL checker report was reviewed, and manual browser checks followed the PDF rules for ad blockers, CAPTCHAs, cookies, warnings, log-ins, and two refreshes for broken pages.
- [ ] Extracted content files were searched for query-relevant terms.
- [ ] Any checker/manual-review issue was called out in an Access note before the rating table, with affected result labels named.
- [ ] Manual-review results were not guessed from title, URL, or domain reputation, and any result graded from a sufficient snippet is marked `⚠ page not opened, verify manually`.
- [ ] Rows with insufficient content and unresolved manual review were marked "Manual review needed" rather than given a guessed grade.
- [ ] Checker-only failures were not treated as CU unless normal/manual access confirmed inaccessibility, a privacy/security/Not Secure warning, unbypassable log-in/password/subscription wall, visit-limit pop-up, or missing required result context.
- [ ] Any result confirmed not to open after two refreshes, or confirmed to show a browser privacy/security/Not Secure warning, was marked Content Unavailable and graded Not Satisfying.
- [ ] Snippets were cross-checked against actual landing-page content.
- [ ] Time-sensitive results were checked against query date.
- [ ] Location-sensitive results were checked against user/requested location.
- [ ] Results were judged by meaning, not incidental word overlap.
- [ ] Secondary-interpretation results were graded Somewhat Satisfying, and only results matching no plausible interpretation (or the wrong device, product, app or task) were graded Not Satisfying.
- [ ] Implausible query dates were judged against today, and missing query context was flagged only when the grade depends on it.
- [ ] One-step-away results were demoted appropriately.
- [ ] Too-specific or too-general results were demoted.
- [ ] Answer cards were fact-checked.
- [ ] News results were about the entity/event as the primary topic.
- [ ] Maps distance and explicit locale rules were applied.
- [ ] CU, Inappropriate, and Wrong Language flags were checked using the exact PDF categories, not looser summaries.
- [ ] OPR did not reward a side merely for having more results.
- [ ] OPR comment follows the shared-result check when both sides share meaningful results.

## OPR Rules

Use the OPR scale this way:

- Much Better: all meaningful differences favor one side, or there is a very large early-position gap such as Highly Satisfying vs Not Satisfying at L1/R1.
- Better: multiple meaningful differences favor one side, though the sides may share useful results.
- Slightly Better: only a small difference, later-position difference, or minor ranking/variety improvement.
- About the Same: differences are negligible, balanced, or not confidently meaningful.
- About the Same: also use when both sides miss the core user need and the only advantage is keyword closeness rather than real usefulness.

When one side is empty:

- Do not release the task; an empty side is not a technical error.
- Follow the threshold shown in the UI: prefer the side with results only if it has at least one result graded Somewhat Satisfying or better, or (on the other project type) Satisfying or better.
- Do not choose About the Same when one side is empty and the other has results.
- If the side with results does not meet the visible threshold, prefer the side with no results.

## OPR Comment Rules

Authoritative source: `comment-style.md`. Do not maintain a second copy of the comment rules or examples here.

## Compact Chat Output

Output contract: see `../SKILL.md` (`Phase 4: Chat Output`). Use `Manual review needed` in the Grade cell when a page could not be verified and the snippet is too thin to judge, and `⚠ page not opened, verify manually` beside any grade taken from the snippet.
