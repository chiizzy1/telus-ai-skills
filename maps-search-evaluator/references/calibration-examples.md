# Calibration Examples

Worked examples for **checking your calibration when a rating is genuinely uncertain**. Read the branch in `query-family-playbook.md` first — it decides which rating applies. Come here to sanity-check a borderline call against a fully worked case.

> **`decided-cases.md` outranks this file.** Where the guideline has already ruled on a shape — lack of connection, the distance ladders — that file quotes the ruling verbatim and is the authority. Use these examples for calibration on shapes it does not cover.

For the complete set of roughly 90 official examples, see `TELUS-TASKS/maps-extracted/text.md` Section 10, "How to Rate Results" (pages 179–272).

Release Survey rules live in `rating-contract.md`, which is the single authority for them.

## Contents

- [Worked Examples by Query Type](#worked-examples-by-query-type) — 15 cases spanning category, navigational, address, POI, transit, parking, routing, viewport, and rural queries
- [Pin Accuracy Examples Summary](#pin-accuracy-examples-summary)
- [Quick Reference: Common Rating Patterns](#quick-reference-common-rating-patterns)

## Worked Examples by Query Type

### Example 1: Category Query — Many Results Available

**Query**: `[starbucks]`
**User**: Inside fresh viewport in San Francisco, CA
**Query Type**: Business (chain)
**Location Intent**: User location (user inside fresh viewport)
**Navigational?**: No — many Starbucks locations exist

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| ① Starbucks, 865 Market St (close to user) | **Excellent** | Close proximity to user inside viewport. |
| ② Starbucks, 170 O'Farrell St (moderate distance) | **Good** (Distance/Prominence) | A bit farther from the closest relevant locations. |
| ③ Starbucks, 264 Kearny St (farther, still in viewport) | **Acceptable** (Distance/Prominence) | Even farther but still inside viewport. |
| ④ Starbucks, 580 California St (outside viewport) | **Bad** (Distance/Prominence) | Many closer locations available; this one is significantly farther and outside viewport. |
| ⑤ Starbucks, 140 Mason St (close to user, outside viewport) | **Excellent** | Close proximity to user — proximity matters more than viewport boundary. |

### Example 2: Navigational Query — Specific Business

**Query**: `[99 bottles santa cruz]`
**User**: Fresh viewport in San Luis Obispo, CA
**Query Type**: Business with location modifier
**Location Intent**: Explicit location (Santa Cruz)
**Navigational?**: Yes — unique business in specific city

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| ① 99 Bottles Of Beer On The Wall, PERMANENT_CLOSURE, Santa Cruz, CA | **Navigational** + "Closed" checkbox | Expected PERMANENT_CLOSURE — only result matching intent. Rate as if open. |
| ② 99 Cents Only Stores, Gilroy, CA | **Bad** (User Intent) | Different business, wrong location. |
| ③ 99 Bottles & Cocktails, Anaheim, CA | **Bad** (User Intent) | Different restaurant, not in Santa Cruz. |

### Example 3: Category Query with Unexpected Closed Result

**Query**: `[vintage store]`
**User**: Fresh viewport in Washington, DC
**Query Type**: Category
**Navigational?**: No — many vintage stores exist

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| ① Meeps Vintage, 2104 18th St NW, Washington, DC | **Excellent** | Matches intent, close to user inside viewport. |
| ② Miss Pixie's, 1626 14th St NW, Washington, DC | **Excellent** | Vintage clothing, among closest results. |
| ③ Buffalo Exchange, PERMANENT_CLOSURE, 1318 14th St NW | **Bad or Acceptable** (User Intent) + "Closed" checkbox | Unexpected PERMANENT_CLOSURE — open options nearby. Demote by 2 (highest = Acceptable). Given abundance, Bad is also defensible. |

### Example 4: Address Query — Full Address

**Query**: `[717 E El Camino Real, Sunnyvale, CA 94087]`
**Query Type**: Address (full)
**Navigational?**: Yes — unique full address

| Result | Relevance | Name Accuracy | Address Accuracy | Pin |
|--------|-----------|--------------|-----------------|-----|
| 717 E El Camino Real, Sunnyvale, CA 94087 | **Navigational** | **n/a** (address result) | **Correct** | Based on rooftop placement |

### Example 5: POI Query — Famous Landmark

**Query**: `[Sydney]`
**User**: Test locale en_AU
**Navigational?**: Yes — the city of Sydney

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| Sydney, Australia | **Navigational** | Primary intent — the city. |
| Sydney Opera House, Sydney, NSW | **Good** (User Intent) | Not primary intent, but promoted to secondary due to international prominence. |
| Sydney Town Hall, 483 George St, Sydney | **Bad** (User Intent) | Not internationally prominent — no promotion. |
| Sydney Buses Depot, 34-36 King St, Randwick | **Bad** (User Intent) | Unlikely intent, very low prominence. |

### Example 6: Transit Query — Specific Station

**Query**: `[12th st oakland bart]`
**User**: Fresh viewport in California
**Navigational?**: Yes — specific named BART station

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| 12th St. Oakland Station, Oakland, CA | **Navigational** | Exact match for the specific station. |
| 19th St. Oakland Station, Oakland, CA | **Bad** (User Intent) | Different BART station — doesn't satisfy the specific query intent. |

### Example 7: Service-Level Mismatch

**Query**: `[walmart supercenter]`

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| Walmart Supercenter, 3435 E Broadway Blvd, Tucson | **Excellent** | Exact service level match. |
| Walmart Neighborhood Market, 5500 E 22nd St, Tucson | **Good** (User Intent) | Lower service level than requested — satisfies intent but to a lesser degree. |

**Query**: `[walmart]` (generic)

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| Walmart Supercenter | **Excellent** | Any Walmart is fine; more service = still satisfies. |
| Walmart Neighborhood Market | **Excellent** | Any Walmart is fine when no service level specified. |

### Example 8: Few Results + Greater Distance

**Query**: `[Wartestraße]`
**User**: Near Berlin, Germany
**Context**: Only 4 streets in Germany with this name

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| ① Wartestraße, Gransee (closest) | **Excellent** | Closest to user/viewport. |
| ② Wartestraße, Siegen | **Good** (Distance/Prominence) | Far from user but second closest of only 4 results. |
| ③ Wartestraße, Wiesbaden | **Good** (Distance/Prominence) | Similar distance to Siegen, same rating. |
| ④ Wartestraße, Geislingen | **Acceptable** (Distance/Prominence) | Fourth closest, significantly farther — but only 4 exist in the country. |

### Example 9: Name & Category Accuracy

| Result Name | Official Name | Name Rating | Reason |
|-------------|--------------|-------------|--------|
| McDonald's | McDonald's | ✅ Correct | Exact match. |
| Macys | Macy's | ⚠️ Partially Correct | Missing apostrophe. |
| Seven Eleven | 7-Eleven | ⚠️ Partially Correct | Unexpected form. |
| Taco Bull | Taco Bell | ❌ Incorrect | Meaning change — ambiguous. |
| IEA | IKEA | ❌ Incorrect | Short names are very sensitive to errors. |
| Mickey D's | McDonald's | ❌ Incorrect | Slang, not official. |

### Example 10: Address Accuracy — Component Issues

| Result Address | Official Address | Rating | Issue |
|---------------|-----------------|--------|-------|
| 836 E Fremont Ave, Sunnyvale, CA | 834 E Fremont Ave, Sunnyvale, CA | Incorrect — Street Number | Wrong street number. |
| Museumplein 6, 1071 DJ Amsterdam | Museumplein 6, 1071 DJ Amsterdam | ✅ Correct | All components match. |
| Museumplein 6, 1071 DJ Utrecht | Museumplein 6, 1071 DJ Amsterdam | Incorrect — Locality | Wrong city (Utrecht instead of Amsterdam). |
| Museumplein 6, 1071 DM Amsterdam | Museumplein 6, 1071 DJ Amsterdam | Incorrect — Postal Code | "DM" instead of "DJ". |
| 118 El Camino Real, Sunnyvale, CA | 118 E El Camino Real, Sunnyvale, CA | Incorrect — Street Name | Missing direction "E". |

### Example 11: Parking Intent

**Query**: `[parking]`

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| Public garage close to user | **Excellent** | Public parking, close. |
| Free street parking close to user | **Excellent** | Free and paid are equally relevant. |
| Long-term parking lot moderate distance | **Good/Acceptable** (Distance) | Time limits don't affect relevance — demote only for distance. |
| Residents-only gated parking | **Bad** | Private parking — cannot be used by general public. |
| Can't confirm if public or private | Rate as if public | Benefit of the doubt. |

### Example 12: No Maps Intent

**Query**: `[eureka temperature]`
**Maps Intent**: No — information query
**Action**: Rate ALL results **Bad**.

### Example 13: Routing Query

**Query**: `[london, brighton]`
**Query Type**: Routing
**Action**: Returning either "London" or "Brighton" individually → **Excellent**.

### Example 14: User Outside Fresh Viewport — Many Results

**Query**: `[starbucks]`
**User**: In Alameda (outside viewport), Fresh viewport in San Francisco

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| Any Starbucks inside the viewport | **Excellent** | User is outside viewport — all results inside viewport get no distance demotion. |
| Starbucks outside viewport (many inside) | **Bad** (Distance/Prominence) | Many results inside viewport make outside results irrelevant. |

### Example 15: Rural Area — Few Results

**Query**: `[american legion]`
**User**: Bismarck, ND (rural)

| Result | Relevance | Explanation |
|--------|-----------|-------------|
| ① American Legion (closest, in Bismarck) | **Excellent** | Closest result. |
| ② American Legion (significantly further north) | **Good** | Second closest in a rural area — greater leniency. |
| ③ American Legion (quite remote) | **Acceptable** | Still a viable option given only 2 closer results. |
| ④ American Legion (similar distance to ③) | **Acceptable** | Similar distance, similar leniency in rural context. |

---

## Pin Accuracy Examples Summary

| Scenario | Perfect | Approximate | Next Door | Wrong |
|----------|---------|-------------|-----------|-------|
| **Single residential home** | On rooftop | On property (yard, driveway) | Immediate neighbor (same street, same side, same block) | Everything else |
| **Store in strip mall (with evidence)** | On the confirmed section of shared rooftop | Rest of shared rooftop + shared parking | N/A (no Next Door in shared spaces) | Outside the shared parcel |
| **Store in strip mall (no evidence)** | Entire shared rooftop | Shared parking lot | N/A | Outside the shared parcel |
| **Campus (university, hospital, zoo)** | Entire campus parcel (all buildings) | N/A | N/A | Outside campus boundaries |
| **Gas station** | On any structure (building, canopy) | On property | Next-door property | Everything else |
| **Natural feature (mountain, river)** | Within feature boundaries | N/A | Adjacent property | Outside boundaries |
| **Transit stop (bus stop)** | At the stop location | On correct street segment | Adjacent stop/property | Wrong street or far away |
| **Missing pin or pin at 0,0** | — | — | — | Always **Wrong** |
| **Leaning building** | On actual location (research-confirmed) | On property | Next door | Everything else |

---

## Quick Reference: Common Rating Patterns

| Scenario | Relevance | Key Rule |
|----------|-----------|----------|
| Query = specific business name → result = that business nearby | Excellent to Navigational | Depends on uniqueness |
| Query = specific business → result = competitor | Bad (User Intent) | Different business entirely |
| Query = category → result = matching business nearby | Excellent | Satisfies category intent |
| Query = city name → result = famous landmark in that city | Good (User Intent) | Secondary intent via international prominence |
| Query = city name → result = random business in that city | Bad (User Intent) | Too specific for broad query |
| Query = street → result = specific address on that street | Bad (User Intent) | Too specific for street-level query |
| Query = address → result = business at that address | Navigational | Business name adds correct info |
| Query = business + address → result = address only (no business name) | Bad (User Intent) | Users can't tell if it's the right place |
| Result inside fresh viewport, user outside | No distance demotion | User outside = viewport-based rating |
| Result inside fresh viewport, user inside | Can demote for distance | But cannot rate Bad for distance alone |
