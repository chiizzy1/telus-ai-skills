# US Address Verification

Source: **Country Specific Guidelines – en_US** (March 2022), supplemental to the global
Maps Search guidelines. This file governs US address ratings. Where it and
`address-accuracy.md` differ on a US result, this file wins.

## Contents

- [Essential components by result type](#essential-components-by-result-type)
- [The USPS gate — when to check at all](#the-usps-gate--when-to-check-at-all)
- [City, postal code, cardinal direction, street type](#city-postal-code-cardinal-direction-street-type)
- [Reading USPS output](#reading-usps-output)
- [Business/POI validation flow](#businesspoi-validation-flow)
- [Address-type validation flow](#address-type-validation-flow)
- [Locale-specific addressing systems](#locale-specific-addressing-systems)

---

## Essential components by result type

Mandatory components for **Maps Search**. Missing a mandatory component is `Incorrect`,
never `Correct with Formatting Issue`.

| Result type | POI name | Street # | Unit # | Street name | Locality | State | Postal code | Country |
|---|---|---|---|---|---|---|---|---|
| **Business / POI** | Yes | Yes | if applicable | Yes | Yes | Yes | Yes | see note |
| **Full address** | n/a | Yes | if applicable | Yes | Yes | Yes | Yes | see note |
| **Street** | n/a | n/a | n/a | Yes | Yes | Yes | Yes | see note |
| **Locality** | n/a | n/a | n/a | n/a | Yes | Yes | No | see note |
| **Postal code** | n/a | n/a | n/a | n/a | Yes | Yes | Yes | see note |
| **State** | n/a | n/a | n/a | n/a | n/a | Yes | No | see note |
| **Country** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | Yes |

> **Country rule.** Optional when the result is **inside** the test locale; **mandatory**
> when the result is outside it. So a US result on an en_US task does not need "United
> States" — but a Canadian result on that same task does.

Features and POIs with no expected address — parks, natural features — are exempt; see
`address-accuracy.md`.

---

## The USPS gate — when to check at all

**You are only required to check USPS when the result address differs from the official
website.** If they match, no check is needed and the address is `Correct`.

This is a gate, not a habit. It exists because a discrepancy between the result and the
official site is *not by itself* a fault — USPS frequently recognises both forms.

| Result vs official website | Action |
|---|---|
| Identical | No USPS check. Rate on the official source |
| Differs on **locality** | Check USPS |
| Differs on **postal code** | Check USPS |
| Differs on **cardinal direction** (E/W/N/S), either direction | Check USPS |
| Differs on **street type** (Blvd/St, Rd/Dr) | Check USPS |
| Differs on anything else | `Incorrect` + the component(s) — no USPS check needed |

Tool: USPS **Look Up a ZIP Code™** — by address, cities by ZIP, or find by business.

---

## City, postal code, cardinal direction, street type

**The controlling question is always: what does USPS return for the RESULT address?**
If USPS returns the result's form, the result is `Correct` even though the official
website says something else.

### City

Multiple localities are often valid for one address — an unincorporated community or
neighbourhood alongside the official postal city.

| Result | Official site | USPS returns | Rating |
|---|---|---|---|
| 2828 Colorado Blvd, **Los Angeles**, CA 90041 | Eagle Rock, CA 90041 | **both** Los Angeles and Eagle Rock | **Correct** |
| 6833 Main St, **Hialeah**, FL 33014 | Miami Lakes, FL 33014 | only Miami Lakes | **Incorrect – Locality** |

### Postal code

Found on USPS → `Correct`. Not found → `Incorrect – Postal Code`. Verify before demoting;
several ZIPs can be valid for one address.

### Cardinal directions and street types

| Result | Official site | USPS returns | Rating |
|---|---|---|---|
| 757 **E** Lewis and Clark Pkwy | *(no direction)* | 757 E Lewis and Clark Pkwy | **Correct** |
| 13801 Independence Blvd | 13801 **E** Independence Blvd | 13801 E Independence Blvd | **Incorrect – Street Name** |
| 142 **S** Chesterfield St | 142 **SE** Chesterfield St | 142 S Chesterfield St | **Correct** |
| 1855 S Stapley **Rd** | 1855 S Stapley **Dr** | 1855 S Stapley Dr | **Incorrect – Street Name** |
| 2823 E MLK **Blvd** | 2823 E MLK **St** | 2823 E MLK Blvd | **Correct** |

Note that three of these five rate **Correct** despite disagreeing with the official
website. Demoting on the website alone would have been wrong in the majority of cases.
Cardinal-direction and street-type faults are `Incorrect – Street Name`, not a separate
component.

---

## Reading USPS output

**DPV Confirmation Indicator** — expand the returned address to see it:

| Indicator | Meaning |
|---|---|
| `Y` | Deliverable. The address exists |
| `N` | Not deliverable. The address likely does not exist |

**ZIP+4.** The four-digit extension is used only to judge whether the address exists.
**Never demote for a missing +4**, and ignore it if the result includes one. An address
returned *without* a +4 designation likely does not exist.

**Error message.** USPS returning an error means non-existent — but check first for
misspellings and mismatched street types, which produce false negatives.

**USPS is not the only word.** Rural homes, PO Box holders and parks can lack mail
service while plainly existing. When USPS cannot validate but other sources show the
address is real — cabins, gated communities — search the number and street in quotes
(`"11413 N Lake Rd" Espyville, PA`) and seek consensus across county assessor or real
estate databases carrying exterior property photos.

---

## Business/POI validation flow

1. **Official website?**
   - **Yes** → does the result address match it?
     - Match → **Correct**
     - Mismatch is locality, postal code, cardinal direction or street type → **check USPS** → confirmed → **Correct**; not confirmed → **Incorrect + component(s)**
     - Mismatch is anything else → **Incorrect + component(s)**
   - **No** → recent **claimed social media**? (an official resource — see `research-evidence.md`)
     - **No** → name and address visible in recent **street imagery**?
       - **No** → seek consensus among **three** unofficial sources → agree → **Correct**; conflicting → **Can't Verify**

Applies only to POIs where a full address is expected.

## Address-type validation flow

1. **Is it a P.O. Box?** → **Incorrect – Address does not exist**
2. Otherwise **check USPS**:
   - Validates → **Correct**
   - Does not validate → research other map providers and sources:
     - Address is associated with some entity → **Incorrect – Other Issue**
     - No entity can be confirmed → **Incorrect – Address does not exist**

---

## Locale-specific addressing systems

Four US systems that look wrong to an outsider and are not.

### Coordinate address system — Utah, Indiana, Idaho, Illinois

Grid-based, with a central `(0,0)` point; streets increment by 100 and are named by
direction from centre.

`1675 S 900 W, Salt Lake City, UT 84104` → street **number** is `1675 S`, street **name**
is `900 W`. Treat the whole thing as number-plus-name when checking USPS.

### Cross-street system — Queens, NYC

Two numbers, a hyphen, then the street. The first is the lower cross street, the second
the position on the block. **The hyphen is optional and must be removed for USPS.**

| Result | Official | Rating |
|---|---|---|
| 6925 49th Ave | 69-25 49th Ave | **Correct** — hyphen optional |
| 3601 31st St | 36-01 31st St | **Correct** |
| **36-1** 31st St | 36-01 31st St | **Incorrect – Street Number** — dropping the `0` changes the address |
| **361** 31st St | 36-01 31st St | **Incorrect – Street Number** — `361` ≠ `3601` |

### County grid — Milwaukee, WI area

`W156N7356 Pilgrim Rd, Menomonee Falls, WI 53051`. The coordinate block `W156N7356` **is
the street number**.

### Counties

Counties are **address-type** results and must carry the word "County".

`Pope, AR` where the expectation is `Pope County, AR` → **Incorrect – Locality**. There is
no city named Pope, AR.
