# Search SBS — Result-Type Quick Reference

Use with `../SKILL.md`. The grade anchors, Highly Satisfying disqualifiers, and flag rules live in `SKILL.md`; this file holds the per-result-type detail and the piracy/scraped-content checklist.

## Piracy and Scraped Content (Common Misses)

Piracy and scraped-content flags are frequently overlooked. Always actively check for these. If a result is piracy or scraped spam, flag Inappropriate and grade Not Satisfying immediately. Do not evaluate it further.

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
- A card with no stated result type is a **Suggested Website**; grade it as a web result.
- Grade the DESTINATION page, not the snippet. For normal redirects, grade the final destination. If the page cannot be opened and the snippet is sufficient, grade from the snippet and mark it `⚠ page not opened, verify manually`.
- Do not fix an insecure/broken result by substituting a different official-looking URL.
- Navigational query → official site = Highly Satisfying (even if login required).
- "x" is ambiguous — research first, don't assume navigational.
- Autocorrected queries: grade as if user typed the corrected version, but only when the typed query is a fragment or misspelling (`iphon`). A real word is graded as typed (`fact` is not an autocorrection of `factual`).

### Apps
- Official app for a well-known app query can be Highly Satisfying.
- Google Play result for an app-name query: Somewhat Satisfying (Scenario 8). v2.2.2 removed the general Apple-device assumption from section 1.4, but this scenario was not changed and still decides it.
- Business apps are Highly Satisfying only when regularly used for ordinary customer interaction.

### Maps & Local Intent
- Named place, exact address, or closest branch of a named chain → Highly Satisfying.
- Type-of-business query (`thai restaurant`), nearby result → Satisfying (Scenario 19). Recommendation queries can never be Highly Satisfying.
- Grade on what is visible in the card. If several Maps results appear, grade on the first one only.
- **Distance has no thresholds in the guideline; it is decided by its worked examples.** Match the live case to the closest one:

  | Query | User → result | Distance | Grade | Why |
  |---|---|---|---|---|
  | `dunkin` | Sunnyvale → San Jose | 6.8 mi, not closest | Satisfying | Nearby branch (Scenario 17) |
  | `starbucks` | San Jose → Fremont | 17 mi | Somewhat Satisfying | Not nearby, still accessible (Scenario 18) |
  | `vietnamese restaurant` | San Jose → San Francisco | 43 mi, dozens closer | Somewhat Satisfying | Accessible, just not what most want |
  | `vietnamese restaurant` | Cupertino → San Francisco (official site) | 50 mi | Somewhat Satisfying | Scenario 25 |
  | `restaurants` | Wilsal, MT (pop. 237) → Bozeman | 39 mi | Satisfying | Rural users travel further |
  | `restaurants` | New York City → Greenwich, CT | 36 mi | Not Satisfying | Dense city, endless closer options |
  | `donuts` | (any) | 30 mi | Not Satisfying | Cheap, common item |
  | `Lexus dealer` | (any) | 30 mi | Satisfying, or Highly Satisfying if closest | Expensive, rare purchase |
  | `nearest subway` | Seattle → | 710 mi | Not Satisfying | No sense showing it |

  Within "perhaps up to an hour's drive," Somewhat Satisfying is the default for a common business; Not Satisfying needs either an extreme distance, a cheap everyday item, or a dense city where the trip is absurd.
- Correct + nearby but not closest → Satisfying.
- Correct + not nearby but still accessible, perhaps up to an hour's drive → Somewhat Satisfying (Scenario 18: `starbucks` from San Jose → Fremont, 17 miles).
- So far that showing it makes no sense (`nearest subway` from Seattle → 710 miles) → Not Satisfying. No distance shown → Content Unavailable, graded Not Satisfying.
- For explicit locale queries ("restaurants in Galway"), distance from user is irrelevant — match the requested locale.
- "Permanently closed": Lower by 1 grade only if a similar open business exists nearby.

### Locale & Language Nuances
- **Explicitly/Implicitly Locale-Sensitive:** Wrong locale = Not Satisfying. This includes the right company for the wrong region: `farmers insurance` from Texas → the Hawaii page. It applies within one interpretation of the query; a different *meaning* of the query is handled by the Interpretation Gate instead (`cao` from Florida → the Irish site is Somewhat Satisfying).
- **Mildly Locale-Sensitive:** (e.g., medical advice from UK for a US user) = Penalize by exactly one grade level.
- **English Results in Non-English Locales:** 
  - Locale where most understand English (e.g., ES-US) = Grade normally. 
  - Locale where many understand English (e.g., Western Europe) = Downgrade one level.
  - Locale where few understand English = Not Satisfying.
- **Ambiguous Queries (Secondary Interpretation):** When one interpretation is dominant, a result relevant to a secondary interpretation is graded Somewhat Satisfying (`michael jordan` → Michael B. Jordan's IMDB page).
- **Ambiguous Queries (None Dominant):** If a query has multiple reasonable interpretations but NONE are dominant, grade normally for all, EXCEPT any result that would be Highly Satisfying must be downgraded to Satisfying.

### News
- **Current Events:** 
  - Timely + relevant + high-quality source, query topic as primary subject → Highly Satisfying.
  - Timely + relevant but from lesser source → Satisfying.
  - Stale (>3 months older than search date) but still valid → max Somewhat Satisfying.
- **Historical Events:** Time sensitivity/staleness does not impact the relevance grade (no penalty).
- Outdated, wrong event, or entity merely mentioned → Not Satisfying.
- News about a named entity: entity must be the PRIMARY topic, not just mentioned.
- News result timestamp more than 3 months newer than the query date → CU.

### Knowledge/Answer/Info Cards
- Correct direct answer visible without clicking → Highly Satisfying (Scenario 20).
- Answer present but only after opening the page, including on an official page → Satisfying (Scenario 21: `instagram.com change pass`, `cambridge library hours`). This is for **a specific fact** with one right answer.
- **Knowledge term or "learn about" query** (`linguistics`, `what causes diabetes`, `utilitarianism`) → Wikipedia, another authoritative reference, or a knowledge card is **Highly Satisfying** (Scenario 23), even though the user opens the page. The page *is* the answer.
- **Dictionary card** that precisely answers a definition need → Highly Satisfying; it must be the correct interpretation of the word.
- **Stocks:** correct symbol and a price shown.
- Answer embedded (requires click-through) → Satisfying.
- Incorrect or missing answer → Not Satisfying.
- Definition of a related word, not the word asked → Somewhat Satisfying (`fleeting meaning`).
- **Flights:** Must show arrival/departure times, status, and destinations to be useful.
- **Weather:** Location must match the requested location, or user's location if none specified.
- **ALWAYS verify factual accuracy via research.**

### Wikipedia
- Wikipedia for a named entity = Highly Satisfying (Wikipedia is an authoritative source).
- Wikipedia for a non-dominant interpretation = downgrade accordingly.
- Wikipedia page too specific or too general for query = downgrade.
- Contains the answer but requires effort for a direct question = usually Satisfying.

### Web Images (Visually Distinctive Entities)
- Applies to anything whose concept/identity can be conveyed visually (e.g., Jacinda Ardern, Taj Mahal, bal-peen hammer).
- All images correct, clear, focused, representative (how they look today, or best known era), non-duplicate → Highly Satisfying.
- All but 1 or 2 images have every property → Satisfying.
- Up to half of the images have every property → Somewhat Satisfying.
- Any image shows the WRONG subject → Not Satisfying. Any image missing → Content Unavailable, graded Not Satisfying.
- Judge "correct subject" against the interpretation the group serves: `pitbull` → pit bull dog pictures is Somewhat Satisfying as a secondary interpretation, because the dominant meaning is the singer.

### Products
- Specific product page (even out of stock) → don't penalize for specific queries.
- Generic product query + out of stock → lower the grade.
- Vendor pages for recommendation/advice-style product queries → max Satisfying.
