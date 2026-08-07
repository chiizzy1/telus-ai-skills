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
When the **entire campus** is the result → the entire parcel (all buildings, lots, structures) = **Perfect**.

When a **specific building/POI within the campus** is the result → only that building's area is Perfect; rest of campus is Approximate (until you hit a through road boundary).

---

## Features Without Rooftops

### Natural Features (Mountains, Rivers, Parks)
- Pin should fall within the feature's natural boundaries.
- **Perfect** = pin is on/within the feature.
- **Approximate** = pin is on immediately adjacent land/water still associated with the feature.
- **Wrong** = pin is clearly outside the feature.

### Transit POIs

#### Bus Stops
- Pin should be at the stop location (bench, sign, shelter).
- **Perfect** = pin on the stop's physical location.
- **Approximate** = pin on the correct street segment near the stop.
- **Wrong** = pin on wrong street or far from the stop.

#### Underground/Subway Stations
- Station has multiple entrances. The entrance area = the **entrance polygon**.
- **Perfect** = pin on any entrance or on the station structure.
- **Approximate** = pin within the property boundary of the station complex.

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
- Pin should fall on the street.
- **Perfect** = pin on the street.
- **Approximate** = pin near the street but not on it.

### Localities, States, Countries
- Pin should fall within the administrative boundary.
- **Perfect** = pin anywhere within the boundary.

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
