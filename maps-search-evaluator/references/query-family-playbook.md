# Query-Family Playbook

Official Chapter 10 ("How to Rate Results", pages 179–272) and Chapter 11 ("Top Rating Tips", pages 273–276) turned into per-branch decision guidance.

Find the branch that matches the query, then apply its **initial rating** and work demotions from there. Exact labels come from `rating-contract.md`; this file decides *which* label.

## Contents

- [Address queries](#address-queries) — [specific](#specific-address) · [non-specific](#non-specific-partial-address) · [does not exist](#query-address-does-not-exist) · [street / locality / region](#street-locality-region-country)
- [POI queries](#poi-queries) — [prominent POI](#prominent-poi) · [multiple interpretations](#multiple-query-interpretations)
- [Business queries](#business-queries) — [non-chain](#non-chain-business) · [chain](#chain-business) · [general modifier](#chain-with-general-location-modifier) · [specific modifier](#chain-with-specific-location-modifier) · [back office](#back-office-and-no-physical-location) · [does not exist](#businesspoi-does-not-exist)
- [Category queries](#category-queries) — [distance demotion](#category-distance-demotion) · [intent fit](#category-intent-fit) · [prominence](#category-prominence) · [location modifier](#category-with-location-modifier) · [navigational](#navigational-result-for-a-category-query) · [clear vs soft](#clear-vs-soft-categories) · [parking](#parking)
- [Other query types](#other-query-types) — [routing](#routing-queries) · [coordinates and my location](#coordinate-and-my-location-queries)
- [Unclear results](#unclear-results)
- [Top Rating Tips](#top-rating-tips)

## Address queries

### Specific Address

**Cues** — The query is an address that names a locality, so location intent is explicit. Viewport and user location are **irrelevant**.

**Initial rating** — `Navigational` for a result at that exact location.

**Demotions** — Anything not at the queried location is demoted on distance and intent fit.

**Common wrong answer** — Demoting the exact-match result because it sits far from the user or outside the viewport. An explicit locality overrides both.

> `[12112 sugarloaf key st tampa fl 33626]` → the matching address result is `Navigational`, Name `n/a`, Address `Correct`. It is an apartment complex where every building shares the address, so a pin on any one rooftop is `Perfect`.

### Non-Specific / Partial Address

**Cues** — An address with no stated locality. Could refer to many places. Infer intent from viewport and user location.

**Initial rating** — `Navigational` is available when the exact location exists and is very close to the user, or sits inside a fresh viewport — **unless** other addresses satisfying the same intent are equally close, which removes the uniqueness that Navigational needs.

**Demotions** — Demote on distance, and on the **density** of potential results in the area. A farther result that could still satisfy intent goes as high as `Good` (`Distance/Prominence`). Too far → `Bad` (`Distance/Prominence`).

**Common wrong answer** — Awarding `Navigational` to a partial address when several equally close candidates exist.

> `[154 orchard st]` with a fresh viewport over Midtown Manhattan: the 154 Orchard St inside the viewport is eligible for the top rating; same-numbered addresses in other boroughs are demoted by distance.

### Query Address Does Not Exist

**Cues** — Research shows the full queried address has no building and no officially assigned plot.

**The navigational question is always `No`.**

Three result shapes, each with a fixed treatment:

| Result shown | Relevance | Notes |
|---|---|---|
| Closest verified address — same street, same city/state | `Excellent` | — |
| The same non-existent address as queried | `Excellent` | Address → `Incorrect – Address does not exist`; Pin → `Can't Verify` |
| The queried street with no street number | `Acceptable` | Technically satisfies a broad intent |

**Common wrong answer** — Rating the non-existent address `Bad` for relevance. Relevance stays `Excellent`; the fault is recorded under Address Accuracy.

### Street, Locality, Region, Country

**Cues** — The query names a whole street, locality, postal code, region, or country.

**Initial rating** — The matching feature result is the intended answer.

**Demotions** — A **single business or single address on** a queried street is too specific for a broad intent → `Bad` (`User Intent`). Name, address, and pin are still rated as usual.

**Common wrong answer** — Treating a well-known business on the street as a good answer to a street query.

> `[Stevens Creek Blvd]` → `Happy Lamb Hot Pot, 19062 Stevens Creek Blvd` is `Bad` (`User Intent`), while Name `Correct`, Address `Correct`, Pin `Perfect`.

## POI queries

### Prominent POI

**Cues** — A named point of interest, prominent and unambiguous enough that its location *is* the location intent.

**Initial rating** — `Navigational` for the correct location. Viewport and user location are irrelevant — the user wants that place wherever they are.

**Common wrong answer** — Demoting for distance because the POI is far from the user.

> `[mount rushmore]` → `Navigational`, no matter where the user is.

### Multiple Query Interpretations

**Cues** — The query supports several readings, and viewport plus user location do not settle it. **Research the query rather than guessing.**

**Initial rating** — `Navigational` for the dominant interpretation when one is clearly most prominent; secondary interpretations are real results, demoted on intent.

**Common wrong answer** — Rating a secondary interpretation `Bad`. If it genuinely satisfies a lesser reading of the query, it is a demotion, not a failure.

> `[new york]` with user in France → New York City is `Navigational`; New York **State** satisfies a secondary intent and is `Good` (`User Intent`).

## Business queries

### Non-Chain Business

**Cues** — A business with only one location. Treat exactly like a navigational query.

**Initial rating** — `Navigational` for the correct location; every other result is `Bad` (`User Intent`).

> `[klein high school]` → the school is `Navigational`; other results are `Bad`.

### Chain Business

**Cues** — More than one location, from national chains down to small local ones.

**Initial rating** — `Excellent`. A bare chain query is **not** eligible for `Navigational` unless a location modifier pins one unique location.

**Demotions** — Distance, judged against **all real-world chain locations**, not only the results shown. A closer location that was not returned still demotes the ones that were.

**Common wrong answer** — Awarding `Navigational` to the nearest branch of a chain, or judging distance only against the displayed result set.

### Chain With General Location Modifier

**Cues** — Modifier is a locality or area — `[kfc philadelphia]`.

**Initial rating** — `Excellent` for results **inside** the named location, with **no distance demotion** inside it.

**Demotions** — Outside the named location, demote by distance from it and by how many real-world candidates exist inside.

### Chain With Specific Location Modifier

**Cues** — Modifier is a street, full address, or a named POI — `[university of kentucky starbucks]`.

**Initial rating** — `Navigational` becomes available, since the modifier points at one unique location. Results satisfying the location intent are **not** demoted for distance.

**Demotions** — Scale to how far the result sits from the expected area and how sparse the chain is there.

> An Aldi well outside Waco, where Aldi stores are sparse, is demoted **−3** from an initial `Navigational` to `Acceptable` (`Distance/Prominence`).

### Back Office and No Physical Location

**Cues** — Mobile-only businesses (locksmith, dog groomer) and administrative offices not open to the public.

**Initial rating** — `Bad`. They carry little or no maps intent.

**Data ratings** — Address from the official website or a consensus of three sources, else `Can't Verify`. Entire address missing → `Can't Verify`. Pin judged against the address in the result; no address present → Pin `Can't Verify`.

**Exception worth knowing** — When the query is for a POI on a named street, a result for that POI **on** the named street whose official address is on a different street can still be `Excellent`.

### Business/POI Does Not Exist

**Cues** — Research shows the business is closed or never existed.

**Initial rating** — Rate relevance **as if it were open**. Check `Business/POI is closed or does not exist`.

**Field gating** — Name, Address, and Pin questions **do not appear**. Produce no data ratings.

**Common wrong answer** — Demoting to `Bad` because of the closure, or reporting data ratings for a gated result.

> `[sushi]`, user in Sunnyvale → a closed sushi restaurant nearby gets the checkbox and `Excellent`, because if it were open it would be one of the best answers.

Expected vs unexpected `PERMANENT_CLOSURE` is a separate axis — see `result-level-issues.md`.

## Category queries

A category query asks for a group of entities sharing characteristics. There are always many possible results, so **`Navigational` is normally unavailable** — see the exception below.

### Category Distance Demotion

Three configurations, all demoting via `Distance/Prominence`:

| Configuration | Behaviour |
|---|---|
| User **inside** a fresh viewport | User location is the intent. Demote by distance from the user. |
| User **outside** a fresh viewport | Results are expected in or near the viewport, however far the user is. Demote by distance from the viewport. |
| **Fewer possible results** in the area | Tolerance widens. In a sparse or rural area a farther result stays high, because there is nothing closer to prefer. |

**Common wrong answer** — Applying dense-urban distance expectations to a rural query. Density sets the scale.

### Category Intent Fit

Results must actually belong to the category. Demote via `User Intent` when a result only partly fits, independent of any distance demotion.

### Category Prominence

A markedly more prominent member of the category outranks a merely nearer one. Demote a result that is less prominent than the query intent implies via `Distance/Prominence`.

### Category With Location Modifier

**Initial rating** — Every result **inside** the named location gets the highest initial rating of `Excellent`. **Disregard user and viewport location entirely.**

**Demotions** — Outside the location, demote by distance from it and by how many real-world candidates it contains. Further demote on category fit.

Modifiers take many forms — cities, neighbourhoods, streets, and POIs, as in `[aeropuerto barcelona gasolinera]`.

### Navigational Result for a Category Query

Sometimes a query that looks like a category with a modifier resolves to one prominent result, which **can** be `Navigational`. Judge it on the actual wording, the real-world candidates, and local knowledge.

**Even when a Navigational result exists, keep treating the query as a potential category query** and consider the other results relevant rather than dismissing them.

### Clear vs Soft Categories

| | Clear category | Soft category |
|---|---|---|
| Example | `[mall]`, `[italian restaurant]` | `[ski shop]`, mapping to the broader Sporting Goods category |
| Rule | Results must belong to that category; those that do not are `Bad` (`User Intent`) | Several result types can satisfy the intent to differing degrees |
| Approach | Straightforward membership test | Research each result; market customs decide what belongs |

**Common wrong answer** — Applying a strict membership test to a soft category and rating partial fits `Bad` when they deserve a middle rating.

### Parking

"Parking" covers parking lots, garages, and decks. Judge whether the result is the kind of parking the query implies, then apply the normal category distance and prominence demotions.

## Other query types

### Routing Queries

**Cues** — Two distinct locations that are not near each other, separated by a comma or "to" — the user wants directions.

**Initial rating** — **Each of the two endpoint locations is `Excellent`.** Returning either endpoint is the best experience Search can offer.

**Common wrong answer** — Rating one endpoint `Bad` because it is not the "real" destination.

### Coordinate and "My Location" Queries

These are rated **differently from everything else in the guideline**. Applies to coordinates and to `[my location]`, `[current location]`, `[where I am]`, and similar.

Draw a **50 m radius** around the queried coordinates, or around the user location for "my location" queries.

| Dimension | Rule |
|---|---|
| Relevance | Exists and within 50 m → `Excellent`. Does not exist, or outside 50 m → `Bad`. **No Navigational results, ever.** |
| Pin Accuracy | Within 50 m → `Perfect`. Outside → `Wrong`. |
| Name and Address Accuracy | Normal guidelines |

**Common wrong answer** — Answering the navigational question `Yes` for a coordinate query, or applying ordinary pin rules instead of the 50 m test.

## Unclear Results

When the entity cannot be identified with certainty, or does not correspond to the given location and cannot be confirmed closed, use **all** available information — including fields you do not rate, such as URL and phone number. **Never call a business.**

Procedure:

1. Gather every signal — name, URL, phone, category, pin, and surrounding entities.
2. If the evidence shows the business **exists nearby** but the result's data is wrong, record it as a **data-accuracy** fault, not non-existence.
3. If the evidence is **tied**, or you are rating **Search Relevance only**, check `Business/POI is closed or does not exist` and rate relevance as if the entity did exist.

For locating-by-proximity cases, the guideline uses the same 50 m circle as coordinate queries: a result with any part of its Perfect area inside the circle is `Excellent`; one with none is `Bad`.

> A `Caribou Coffee` result carries Caribou's official URL and a phone number matching a real nearby Caribou, but its street address belongs to the Nike store in the same shopping centre. The business exists → no closure checkbox. Relevance `Excellent`, Name `Correct`, Pin `Perfect`, Address `Incorrect – Street Number, Street Name`.

## Top Rating Tips

Official Chapter 11 — the most common rating dilemmas.

**Query is business/POI name + address, result is the address alone.** Relevance `Bad` (`User Intent`) — the user cannot tell whether the result refers to the business they named. Address and pin are rated as usual.
> `[Gary Danko 800 North Point St, San Francisco, California 94109]` → the bare `800 North Point` address result is `Bad`, with Address `Correct` and Pin `Perfect`.

**Query is a street name, result is a single business on that street.** Relevance `Bad` (`User Intent`) — too specific for a broad intent. Name, address, and pin as usual.

**Location intent with a fresh viewport.** User **inside** → the user's location is the intent. User **outside** → results are expected in or near the viewport, no matter how far away the user is.

**Location intent with a stale viewport.** Consider only the user location. When the user location is missing, fall back to the stale viewport.

**A full address result that does not exist.** Relevance stays `Excellent`; record `Incorrect – Address does not exist` and Pin `Can't Verify`. See [Query Address Does Not Exist](#query-address-does-not-exist).
