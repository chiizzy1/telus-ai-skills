# Validity — Eligibility and State

Two questions, asked first, and each can shut down the rest of the task.

## Eligibility (§3.1)

The question is what *kind* of thing this is, not whether its data is right. Research
the business type and confirm it has a history of operating at the listed location.

| Option | The distinguishing test |
|---|---|
| **Conventional POI** | Fixed location, regular schedule |
| **Seasonal** | Permanent location, regular *seasonal* schedule — ski resorts, pumpkin patches, haunted houses, outdoor pools, summer camps |
| **Home Based** | Operates from a residence **and has visible street-facing signage**. No signage → `Not a POI` |
| **Service Area** | Travels to the customer's home by appointment — plumbers, locksmiths, contractors, landscapers |
| **Mobile** | No consistent location; moves to find customers — food trucks, ice cream trucks, pet grooming vans |
| **Not a POI** | Fails the criteria entirely (below) |
| **Can't Verify** | Cannot be verified from insufficient, outdated or unreliable information |

### The three judgement calls that actually decide this

1. **Home Based turns on the structure, not the trade.** A photography studio in a
   commercial space is `Conventional`. The same studio in a house is `Home Based` —
   and only if the residence carries street-facing signage. Use street imagery to
   confirm the structure type.
2. **Service Area turns on whether the POI travels.** A caterer with a commercial
   pick-up counter is `Conventional`; a caterer who only delivers is `Service Area`.
   Check the About page, plus descriptions and reviews, for actual behaviour.
3. **Mobile turns on movement.** A food truck permanently parked at one site is
   `Conventional`.

Conventional explicitly **includes** POIs within POIs (a shop in a mall, a terminal in
an airport, a department in a university), housing complexes, hotels, transit stations
and bus stops, parking lots, public restrooms, landmarks, AOIs such as parks and
lakes, farmers' markets with recurring dates, and professionals trading under their
own name (`Jane Doe, M.D.`).

It explicitly **excludes**, within those same groups: individual apartment units,
individual hotel rooms, restricted-access administration offices, restricted-access
parking lots, and restricted-access restrooms.

### `Not a POI`

Private residences without a home business · businesses at a P.O. Box or their
accountant's office with nowhere to navigate to · people's names not trading as a
business · temporary pop-ups without a fixed location · non-public amenities (stairs,
lifts, private restrooms) · non-public offices with no public hours · land areas and
territories, including countries, cities, neighbourhoods and indigenous lands · spam
listings · fictitious listings · virtual-only businesses with no in-person location.

**`Not a POI` ends the task.** Nothing downstream is rated.

## State (§3.2)

To be `Active`, the POI must be operating on a regular schedule **at its current,
listed location**. A POI that relocated is not `Active` at the old address — §3.3's
worked example rates the vacated address `Permanently Closed`.

| Option | Meaning |
|---|---|
| **Active** | Currently open and operating. A Seasonal POI must be open *at the time of rating* |
| **Temporarily Closed** | Construction, remodelling, natural disaster, disease, a confirmed future opening date, or a Seasonal POI inside its regular shutdown |
| **Permanently Closed** | Closed, relocated, renamed, or replaced. Evidence may be explicit (official notice, primary publication) or implied (dormant social page with no reviews in the past year) |
| **Can't Verify** | Insufficient, outdated, **conflicting**, or unreliable information |

`Temporarily Closed` removes the Hours question.

### What is *not* a temporary closure

- Reduced hours or services while remaining partially open.
- Seasonal reopening at a **different, non-permanent** location — a holiday
  decorations store that pops up somewhere new each year.
- **Academic breaks and public holidays.** A school is temporarily closed only when an
  official closure announcement is posted.
- **Labour disputes and strikes.**

### The closure procedure (§3.2.1.2.1) — work it in order

**Step 1 — Official sources.** If the official site or claimed social page says closed,
relocated, renamed or replaced → `Permanently Closed`. If official sources give no
indication of closure → `Active`. Exercise discretion where the official source looks
stale or poorly maintained.

**Step 2 — Authoritative and reliable sources.** Only if no official source exists.
A business registry showing closure, an unofficial social page flagged Closed, or one
recent review saying so.

**Step 3 — Count recent user reviews** (within the last year):

- More recent reviews say **open** than sources saying closed → **`Can't Verify`**
- More recent reviews say **closed** than say open → **`Permanently Closed`**
- No closure indications at all, plus a recent review saying open → **`Active`**

> **Only written reviews count.** §3.2.1.2 is explicit that crowdsourced closure
> *banners* are not allowed as evidence. The banner is the site's inference; the review
> is a person's report.

### The search that has to be right

Ask *"is this location open"*, not *"how many locations does this chain have."* An
inventory question returns a chain page and a count; a status question returns the
notice. A missed closure on a live task came from exactly this substitution.
