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
- Apply the meaning-match gate before giving SS or better: if the result is about the wrong device, product, app, entity, or task, grade it NS even when it shares keywords with the query.
- Verify landing-page content for web/news results. Snippets can be stale or misleading.
- Do not grade inaccessible, bot-blocked, JavaScript-empty, CAPTCHA-blocked, or very thin pages from title/URL reputation alone. Manual review must follow the PDF: turn off ad blockers, answer CAPTCHAs when possible, close cookie pop-ups, refresh broken pages twice, and note warnings/log-ins/pop-ups.
- If a page cannot be verified and the task content is empty or too thin to judge, do not assign HS, S, SS, or NS from guesswork. Put "Manual review needed" in the Grade cell until the user provides the visible page content or confirms access.
- Always tell the user when any checker result was not fully accessible. Add a short Access note before the rating table, naming the affected result labels and separating manual-review needs from confirmed Content Unavailable flags.
- Treat user location, language, locale, and query date as rating inputs.
- Check flags before satisfaction grading.
- For OPR, compare grades first, then ranking, then useful variety.

## Intent Analysis

Identify these before grading:

- Exact query text.
- User location and locale/language.
- Query date, especially for news, recurring events, "new", "best", "current", weather, sports, prices, and schedules.
- Dominant interpretation shown by research.
- Common alternate interpretations.
- Query type: navigational, informational, transactional, local/maps, app, news, image, answer/knowledge, product, entertainment.
- Whether the query has explicit locale intent, such as "restaurants in Galway". If so, judge results against the requested locale, not the user's physical distance.

## Flag Rules

If any flag applies in TryRating-style tasks, grade the result NS.

Content Unavailable:

- Confirmed normal-user inaccessibility: blank page, parked domain, 404, 410, removed content, country unavailable page, or anything else where the content has been removed or is inaccessible after refreshing twice.
- Browser privacy/security warning for the exact result URL, including a `Not Secure` warning or label in the browser address/search bar. If the warning remains after normal refresh/checking, flag Content Unavailable and grade NS. Do not fix the task result by substituting a different official-looking URL.
  - The checker reports two different signals here. `security_warning_detected` means it hit a real certificate or TLS failure and is a strong CU signal. `insecure_http` only means the result URL is plain `http://`, so a browser will label it `Not Secure`; open it yourself and confirm that label before flagging CU on that basis alone.
- Log-in/password/subscription wall that blocks useful content for some users after trying to close or bypass it. Exception: for navigational queries such as `go to facebook.com`, if the result is the exact requested website, do not flag CU just because log-in is required; grade the navigational match.
- Banner or pop-up indicating a limit on number of visits, even if the limit has not yet been reached.
- Required result context missing, such as a Maps card with no distance.
- Web image group with any missing image.

Inappropriate:

- Pornography, adult advertising/services, sex toys, illegal drugs, hate speech, gambling, spam/phishing, pirated content including fake/free streaming, gore/shock, malicious/deceptive pages, sideloading app sites, content contradicting expert consensus on public-interest topics, or pages with no original/useful content such as scraped or auto-created spam. Medical, educational, fine-art, or journalistic context is not inappropriate just because it mentions sensitive content.

Wrong Language:

- Result is neither English nor the language of the user locale.
- English results are never Wrong Language.
- Use only the PDF exceptions: the query requests that country-specific site, the user is visiting another country and the result is a local business/attraction in that country language with no equivalent result, or the query is foreign-language text that is also a popular song/movie/business/etc. in the current locale.

Manual Review:

- 403, 429, bot-blocking, JavaScript-only output, empty extraction, checker connection failure, or very thin extracted text means do not guess and does not automatically mean CU. If a page shows a CAPTCHA, the PDF says to answer it and proceed; because automation usually cannot do that, ask for manual inspection unless the task result itself is self-contained and sufficient for its type. If the task content is not enough, mark the table row as "Manual review needed", not SS or another guessed grade. If normal/manual access confirms the exact result URL does not open after two refreshes, shows a privacy/security warning, shows a `Not Secure` warning/label in the browser address/search bar, shows an unbypassable log-in/password/subscription wall, shows only an error page, redirects to an unrelated homepage/main page with the requested content missing, or has no usable content for a normal user, flag it Content Unavailable and grade NS.
- If the checker reports `manual_review_required` or `automation_result: manual_review_needed`, include an Access note in the final answer even when the task content is enough to grade. Example: `Access note: R5 required manual review because the checker could not fully verify the page. Do not mark CU unless manual access also fails.`
- Do not hide access problems just because they do not change the final OPR. The user must be told which results were not fully accessible through the checker.

## Grade Anchors

Highly Satisfying (HS):

- Almost all users would want it.
- Official site or official app for a clear navigational/app query.
- Correct, direct answer visible without extra work. (This includes standard web results if the snippet text clearly displays the direct answer).
- Wikipedia or another authoritative source for a dominant named entity.
- Authoritative dictionary page for an explicit definition query (e.g., Merriam-Webster, Dictionary.com). These are the definitive source and are NOT capped at S.
- Correct closest Maps result for local intent.
- Timely, highly relevant, high-quality news where the query topic is the primary subject.

HS Disqualifiers:

- Blog posts and less authoritative sources, max S.
- Advice or recommendation queries, max S.
- Generic product vendor pages, max S.
- One-step-away results, max S.
- Non-dominant interpretation results.
- Ambiguous queries without a clear dominant interpretation.
- Movie/TV/book/music cards that primarily offer purchase/streaming, max S.

Satisfying (S):

- Many users would want it, but it is less direct, less complete, or requires more effort.
- One-step-away result such as a review page, blog article, stock/news page for a company query, or Wikipedia page that contains the answer but requires clicking/searching.
- Useful app variant or companion app from the same vendor.
- Correct nearby Maps result that is not closest.
- Product page where the item can be purchased for a specific product query.

Somewhat Satisfying (SS):

- Some users may find it useful, but it is not what most searchers wanted.
- Minor/non-dominant interpretation.
- Too specific or too general for the query.
- Stale but still valid news.
- Related entity, competing brand, related video/page, or tangential result.
- Correct but only moderately accessible Maps result.
- Must still be about the same basic user need. Shared wording alone is not enough for SS; wrong-device or wrong-task results are usually NS.

Not Satisfying (NS):

- Flagged result.
- Off-topic, wrong entity, wrong year/event, misleading, or incorrect.
- Wrong device/product/app/task even if it shares important query words, such as Mac root-user help for an iPad jailbreak query.
- Too outdated for the query's time need.
- Very distant local/maps result unless explicit locale makes that distance irrelevant.
- Incidentally matches words but misses intent.

## Result-Type Examples

Apps:

- Query `facebook`, result Facebook iOS app: HS.
- Query `candy crush saga`, result another current Candy Crush game from the same vendor: S.
- Query for an iOS app, result Google Play page: usually SS because Apple device context is assumed.
- Query `dominos`, result Domino's app that supports ordering: HS.
- Query `dell`, result an internal/partner event app not used by normal customers: not HS; usually SS or NS depending usefulness.

Maps:

- Correct closest business for local intent: HS.
- Correct nearby but not closest business: S.
- Correct but not close, still plausible for the item/service: SS.
- Correct but too far for the user's need: NS.
- Explicit locale query such as `cars in Galway`: judge match to Galway, not distance from user.
- Missing required result context, such as distance on a Maps card, is CU/NS.

News:

- Query asks for current news, result is timely, relevant, and from a high-quality local/national source: HS.
- Entity is merely mentioned but not the primary topic: downgrade, often NS.
- Stale but accurate story about an older event when current information is expected: SS or NS depending query.
- News result timestamp more than 3 months newer than the query date is CU.

Knowledge/Answer:

- Correct answer visible and concise: HS. (This includes standard web results if the snippet text clearly displays the direct answer without requiring a click).
- Authoritative dictionary pages for definition queries: HS. These are the definitive source and do not require hunting for the answer.
- Correct answer embedded in a long article (user must click and hunt for the answer): S.
- Incorrect answer or answer to a different question/date: NS.
- Always verify factual accuracy with research.

Wikipedia:

- Dominant named entity page: HS.
- Contains the answer but requires effort for a direct question: usually S.
- Minor interpretation, too specific, or too broad: SS/NS based on usefulness.

Products:

- Specific product query and official/specific product page, even out of stock: do not automatically penalize for being out of stock.
- Generic product query and out-of-stock product page: lower the grade.
- Vendor pages for recommendation/advice-style product queries are max S.

Web Images:

- All images correct, clear, focused, representative, and non-duplicate: HS.
- One or two weak images but mostly good: S.
- Up to about half useful: SS.
- Wrong subject or missing image: NS/CU.

## Common Mistakes Checklist

Check every item before finalizing:

- [ ] Query was researched on multiple sources or provided search links.
- [ ] Dominant interpretation was verified, not assumed.
- [ ] Query location, language, and date were considered.
- [ ] URL checker report was reviewed, and manual browser checks followed the PDF rules for ad blockers, CAPTCHAs, cookies, warnings, log-ins, and two refreshes for broken pages.
- [ ] Extracted content files were searched for query-relevant terms.
- [ ] Any checker/manual-review issue was called out in an Access note before the rating table, with affected result labels named.
- [ ] Manual-review results were not guessed from title, URL, snippet, or domain reputation.
- [ ] Rows with insufficient content and unresolved manual review were marked "Manual review needed" rather than guessed as HS, S, SS, or NS.
- [ ] Checker-only failures were not treated as CU unless normal/manual access confirmed inaccessibility, a privacy/security/Not Secure warning, unbypassable log-in/password/subscription wall, visit-limit pop-up, or missing required result context.
- [ ] Any result confirmed not to open after two refreshes, or confirmed to show a browser privacy/security/Not Secure warning, was marked Content Unavailable and graded NS.
- [ ] Snippets were cross-checked against actual landing-page content.
- [ ] Time-sensitive results were checked against query date.
- [ ] Location-sensitive results were checked against user/requested location.
- [ ] Results were judged by meaning, not incidental word overlap.
- [ ] Any result with the right words but wrong device, product, app, entity, or task was graded NS.
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

- Much Better: all meaningful differences favor one side, or there is a very large early-position gap such as HS vs NS at L1/R1.
- Better: multiple meaningful differences favor one side, though the sides may share useful results.
- Slightly Better: only a small difference, later-position difference, or minor ranking/variety improvement.
- About the Same: differences are negligible, balanced, or not confidently meaningful.
- About the Same: also use when both sides miss the core user need and the only advantage is keyword closeness rather than real usefulness.

When one side is empty:

- Follow the live task instruction exactly if visible. The PDF says the product may show either an SS+/S+/HS threshold or an S+/HS threshold for preferring the side with results.
- Do not choose About the Same when one side is empty and the other has results.
- Prefer the side with results only when its results meet the visible threshold; otherwise showing no results can be better than showing useless results.

## OPR Comment Rules

Authoritative source: `comment-style.md`. Do not maintain a second copy of the comment rules or examples here.

## Compact Chat Output

Output contract: see `../SKILL.md` (`Phase 4: Chat Output`). Use `Manual review needed` in the Grade cell when a page could not be verified and the snippet is too thin to judge.
