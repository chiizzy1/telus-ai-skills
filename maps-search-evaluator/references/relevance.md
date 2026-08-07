# Relevance Rating

Relevance measures how well a result satisfies the user's query intent. It is rated **independently of data accuracy** — always assume the result exists and the displayed data is correct.

## Contents

- [Relevance Rating Scale](#relevance-rating-scale)
- [General Rating Rules](#general-rating-rules)
- [Intent Types](#intent-types)
- [Query-Result Connection Types](#query-result-connection-types)
- [Prominence](#prominence)
- [Distance](#distance)
- [Distance by Viewport Position](#distance-by-viewport-position)
- [Special Viewport Rules](#special-viewport-rules)
- [Partial Address Does Not Exist](#partial-address-does-not-exist)
- [City vs. Municipality](#city-vs-municipality)
- [Unexpected Results](#unexpected-results)
- [Transit-Specific Relevance Rules](#transit-specific-relevance-rules)
- [Parking Intent](#parking-intent)
- [Service-Level Mismatch](#service-level-mismatch)
- [PERMANENT_CLOSURE Relevance Rules](#permanent_closure-relevance-rules)
- [Location – User Intent Deviation](#location-user-intent-deviation)

---

## Relevance Rating Scale

| Rating | Definition | Demotion Required? |
|--------|-----------|-------------------|
| **Navigational** | The single most likely result that completely satisfies a distinct user intent. Distinct intent is defined by: extreme prominence (e.g., Eiffel Tower), uniqueness (e.g., a full unique address), or proximity (e.g., incomplete address pointing to an unambiguous, extremely close option). | No |
| **Excellent** | A high-quality result that clearly satisfies user intent. Multiple results can be Excellent. Highest possible initial rating for ambiguous queries or queries ineligible for Navigational. | No |
| **Good** | Only partially satisfies user intent due to relevance, prominence, or distance. | Yes — select User Intent and/or Distance/Prominence checkbox(es). Comment required. |
| **Acceptable** | Technically satisfies user intent but does so poorly due to relevance or distance. | Yes — select checkbox(es). Comment required. |
| **Bad** | Does not satisfy user intent due to lack of relevance or great distance (when closer satisfying results are available). | Yes — select checkbox(es). Comment required. |

One Navigational result does **not** prevent other results from satisfying the query to a lesser degree. It is rare (but possible) to have both a Navigational AND an Excellent result in the same set.

---

## General Rating Rules

1. **Rate each result individually.** Ignore the order of results.
2. **Do not demote duplicates.** Rate each duplicate on its own merits.
3. **Always rate against the real world.** If a better result exists but isn't shown, demote the shown result(s) while considering the missing one(s).
4. **Ignore closed/non-existent results when judging distance/prominence.** Only compare against open, existing results.
5. **Adult content**: Navigational to Bad if the query clearly requests adult content; **Bad** if the query does not imply such intent.
6. **Extremely inappropriate or illegal content**: Rate **Bad**. If the result would be embarrassing to show users, it's inappropriate.

---

## Intent Types

Satisfying user intent is the first step. This determines the **Initial Rating** before distance/prominence adjustments.

| Intent Type | Definition | Highest Initial Rating |
|-------------|-----------|----------------------|
| **Primary Intent** | Result satisfies the most obvious and likely user intent. | Navigational or Excellent |
| **Secondary Intent** | Result is less likely to be user's intent but still satisfies the query. Often less prominent than the primary target. | Good (User Intent) |
| **Unlikely Intent** | Result matches the query but is very unlikely to be what the user wanted. | Acceptable (User Intent) |
| **Non-Relevant Intent** | Issues make the result useless for the user. | Bad (User Intent) |

---

## Query-Result Connection Types

For a result to be relevant at all, there must be a connection between the query and the result.

### 1. General Connection
The result satisfies the most specific part of the query's intent.
- `[marriot]` → "San Francisco Marriott Union Square" → **General connection** (satisfies the brand search near the user).
- `[Houston airport]` → "George Bush Intercontinental" → **General connection** (airport in Houston).
- `[london, brighton]` → "London" → **General connection** (routing query — returning either city is Excellent).

### 2. Abbreviation / Alternate Name Connection
The query uses an abbreviation or former name; the result provides the full/current name.
- `[ewr]` → "Newark Liberty International Airport" → EWR is the airport code.
- `[sears tower]` → "Willis Tower" → Former name of the building.

### 3. Category Connection
The query is a category; the result belongs to that category.
- `[food]` → "La Ciccia" (Italian restaurant) → Category connection.

### 4. Spell Correction Connection
The query is misspelled; the result corrects the error. Applies only when no result for the actual misspelled query exists.
- `[aple store]` → "Apple Store" → Obvious spelling correction.
- `[23 Clair street]` → "23 Clair Boulevard" → No "Clair St" exists near the viewport; "Clair Boulevard" is the most likely intent.

### 5. Transit Intent Connection
The result satisfies the transit intent of the query. Must match the specific transit system if one is named.
- `[bart]` → "Richmond BART Station" → Transit intent satisfied.

### 6. Special Character Connection
Special characters (diacritics, etc.) are considered valid variations per language conventions.
- `[möllersdorf]` → "Moellersdorf" → "oe" is a valid variation of "ö" in German.

### 7. Address-Result Connection
When query and result addresses differ:

| Scenario | Rating |
|----------|--------|
| Same street number, different/missing unit number (not a street extension) | **Good** |
| Full address query, result is street name only | **Acceptable** (unlikely secondary intent) |
| Street query, result is just the locality | **Bad** (does not satisfy intent) |

### 8. Lack of Connection
No logical relationship between query and result, or the connection won't be obvious to the user → **Bad**.

Key examples of lack of connection:
- `[Raging Waters]` → "2333 South White Rd, San Jose" (address without business name) → **Bad** — users can't tell if this is the right place.
- `[valley fair mall]` → "Macy's, 2801 Stevens Creek Blvd" (a store inside the mall) → **Bad** — result is a store, not the mall.
- `[macy's]` → "Westfield Valley Fair" (the mall containing Macy's) → **Bad** — result is a mall, not a store.
- `[costco]` → "Costco Gasoline" → **Bad** — gas station ≠ store, even at the same address.
- `[costco gas]` → "Costco" (the store) → **Bad** — store ≠ gas station.

---

## Prominence

After establishing initial intent, consider prominence. Prominence refers to a feature's popularity (visitors, media references). Prominence varies by locale.

**Prominence hierarchy** (most to least):
1. Known internationally
2. Known nationally
3. Known regionally
4. Known locally
5. May not even be known locally

**Promoting for prominence**: A result that doesn't directly satisfy primary intent can be **promoted to secondary intent (Good)** if it is internationally prominent.
- `[Sydney]` → "Sydney Opera House" → Not primary intent (the city is), but promoted to Good due to international prominence.
- `[Sydney]` → "Sydney Town Hall" → NOT internationally prominent → stays **Bad**.

**When NOT to promote**: Only internationally prominent POIs get promoted. Regional or local prominence is not enough.

---

## Distance

The farther a result is from the area of expected results, the less desirable it becomes. Distance is measured as a **straight line** (not driving distance).

### Distance Factors
- Number of possible results in the real world
- Distribution of all possible results
- Population density (rural, urban, suburban)

### Do NOT Demote for Distance When
- This is the **closest possible result**, even if far away.
- Other closer results are found to be **closed or non-existent**.

### Demote for Distance When
- Other results that satisfy the query and provide the same/similar service are **closer**.

---

## Distance by Viewport Position

### Many Possible Results (e.g., `[starbucks]`)

**User INSIDE fresh viewport:**

| Result Position | Rating | Explanation |
|----------------|--------|-------------|
| Close to user, inside viewport | **Excellent** | Closest relevant results. |
| Farther from user, inside viewport | **Good** (Distance/Prominence) | A bit farther from the closest options. |
| Even farther, still inside viewport | **Acceptable** (Distance/Prominence) | Still inside viewport but far from user. |
| Outside viewport, many closer options exist | **Bad** (Distance/Prominence) | Significantly farther with many closer alternatives. |
| Close to user, outside viewport | **Excellent** | Proximity to user matters more than viewport boundary. |

**User OUTSIDE fresh viewport:**

| Result Position | Rating | Explanation |
|----------------|--------|-------------|
| Inside viewport | **Excellent** | All results inside the viewport receive no distance demotion. |
| Outside viewport, many results inside | **Bad** (Distance/Prominence) | Many closer options inside the viewport. |

### Few Possible Results (e.g., `[zara]` with only a few stores)
Be **more lenient** on distance. Because there are fewer options:

| Result Position | Rating | Explanation |
|----------------|--------|-------------|
| Closest result (even outside viewport) | **Excellent** | Closest available, even if not in viewport. |
| Second/third closest, moderate distance | **Good** (Distance/Prominence) | Fewer options justify leniency. |
| Significantly farther than others | **Acceptable** (Distance/Prominence) | Still relevant given limited options. |

### Rural Areas
Results are often farther away. Apply **greater leniency** on distance. Similar to "few possible results" but with emphasis on distance tolerance.

### Few Results + Greater Distance
When there are very few results nationally (e.g., only 4 streets named "Wartestraße" in all of Germany), each result's relevance remains fairly high even over longer distances.

---

## Special Viewport Rules

### Fresh Viewport, User Inside — Cannot Rate Bad for Distance Alone
Results inside the fresh viewport can be demoted for distance, but **cannot be rated Bad for distance alone**. They can still be rated Bad for other reasons (e.g., no connection to query).

### Fresh Viewport, User Outside — No Distance Demotion Inside Viewport
Results inside the fresh viewport receive **no distance demotion**. Exception: If the viewport is extremely large (e.g., an entire continent), results within it that wouldn't realistically be useful can be demoted.

### Large Viewport Exception
When the viewport is large but there are a limited number of relevant results within it, the results may still be useful and should not be automatically demoted.

---

## Partial Address Does Not Exist

Relevance is rated independently of data accuracy, including addresses that don't exist.
- **Do not demote existing addresses** because closer non-existent addresses are returned.
- Evaluate distance **separately** for existent and non-existent addresses.
- A non-existent address close to the user can still be rated **Excellent** for relevance (because relevance ignores data issues). Its address accuracy would be rated "Address Does Not Exist."

---

## City vs. Municipality

When city and state/county/municipality share a name:
- The **city** is typically more prominent → **Navigational**.
- The state/county/municipality → **Good** (secondary intent).
- If the query specifically requests the county/municipality, that result is **Navigational** and the city is **Bad**.

Examples:
- `[new york]` → "New York City" = **Navigational**, "New York State" = **Good** (Distance/Prominence).
- `[santa clara county]` → "Santa Clara County" = **Navigational**, "Santa Clara" (city) = **Bad** (User Intent).

---

## Unexpected Results

When a straightforward query produces unexpected results:
- Ask: Is there a logical relationship? How likely is the user looking for this?
- Result can satisfy secondary intent due to **prominence** or **transit intent**.
- Promoting for prominence → only for internationally prominent POIs.

Key rules:
- Street query → single business on that street → **Bad** (too specific for a broad query).
- Street query → single address on that street → **Bad** (too specific).
- POI query → transit stop at that POI → **Good/Acceptable** (secondary transit intent).
- City query → famous landmark in that city → **Good** (prominence promotion, if internationally prominent).

---

## Transit-Specific Relevance Rules

### POIs and Transit Intent
Non-transit POIs can be associated with transit POIs sharing the same name. Consider prominence to decide if both can be the intent.
- `[Piccadilly Circus]` → Both the square AND the station are internationally prominent → Both **Excellent**.
- `[Dam Square]` → The square is Navigational; the tram stop (Dam Square Line 2) is **Good/Acceptable** — not prominent.

### Transit Queries
- If a query has clear navigational intent for a specific station, all other station results are **Bad**.
  - `[12th st oakland bart]` → "12th St. Oakland Station" = **Navigational**; "19th St. Oakland Station" = **Bad** (different station, doesn't satisfy specific intent).
- If the query names a locality + transit, results within the locality are Excellent; stations in neighboring localities are **Good** (distance demotion); far-away stations are **Bad**.

### Stops vs. Stations
- **Station** = larger structure with platforms, ticketing, enclosed areas.
- **Stop** = bench, sign, or street marking.
- All stations are stops, but NOT all stops are stations.
- **Station query → stop result** = **Bad** (User Intent).
- **Stop query → station result** = OK (stations satisfy stop intent).
- **Category `[bus stops]`** → rate mainly on distance from user. Large bus hubs should be promoted even if farther; small stops close to user should not be demoted because a larger hub exists farther away.

---

## Parking Intent

- Free and paid parking are equally relevant.
- Parking time limits do not affect relevance.
- Parking for any vehicle type is equally relevant.
- **Public parking** → relevant. Includes limited-use parking (e.g., parking available only when visiting a specific business) and mixed residential/visitor parking (not in a gated community).
- **Private parking** (residents only, staff only, permit only, gated community) → **Bad**.
- If you can't confirm public vs. private → give benefit of the doubt, treat as public.

---

## Service-Level Mismatch

| Scenario | Initial Rating |
|----------|---------------|
| Query asks for specific service level (e.g., `[walmart supercenter]`), result is a lower service level (e.g., Walmart Neighborhood Market) | **Good** (User Intent) — satisfies intent but to a lesser degree. |
| Query asks for generic brand (e.g., `[walmart]`), result is a higher service level (e.g., Walmart Supercenter) | **Excellent** — more service than requested still satisfies intent. |
| Query doesn't specify service type (e.g., `[bank of america]`), result is ATM or branch | **Excellent** — any relevant result is acceptable. |
| Query asks for one specific brand, result is a competitor (e.g., `[burger king]` → McDonald's) | **Bad** — different business entirely, even if similar service. |

---

## PERMANENT_CLOSURE Relevance Rules

See [result-level-issues.md](result-level-issues.md) for the full expected/unexpected decision logic. Summary:

### Expected PERMANENT_CLOSURE
The result is the only/best match for the intent and no open alternatives exist nearby.
- Rate as if the business were open (can be Navigational, Excellent, etc.).
- Check "Business/POI Closed/Does not exist" box.

### Unexpected PERMANENT_CLOSURE
Open alternatives exist nearby.
- **Demote by 2** — highest initial rating is **Acceptable**.
- Check "Business/POI Closed/Does not exist" box.

---

## Location – User Intent Deviation

When user/viewport are in an atypical location (e.g., middle of the ocean) and the query doesn't match:
- Rate with a focus on **high prominence**.
- `[Hong Kong]` with user near Naples, Italy → "Hong Kong" (territory) = **Navigational**; businesses named "Hong Kong" near the user = depends on prominence and distance.
