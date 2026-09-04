# Address (§6)

Six bands, and the two extra ones — `Correct - Formatting Issue` and the
`OK Without` / `Missing` split — are where Maps habits go wrong.

| Option | Meaning |
|---|---|
| **Correct** | Complete, accurate, and formatted as the locale expects |
| **Correct - Formatting Issue** | Complete and **correct**, but not in the country's default format, or carrying unnecessary tokens, repetitions, or incorrect labels |
| **Incorrect** | The listed address has incorrect **or missing** information. Component checkboxes appear — tick every one |
| **OK Without** | No address listed, and the business has no official address |
| **Missing** | No address listed, but the business does have one that should be present |
| **Can't Verify** | Cannot be verified from insufficient, outdated, or unreliable information |

## The rule that decides added components

> **§6.1:** *"If more information is shown in the listing than what is shown on the
> POI's official sources, the additional information must be verified through other
> authoritative sources."*

A suite, unit or floor number that the operator does not publish is not automatically
a formatting quirk. Go and try to verify it against an authoritative source. If it
cannot be confirmed anywhere, the address carries information that is not right, and
that is **`Incorrect`** — tick the Unit/Apt component.

`Correct - Formatting Issue` is for material that is **superfluous but true**: a
duplicated label, a redundant country, a non-default component order. It is not a
parking spot for a component you could not confirm.

The direction is fixed by §6.6's worked case: 85°C Bakery Cafe, listed `2700 Alton
Pkwy, Ste 121` against an actual `Ste 123`, is **`Incorrect`**. A suite that does not
exist at all is no better than a suite with the wrong number.

Nor is an unverifiable added component `Can't Verify` — that band is for an address you
cannot establish. When the street address is confirmed by the operator's own site and
a dozen other sources, the address *is* established; it is the extra token that fails.

## Market Specific Issue vs Correct - Formatting Issue (§6.1.2.1)

The line is the **accuracy of the data**, not how odd it looks:

- Data is correct → `Correct - Formatting Issue`
- Data is very unusual, potentially misleading, or wrong →
  `Incorrect – Market Specific Issue`

Use Market Specific Issue for address problems no other checkbox covers — a market
that requires a municipality alongside locality and state, where that component is
missing or wrong.

## Language/Script Issue (§6.1.1)

Address components must be in the test language and script. **Any** combination of
unexpected language or script is `Incorrect`. The single exception is special
characters that are simply not used in the expected language.

You are not expected to master address formats outside your locale — do the normal
research steps and no more.

## Other (§6.1.3)

Use `Incorrect – Other Issue`, with a comment and links, for:

- **Duplicated components** — `146b 146b Basin Street`
- **The POI's name repeated inside the address**
- **Formatting issues alongside components you have already marked incorrect** —
  because once anything is `Incorrect`, `Correct - Formatting Issue` is no longer
  selectable

## Minimum components (§6.3.1)

Expected components vary by POI type. Large, notable POIs are not required to carry a
street number and street name, and an address giving only locality, state and postal
code is **not vague** for them — it is `Correct`:

- `Liberty Island, New York, NY` — Statue of Liberty
- `Hollywood, Los Angeles, CA 90068` — Hollywood Sign
- `Knoxville, TN 37996` — University of Tennessee
- `San Francisco, CA 94128` — San Francisco International Airport
- `San Francisco, CA` — a bus stop on the side of a street, which is not expected to
  have a street number given its non-conventional location

The corollary decides `Missing`: SFO with **no** address listed is `Missing`, because
the locality is its minimum component and the listing lacks it.

## Before rating `Can't Verify`

**Forward-geocode the claimed address and measure the pin against it.** A reverse
lookup only tells you what is *nearest* the pin — it will happily name the next door
along. Two unit numbers four metres apart in one building read as different features
and are not. A wrong `Can't Verify` on a live task came from skipping this.
