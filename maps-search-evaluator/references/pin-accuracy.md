# Pin Accuracy

Pin accuracy rates how correctly a result's pin is placed on the map. The pin should reflect the result's physical location. Pin ratings are evaluated **independently** — a pin can be Perfect even when other components are Incorrect.

## Contents

- [Rating Scale](#rating-scale)
- [Boundaries of the Feature](#boundaries-of-the-feature)
- [Single Rooftop Results](#single-rooftop-results)
- [Multiple Street Numbers Under One Rooftop](#multiple-street-numbers-under-one-rooftop)
- [Shared Spaces (Strip Malls, Shopping Centers, Shared Parking)](#shared-spaces-strip-malls-shopping-centers-shared-parking)
- [Features Without Rooftops](#features-without-rooftops)
- [Map View Layers](#map-view-layers)
- [Pin Display Issues](#pin-display-issues)
- [Research Resources for Pin Accuracy](#research-resources-for-pin-accuracy)
- [Judging a pin from a screenshot](#judging-a-pin-from-a-screenshot)

---

## Rating Scale

| Rating | Definition |
|--------|-----------|
| **Perfect** | Pin drops directly on the **rooftop** of the result (for buildings) or on the **listed feature** (for features without rooftops). |
| **Approximate** | Pin drops within the **property boundaries** of the result but NOT on the rooftop. Same property, same side of street, same block. |
| **Next Door** | Pin drops on the **immediately adjacent property**. Must be: same street, same side, same block, first property to any side. |
| **Wrong** | Pin falls outside the property boundaries and next-door properties. Also: missing pins, pins at coordinates 0,0 (Atlantic Ocean off East Africa). |
| **Can't Verify** | Specific rooftop or boundary cannot be identified. Pin is within the smallest identifiable potentially correct area. Pin outside that area → Wrong. Also used when address is rated "Address Does Not Exist." |

### Perfect — Follow-Up Question
If you rate **Perfect**, you may be asked: *"Does the available evidence indicate the result's precise location?"*
- **Yes** → Strong evidence (street imagery, official maps) confirms the exact spot.
- **No** → The rooftop is identified but the result's specific position under a shared rooftop cannot be pinpointed. The entire rooftop is still Perfect.

### Which rooftop vs. where under it — do not confuse these

§9.2.2 escalates in three steps. The middle step is `Perfect` + `No`; the last is **not** Perfect at all:

| What the evidence establishes | Rating |
|---|---|
| The result's specific spot under a shared rooftop | `Perfect`, follow-up `Yes` |
| The correct rooftop, but not the position under it | `Perfect`, follow-up `No` |
| Neither — several rooftops share the address, nothing says which one the result occupies | **`Can't Verify`** |

**Do not answer `No` to escape a "which building?" problem.** The follow-up `No` is for uncertainty *within* one identified rooftop. Uncertainty about *which* rooftop is `Can't Verify`.

**Exception — address-type results.** When the result *is* the shared address (an apartment complex queried as `12112 Sugarloaf Key St`, where every building genuinely carries that address, §10.1), there is no "which building" question to answer, so a pin on any of those rooftops is `Perfect`. This exception does **not** extend to a business or POI that occupies one building among several sharing an address — that is the `Can't Verify` row above.

### Judging a pin from a screenshot

An agent cannot open the rating tool, so the user supplies a zoomed screenshot per result. That image **is** the tool's map layer — the surface §9.2.1 requires the pin to be reconciled against. Judge it directly rather than asking the user to pre-judge it.

Read the frame in this order:

1. **Find the pin tip.** The head is only an indicator. A tall pin head can sit over a neighbouring roof while the tip is on the correct one.
2. **Identify the result's building**, using the address, the street layout, and any labels in frame.
3. **Trace the property boundary.** Fences, walls, hedges, water, and kerb lines are boundaries; a parcel includes half the road where a road is present. With no visible divider, drop an imaginary 90° line to the road or apply the Half 'n Half rule.
4. **Place the tip** against that boundary: on the rooftop → `Perfect`; inside the boundary but off the rooftop, same side of the street and same block → `Approximate`; on the first property to either side, same street name and side and block → `Next Door`; beyond the result's property and its neighbours → `Wrong`.

What a frame must contain to be usable:

| Requirement | Why |
|---|---|
| Satellite or hybrid layer | The vector layer renders no rooftops, so nothing above can be judged |
| The result's building **and** its neighbours on both sides | `Next Door` and `Wrong` are relative judgements — a cropped frame cannot distinguish them |
| Visible pin tip | The rating is about the tip |
| Scale bar, only if the frame supports a distance claim | Distance otherwise comes from coordinates |

Hard limits, and what to do about them:

- **No scale in an image.** Never infer distance from apparent pixel gaps. Use `../../tools/maps_distance.py` on the coordinates.
- **One fixed frame.** You cannot zoom, pan, or change layer. If the frame is ambiguous, wrongly zoomed, or vector-only, **ask for another**. Do not guess, and do not retreat to `Can't Verify` when a better frame would settle it — `Can't Verify` is for evidence that does not exist, not for evidence you were not sent.
- **Say what you did.** The evidence line reads "pin judged from the supplied screenshot", never anything implying the live map was explored.

If the user corrects what is in the frame — that is a car park not a rooftop, those are two buildings not one — accept it at once; they can zoom and switch layers and you cannot. If they dispute the **rating**, re-check it against the rules above and change it only if the guideline supports the change.

---

## Boundaries of the Feature

To rate pins, you must understand where a feature begins and ends.

### Property Boundaries
Boundaries can be:
- Fences, walls, garden plants/bushes
- Bodies of water (lakes, rivers, oceans)
- Other dividers
- Property boundaries confirmed by official sources
- If no divider exists → draw an imaginary 90-degree line to the road

### Parking lots are never split

**Always treat a parking lot or parking structure as belonging entirely to the feature.**
Do **not** apply the Half 'n Half rule to it, even when the lot is shared and plainly does
not belong to the feature alone. The shared lot is the feature's `Approximate` area, and it
extends to the public road.

Where a structure can be verified as parking from satellite imagery — parked cars or
parking-lot striping — treat the **whole structure** as a parking lot, on the assumption
that it holds no businesses other than parking-related ones.

Half 'n Half still applies to the **street** and to qualifying **internal access roads**.

### Half 'n Half Rule
Extend the feature's boundaries to the **middle of the road**. This defines the outer limits of the Approximate area.

Also applies between buildings: divide the space between two buildings in half to create a boundary.

### Tennis Rule (for close calls)
- If the **tip** of the pin is still **touching** the boundary line → pin is **inside**.
- If the **tip** points **outside** → pin is **outside**.

---

## Single Rooftop Results

Standard buildings (homes, standalone businesses):

| Pin Position | Rating |
|-------------|--------|
| On the rooftop of the intended property | **Perfect** |
| Within the property boundaries but not on rooftop | **Approximate** |
| On the immediate next-door property (same street, same side, same block) | **Next Door** |
| Outside property boundaries and next-door | **Wrong** |

### Residential property with more than one building

Where a home shares its parcel with a garage, shed or other outbuilding, the buildings are
**not** equal:

| Pin Position | Rating |
|---|---|
| On the rooftop of **the house** (any of them, if several houses share the parcel) | **Perfect** |
| Within the parcel, **including on a support or auxiliary building** — a detached garage, a shed | **Approximate** |
| The next-door property | **Next Door** |
| Outside the parcel and outside next door | **Wrong** |

The trap: a garage has a rooftop, so "pin is on a rooftop" reads as Perfect. It is
**Approximate**. Only the dwelling's rooftop is Perfect.

---

## Multiple Street Numbers Under One Rooftop

When a rooftop covers multiple addresses (e.g., townhouses, row buildings):

### WITH street imagery/strong evidence
- Entrances for each number can be identified → draw imaginary lines to delimit the correct section → pin on that section = **Perfect** (answer "Yes" to precise location question).
- Pin on the wrong section of the same rooftop = **Next Door** (if immediately adjacent) or **Wrong** (if farther).

### WITHOUT street imagery/strong evidence
- Only the address range under the rooftop is known but specific locations can't be determined → pin anywhere on the entire rooftop = **Perfect** (answer "No" to precise location question).
- Pin on property boundaries = **Approximate**.
- Adjacent buildings = **Next Door**.

---

## Shared Spaces (Strip Malls, Shopping Centers, Shared Parking)

### Key Rule: No Next Door in Shared Spaces
A feature **cannot be Next Door** to another feature within the **same property boundaries**. Two buildings in the same shared parking lot or parcel can NEVER be rated Next Door to each other.

No Next Door ratings are made outside the parcel/shared space either. Any pin falling outside the Approximate area in a shared space → **Wrong**.

### WITH street imagery/strong evidence
- Exact location confirmed → draw imaginary lines on the rooftop for **Perfect** area. Answer "Yes" to precise location.
- Rest of the connected rooftop + shared parking lot = **Approximate**.
- Outside the parcel = **Wrong** (no Next Door).

### WITHOUT street imagery/strong evidence
- Only the full rooftop is identifiable → entire rooftop = **Perfect**. Answer "No" to precise location.
- Shared parking lot = **Approximate**.
- Outside the parcel = **Wrong** (no Next Door).

### Shared Spaces with Through Roads
If the shared parcel has public roads running through it:
- Apply Half 'n Half rule to through roads.
- The through road acts as a boundary — the result's Approximate area stops at half the through road.
- Features on the other side of the through road = **Wrong**.

**Through roads** are part of the public road network that can be used to go places other than the specific parcel.

Internal access roads within the parcel can only be used as boundaries if ALL THREE conditions are met:
1. They continue all the way through the parcel
2. They have exit and entrance to public roads at both ends
3. They are continuously and clearly separated from parking by curbs, barriers, road markings

If any condition is not met → the internal road is NOT a boundary.

### Campus Results (University, Hospital Complex)

**When the campus itself is the result, there is no `Approximate` and no `Next Door`** —
Perfect or Wrong only. Perfect is the entire campus or business-complex boundary as
established by research: every building, lot and structure inside it. Wrong is anything
outside that boundary.

When a **specific building/POI within the campus** is the result → only that building's area is Perfect; rest of campus is Approximate (until you hit a through road boundary).

---

## Features Without Rooftops

> ### Which bands exist for which feature type
>
> The guideline switches `Approximate` and `Next Door` **off** for several feature types.
> Awarding a band that does not exist is a rating error, and it is the commonest mistake in
> this chapter. Check here before rating anything that is not an ordinary building.
>
> | Feature type | Perfect | Approximate | Next Door |
> |---|---|---|---|
> | Single rooftop / ordinary building | yes | yes | yes |
> | Residential property, multiple buildings | yes | yes | yes |
> | **Street** | yes | **N/A** | **N/A** |
> | **Administrative division** (neighbourhood, locality, state, country) | yes | **N/A** | **N/A** |
> | **Campus / business complex, when the campus IS the result** | yes | **N/A** | **N/A** |
> | **Natural feature** | yes | sometimes — see below | **N/A** |
> | **Transit POI** | yes | yes | **N/A** |
> | Shared space (strip mall, shopping centre) | yes | yes | **N/A** |

### Natural Features (Mountains, Rivers, Parks)

Turns on the feature's **defining feature** — the water for a river or ocean, the cliffs or
peak for a mountain, the sand for a beach. Features bounded arbitrarily instead (parks,
national forests) use their polygon, or where the polygon would be if the data existed.

| Rating | When |
|---|---|
| **Perfect** | On the defining feature, or inside the polygon for an arbitrarily bounded feature. Answers **Yes** to the precise-location follow-up |
| **Approximate** | Outside the defining feature but **still on the feature** — the slope of a mountain rather than its peak, the shore of a river or lake rather than the water |
| **Next Door** | **N/A** |
| **Wrong** | Anything meeting neither |

Two qualifiers: **not every natural feature has an Approximate area** — judge each one
individually — and where the feature sits in an urban or suburban area you may apply the
Half 'n Half rule.

Note the difference from the old reading: Approximate is land **still part of the feature**,
not adjacent land outside it.

### Transit POIs

Transit is the one feature type with an explicit **50-metre** threshold. There is **no
Next Door** for any transit POI.

| Rating | When |
|---|---|
| **Perfect** | On the transit POI's polygon, on the spot where a user would **wait** for transit, or inside the **entrance polygon** of an underground station. Answers **Yes** to the follow-up |
| **Approximate** | Within **50 m** of the waiting spot, or within station **parking lots and surrounding property** as far as Half 'n Half allows |
| **Next Door** | **N/A** |
| **Wrong** | Farther than **50 m** from the ideal location · within 50 m but **on a non-associated rooftop** · outside the Half 'n Half boundary |

The middle Wrong case is the one that catches people: being close enough is not sufficient
if the pin lands on a building that has nothing to do with the stop.

#### Bus, Tram and Streetcar Stops
Usually at the roadside with a single boarding spot. **Perfect** = the waiting spot itself.
**Approximate** = within 50 m of it and inside Half 'n Half.

#### Underground/Subway Stations
Multiple entrances, each with an **entrance polygon**. **Perfect** = any entrance polygon or
the station structure.

#### Airports, Ferry Ports, Large Transit Hubs
- These are large facilities with clear boundaries.
- **Perfect** = pin within the terminal/facility area.
- **Approximate** = pin on airport/port property but not on the terminal.

### Parking Lots and Structures
- For parking lots: the lot itself is the feature boundary.
- **Perfect** = pin on the lot.
- For parking structures: the building is the rooftop.
- **Perfect** = pin on the structure's rooftop.

### Streets

**There is no `Approximate` and no `Next Door` for a street result.** The scale is Perfect
or Wrong. A pin *near* the street but not on it is **Wrong**, not Approximate.

| Rating | When |
|---|---|
| **Perfect** | Anywhere on the street — including **medians**, **physical road dividers**, **bridges that are part of the street**, and **intersections the street passes completely through** |
| **Approximate** | **N/A** |
| **Next Door** | **N/A** |
| **Wrong** | Everything else — including **sidewalks** and **intersections the street does not pass through** |

Three details that decide real cases:

- **Sidewalks are not part of the street.** A pin on the pavement is Wrong.
- **Intersections only count where the street passes completely through.** For Jersey St in
  NYC, the Lafayette St intersection is Perfect because Jersey passes through it; the
  Mulberry St and Crosby St intersections are **Wrong**, because Jersey does not.
- **A divider still counts even in water.** A pin on the physical divider of a bridge —
  Highway 92 on the San Mateo–Hayward Bridge — is Perfect even though it falls over water.

If the satellite view and the vector map disagree on where the street edge is, **use the
most favourable layer**. A `Perfect` street pin answers **Yes** to the precise-location
follow-up.

### Administrative Divisions (neighbourhood, locality, state, country)

**No `Approximate`, no `Next Door`.** Perfect or Wrong only.

- **Perfect** = anywhere inside the division's boundary or polygon. Answers **Yes** to the
  precise-location follow-up.
- **Wrong** = anywhere outside it.

---

## Map View Layers

When there is a **difference** between satellite imagery and vector map pin placement:
- **Always use the layer that is more generous toward the pin.**
- If pin is on rooftop in satellite but in parking lot on vector → use satellite (rooftop = better rating).
- Even for major shifts between layers across an entire city/region, rate by the most generous layer.
- When vector map has no building contours, use satellite as reference to locate buildings, then rate on the vector map.

---

## Pin Display Issues

### Leaning Buildings
Satellite photos can show buildings appearing to lean. The rooftop appears displaced from the building's actual base.
- **Do NOT trust satellite alone** for leaning buildings.
- Research the building's true location using: vector views, hybrid views, street imagery, reliable online map resources.
- Rate based on the building's **actual location** as confirmed by research.
- If no reliable resources available and pin is not objectively wrong → **Can't Verify** (leave a comment).

### Missing Pins
- If a pin does not appear on the map → **Wrong**.
- If pins are missing **5 or more times in a row** → release the task for technical reasons.

### Pin at 0,0 Coordinates
- If pin falls on latitude 0, longitude 0 (in the Atlantic Ocean off East Africa) → **Wrong**.
- Include explanation in comments.

---

## Research Resources for Pin Accuracy

Rate pin placement using consensus from **multiple reliable online resources**, including both aerial and street-level views whenever possible:

1. **Reliable online map resources** — including vector and hybrid views
2. **Street imagery** — also from claimed social media, crowdsourced review sites, primary publications
3. **Official venue maps and directories** — may contain info not in street imagery
4. **Government business and property registries**
5. **Official government maps** — land registry/cadaster, GIS maps

**Critical**: After researching elsewhere, always verify pin placement using the TryRating tool's own layers. Rate based on what you see in TryRating.

Leave comments with coordinates and resource links if pin rating was difficult to determine or couldn't be verified.
