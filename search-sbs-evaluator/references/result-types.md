# Search SBS — Result-Type Quick Reference

Use with `../SKILL.md`. The grade anchors, HS disqualifiers, and flag rules live in `SKILL.md`; this file holds the per-result-type detail and the piracy/scraped-content checklist.

## Piracy and Scraped Content (Common Misses)

Piracy and scraped-content flags are frequently overlooked. Always actively check for these. If a result is piracy or scraped spam, flag Inappropriate and grade NS immediately. Do not evaluate it further.

**Piracy red flags by query type:**

- **Gaming queries** (e.g., Minecraft, Roblox): sites offering cracked/pirated game downloads, illegal mod APKs, or unofficial sideloading. Legitimate wikis and guides are NOT piracy.
- **Movie/TV/Music queries**: fake or free streaming sites, torrent indexes, or pages embedding unauthorized full-length content. Official platforms (Netflix, YouTube, Spotify) and licensed clips are NOT piracy.
- **Software/App queries**: crack, keygen, or serial-number sites. Sideloading app sites (e.g., unofficial APK mirrors) are also flagged Inappropriate even when the app itself is free.
- **Book/Academic queries**: sites hosting unauthorized full-text PDFs of copyrighted works. Official publisher or library links are NOT piracy.

**Scraped-content red flags:**

- Page text is a near-verbatim copy of a well-known source (e.g., a wiki, official site, or top-ranking article) with no original commentary, formatting, or added value.
- Site is plastered with low-quality ads, pop-ups, or redirect chains and the "content" is clearly harvested to generate ad revenue.
- Auto-generated or spun text that reads unnaturally or repeats phrases.

## Grading Specific Result Types

### Web/Web Video/News
- Grade the DESTINATION page, not the snippet. For normal redirects, grade the final destination.
- Do not fix an insecure/broken result by substituting a different official-looking URL.
- Navigational query → official site = HS (even if login required).
- "x" is ambiguous — research first, don't assume navigational.
- Autocorrected queries: grade as if user typed the corrected version.

### Apps
- Apple/iOS context is assumed.
- Official app for a well-known app query can be HS.
- Google Play result for an app query is usually SS because the user is on an Apple device.
- Business apps are HS only when regularly used for ordinary customer interaction.

### Maps & Local Intent
- Correct + closest → HS.
- Correct + nearby but not closest → S.
- Correct + accessible but not close → SS.
- Correct but too far, or no distance shown → NS (or CU if no distance).
- For explicit locale queries ("restaurants in Galway"), distance from user is irrelevant — match the requested locale.
- "Permanently closed": Lower by 1 grade only if a similar open business exists nearby.

### Locale & Language Nuances
- **Explicitly/Implicitly Locale-Sensitive:** Wrong locale = NS.
- **Mildly Locale-Sensitive:** (e.g., medical advice from UK for a US user) = Penalize by exactly one grade level.
- **English Results in Non-English Locales:** 
  - Locale where most understand English (e.g., ES-US) = Grade normally. 
  - Locale where many understand English (e.g., Western Europe) = Downgrade one level.
  - Locale where few understand English = NS.
- **Ambiguous Queries (None Dominant):** If a query has multiple reasonable interpretations but NONE are dominant, grade normally for all, EXCEPT any result that would be HS must be downgraded to S.

### News
- **Current Events:** 
  - Timely + relevant + high-quality source, query topic as primary subject → HS.
  - Timely + relevant but from lesser source → S.
  - Stale (>3 months older than search date) but still valid → max SS.
- **Historical Events:** Time sensitivity/staleness does not impact the relevance grade (no penalty).
- Outdated, wrong event, or entity merely mentioned → NS.
- News about a named entity: entity must be the PRIMARY topic, not just mentioned.
- News result timestamp more than 3 months newer than the query date → CU.

### Knowledge/Answer/Info Cards
- Correct direct answer visible without clicking → HS.
- Answer embedded (requires click-through) → S.
- Incorrect or missing answer → NS.
- **Flights:** Must show arrival/departure times, status, and destinations to be useful.
- **Weather:** Location must match the requested location, or user's location if none specified.
- **ALWAYS verify factual accuracy via research.**

### Wikipedia
- Wikipedia for a named entity = HS (Wikipedia is an authoritative source).
- Wikipedia for a non-dominant interpretation = downgrade accordingly.
- Wikipedia page too specific or too general for query = downgrade.
- Contains the answer but requires effort for a direct question = usually S.

### Web Images (Visually Distinctive Entities)
- Applies to anything whose concept/identity can be conveyed visually (e.g., Jacinda Ardern, Taj Mahal, bal-peen hammer).
- All images correct, clear, focused, representative (how they look today, or best known era), non-duplicate → HS.
- All but 1-2 fail → S.
- Up to half pass → SS.
- Any image shows WRONG subject, or images missing → NS / CU.

### Products
- Specific product page (even out of stock) → don't penalize for specific queries.
- Generic product query + out of stock → lower the grade.
- Vendor pages for recommendation/advice-style product queries → max S.
