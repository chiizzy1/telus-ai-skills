# User Intent — Query Types, Result Types, and Location Intent

## Contents

- [Query Types](#query-types)
- [Result Types](#result-types)
- [Location Intent — Decision Table](#location-intent-decision-table)
- [Research Expectations](#research-expectations)
- [Rating Interface Quick Reference](#rating-interface-quick-reference)

## Query Types

### Address Queries
Contain all or part of a complete address: street number, street name, locality, state, country, postal code.

| Query | Explanation |
|-------|-------------|
| `[717 E El Camino Real, Sunnyvale, CA 94087]` | Full address with street number, street name, locality, state, postal code. |
| `[Stevens Creek Blvd, Cupertino CA]` | Street-level address query — user wants the location of this street. |
| `[Ireland]` | Country-level address query — user wants the location of the country. |
| `[New York]` | Ambiguous — could be city or state. Use prominence, user location, and viewport to determine intent. |

### Point of Interest (POI) Queries
A POI is any location people find interesting or useful. Businesses are also considered POIs.

| Query | Explanation |
|-------|-------------|
| `[London Bridge]` | Famous POI in London. |
| `[Danube River]` | River in Europe. |
| `[Charing Cross Station]` | Transit station in London. |
| `[Union Square, SF]` | Location in San Francisco. |

### Business Queries
Contain the name of a specific business, sometimes with a location modifier.

| Query | Explanation |
|-------|-------------|
| `[Zola Palo alto]` | Business with location modifier — user wants Zola restaurant in Palo Alto. |
| `[Bookasaurus]` | Business without modifier — use viewport and user location to pinpoint. |
| `[Starbucks, 7 Boulevard Poissonnière, 75002 Paris, France]` | Chain business at a specific address. |
| `[Target sunnyvale]` | Chain business with location modifier. |

### Category Queries
A category refers to a group of entities sharing characteristics.

| Query | Explanation |
|-------|-------------|
| `[fast fod]` | Misspelled category — assume "fast food." |
| `[bus stop]` | Transit category — locations of bus stops. |
| `[coffee shops]` | Business category. |
| `[gym]` | Business category for fitness centers. |
| `[gas San Francisco]` | Category with explicit location modifier. |

### Product and Service Queries
Queries about something purchasable or offered by a business/POI. **Confirm the result actually offers the product/service** in a meaningful way. A steakhouse with one salad on its menu does not meaningfully satisfy `[salads]`, but Sweetgreen (which specializes in salads) does.

| Query | Explanation |
|-------|-------------|
| `[vanilla latte]` | Businesses selling this specific coffee drink. |
| `[deep-tissue massage]` | Businesses offering this massage style. |
| `[school supplies]` | Businesses selling pens, notebooks, etc. |
| `[truck tire repair]` | Businesses offering truck tire repair. |
| `[deep dish pizza detroit]` | Specific product in a specific city. |

### Coordinate and "My Location" Queries
| Query | Explanation |
|-------|-------------|
| `[36.082857, -115.172916]` | User specified a location using lat/long coordinates. |
| `[my location]` | User wants to find out where they are. |

### Emoji Queries
Emojis represent the category they picture. Use the most literal meaning.
- ⛽ = gas stations
- 🍕 = pizza
- ☕ = coffee

### Routing Queries
Contain two locations, implying driving directions. Returning either individual location is expected and should be rated **Excellent**.

| Query | Explanation |
|-------|-------------|
| `[london, brighton]` | Two cities — likely a routing query. Either result is Excellent. |

### Queries with No Maps Intent
Some queries have no maps intent. **Rate ALL results Bad.** Includes:
- Queries that do not refer to a physical location.
- Queries that refer to a location but have an information intent (e.g., `[eureka temperature]`).
- Brands/companies with predominantly online intent (e.g., `[facebook]`, `[Groupon]`).
- Time or weather queries (e.g., `[time in new york city]`).
- Pure information queries (e.g., `[is cucumber a fruit or a vegetable]`).

### Foreign-Language Queries
Do NOT release the survey. Research the query or use an online translation tool, then rate as usual.

---

## Result Types

A query can return one of three result types:

### 1. Business/POI Results
- Shows a **name** in the top field.
- Address and **category** shown below.
- Same rating rules apply to both businesses and POIs.

### 2. Address Results
- Shows the **first line of the address** in the top field (instead of a business name).
- Full address shown below.
- **No category** displayed.
- Important: If a result has no category, do NOT automatically assume it's an address. Research to verify — some POIs don't display a category.

### 3. Features Without an Expected Address
- POIs like bus stops, bridges, mountains may look like address results.
- **Check for a category** — if present, the result is a feature/POI, not an address.
- Example: A result showing "Market St & 4th St" with category "Bus Stop" is a POI, not an intersection.

---

## Location Intent — Decision Table

Location intent determines **where** the user expects to find results. Use this table to decide which location to measure distance from.

### Explicit Location
When the query includes a specific location (e.g., `[kfc Philadelphia]`, `[Boston museums]`, `[bubble tea tully road san jose]`):
- **Ignore** the user location and viewport entirely.
- Use the stated location as location intent.

### "Near me" / "nearby" / "nearest" Queries
When the query includes "near me," "nearby," "nearest," or "food near me":
- Use the **user location** as location intent.
- **Ignore** the viewport, even if fresh.

### "My location" Queries
- Use the **user location** as location intent.
- Result should be placed on the user's location.
- **Ignore** the viewport, even if fresh.

### Implicit Location (no location stated in query)
Use the following decision table:

| Viewport Status | Viewport Age | User Position | Location Intent |
|----------------|-------------|---------------|-----------------|
| Present | **Fresh** | **Inside** viewport | **User location**. Results inside the viewport may be demoted for distance to the user but CANNOT be rated Bad for distance alone. Consider the viewport fresh when viewport age is missing. |
| Present | **Fresh** | **Outside** viewport | **Fresh viewport**. All relevant results inside the viewport receive no distance demotion. If no results can be found in or near the viewport, use user location as secondary intent. |
| Present | **Fresh** | **Missing** | **Viewport** is location intent. |
| Present | **Stale** | **Inside** viewport | **User location** (ignore stale viewport). |
| Present | **Stale** | **Outside** viewport | **User location** (ignore stale viewport). |
| Present | **Stale** | **Missing** | **Stale viewport** is location intent. |
| Missing (viewport age also missing) | — | **Present** | Treat viewport as fresh → same as "Fresh, User Inside" above. |
| Missing entirely | — | **Present** | **User location** sets location intent. |
| Missing entirely | — | **Missing** | **Test locale** becomes location intent, with strong focus on prominent results. |

### Key Rules for Distance Demotion

- **Fresh viewport, user inside**: Results inside the viewport may be demoted for distance to the user, but they **cannot be rated Bad for distance alone**.
- **Fresh viewport, user outside**: Results inside the fresh viewport receive **no distance demotion**.
- **Stale viewport**: Always use user location (unless user is missing, then use stale viewport).
- **Distance is measured as a straight line** — no need to account for driving distance.

---

## Research Expectations

Before rating, research the query and results:
- Use a search engine to investigate and understand the query intent.
- Use **official resources**: businesses' official websites, national postal service websites, government websites.
- Use your own local knowledge.
- Use the information provided in the rating interface (pop-up boxes, coordinates, URLs).

**Pop-up information** (phone numbers, URLs, coordinates shown when clicking a result/pin) is for research only. **Never call a business.** Do not rate the information in the pop-up box — rate only the information shown in the result.

---

## Rating Interface Quick Reference

| Element | Purpose |
|---------|---------|
| **Task Bar** | Shows task type, task ID (use for communication), request ID (internal only), estimated rating time. |
| **Query Header** | Shows the query, viewport age (FRESH in green / STALE in red), locale, country, user lat/lng. |
| **Show User / Show Viewport / Show All** | Navigation shortcuts to pan the map. |
| **User Viewport** | Purple box centered over device icon — shows the map area the user was looking at. Shape varies by device. |
| **Device Icon** | Shows center of user viewport. **Not the user's location.** Not for measuring distance. |
| **User Location** | Blue/white icon — the user's actual location. Click to reveal coordinates. |
| **Result Pin** | Pin with unique number and color matching the result heading. **The tip marks the actual location, not the head.** |
| **Measure Distance** | Ruler icon — drop start (green) and end (red) pins to measure straight-line distance. |
| **Drop Location Pin** | Pin icon — drop a purple pin anywhere to see its address and coordinates. |
| **Draw Tool** | Draw custom polygons on the map. |
