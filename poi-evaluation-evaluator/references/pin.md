# Pin (§7)

The one dimension whose five labels match Maps exactly. Everything about how you reach
them differs.

| Option | Definition |
|---|---|
| **Perfect** | Drops directly on the POI's rooftop, or on the listed feature where the POI has no rooftop |
| **Approximate** | Drops within the POI's property boundaries but not on the POI |
| **Next Door** | Drops on a property directly adjacent to the intended property |
| **Wrong** | Outside the property boundaries and farther than the property next door |
| **Can't Verify** | Inside the smallest identifiable area for the POI |

## Rate the pin on its own

> **§7.1:** *"Pin ratings should be evaluated individually and should not be influenced
> by address or other data. A pin can be accurately placed even when other rating
> components are rated Wrong."*

A wrong address does not drag the pin down, and a right address does not rescue it.

## The `Perfect` follow-up

`Perfect` triggers *"Does the available evidence indicate the POI's precise location?"*

| Answer | When |
|---|---|
| **Yes** | The best available evidence indicates the precise location |
| **No** | It does not — the parcel has multiple rooftops and it is unclear which one, or the POI shares a rooftop and its exact position under it is unclear |

Answer from the evidence, not from your confidence. Blind testing on the Maps side
showed raters reach for `No` to escape a "which building?" problem and thereby award a
`Perfect` they had not earned. If you cannot identify the rooftop **at all**, `Perfect`
is not available — that is `Can't Verify`.

## `Next Door` has five conditions, all required

Same street · **the adjacent property carries the same street name** · same side of
the street · the first property to either side · same block.

## `Approximate` has three, all required

Same property · same side of the street · same block.

## No `Next Door` inside a shared space (§7.3.2.1)

Two buildings in the same parcel or the same shared parking lot can **never** be
`Next Door` to one another. And there is no `Next Door` outside the parcel either —
**any pin falling outside the Approximate area is `Wrong`.**

## Public roads cut the Approximate area

At Stanford Shopping Center, only the south part of the mall **up to the centreline of
Arboretum Road** is `Approximate` for Nordstrom; the north part is `Wrong`, because a
public road usable to reach places off the parcel acts as a boundary. By contrast, a
strip mall with shared parking and no public or internal access road through it is
`Approximate` across the entire shared parcel, with only the rooftop section over the
business rated `Perfect`.

## Choose the more generous map layer (§7.3.3.1)

Where satellite and standard disagree, **rate on whichever layer is kinder to the
pin** — a pin on the rooftop in satellite and in the car park on the standard map is
rated from satellite. This holds even when the whole city or region is shifted between
layers. Where the standard map is more generous but shows no building contours, use
satellite to locate the buildings, then rate on the standard map.

Use only the standard and satellite views **provided in the Rating Tool** for that
generosity comparison.

## Leaning buildings (§7.3.4.1)

Satellite photography tilts tall buildings, so a pin that appears to land on one
cannot be rated from satellite alone. Establish the building's true footprint from
consensus across standard views, hybrid views, street imagery and reliable map
resources, then rate against the actual location. If no approved source resolves it and
the pin is not objectively wrong → `Can't Verify`, with a comment.

## `Can't Verify` means "inside the smallest identifiable area"

Where the rooftop cannot be identified — cloud cover in satellite, say — do not submit
`Perfect`. Establish the smallest perimeter that could contain the POI from street
imagery and other views. Inside it → `Can't Verify`. Outside it → `Wrong`.

## Feature types with their own sections

Consult the guideline rather than generalising from the bands above:

| Type | Section |
|---|---|
| Single-rooftop POIs | §7.4 |
| Multiple-rooftop POIs; single-complex and dispersed campuses | §7.5 |
| POIs within POIs | §7.6 |
| Natural features; POIs with waiting or access areas | §7.7 |
| Parking lots, parking structures, EV chargers | §7.8 |
| Transit — bus/tram/streetcar stops, multi-platform, single-rooftop, underground stations and entrance polygons | §7.9 |

## Judging a pin without the tool

An agent cannot open the Rating Tool, so the user supplies screenshots — a zoomed
satellite or hybrid frame, and a standard-map frame where the layers might disagree.
Judge those frames yourself rather than asking the user to pre-judge them. Two rules
carry over: **an image has no scale**, so distances come from coordinates via
`../../tools/maps_distance.py`; and `Can't Verify` is for evidence that does not
exist, not for a frame you were not sent — ask for a better frame first.

## Pin corrections

Any rating other than `Perfect` needs corrected coordinates in the comment, in decimal
degrees: `Correct pin: 37.353150, -121.997281`.
