# Research and Evidence Protocol

What counts as proof for each rating dimension, and what to do when proof is not available.

The governing rule comes from the shared TELUS quality gate: **never report a verification you did not perform.** Saying a page could not be read is always better than implying you read it.

> **This file says what counts as proof. `research-workflow.md` says how to go and get it** — the phase order, the exact commands for `check_urls.py`, reverse-geocoding and distance ranking, and the fallback ladder for when a source returns 403, a captcha, or an empty JavaScript shell. Run the workflow; use this file to judge what it brings back.

## Contents

- [Absolute rules](#absolute-rules)
- [Source priority](#source-priority)
- [Research by dimension](#research-by-dimension)
  - [Query intent](#query-intent) · [Existence and closure](#existence-and-closure) · [Official name](#official-name) · [Category](#category) · [Address](#address) · [Pin location](#pin-location) · [Prominence](#prominence) · [Distance](#distance)
- [When evidence runs out](#when-evidence-runs-out)
- [Disclosing evidence in the output](#disclosing-evidence-in-the-output)

## Absolute rules

1. **Never call a business.** Phone numbers in the pop-up box are research context only — for matching an entity against a known listing, never for dialling.
2. **Never claim a page, map, or image was checked when it was not.**
3. **A search snippet is not proof.** Snippets locate a source; only the source itself substantiates a rating.
4. **Pin ratings need consensus** from multiple reliable resources, including aerial and street-level views wherever both exist.
5. **The task's own map is the final arbiter for pins.** Even when coordinates were gathered elsewhere, rate pin placement on what is actually visible in the tool's layers.
6. **Do not rate the pop-up box.** Rate only the information in the result itself.
7. **An obvious error stays rateable** even when everything else is unverifiable — a missing mandatory address component or a pin in the ocean does not become `Can't Verify` merely because the official website is unreachable.

## Source priority

The guideline sorts sources into **three buckets, not a ranked list**. Use an Official
Resource first. Only when none exists do you fall back to consensus among multiple
Reliable Resources. Unreliable resources are never used at all.

### Official — always try these first

| Source | Use for |
|---|---|
| The entity's **official website** — About/About Us, storefront signage shown on it | Name, address, category, closure |
| **Official chain locator** page | Chain branch names, addresses, which branches exist. A 404 is positive closure evidence |
| **Claimed social media pages** — Facebook, Instagram, X | Name, address, closure announcements, current signage |
| **Street-level imagery** | Signage, whether the premises still operate, which unit a business occupies |
| **Postal authorities** — USPS in the US | Address existence and component accuracy. See `us-address-verification.md` |
| **Official government maps and business registries**, land registry / cadastral maps | Address existence, property boundaries, which rooftop |
| **Official venue maps and directories** — malls, campuses, airports, stations | Unit-level location inside a complex |

> **Claimed social media is OFFICIAL, not a fallback.** Many markets use a Facebook page
> instead of a website, and the guideline says so explicitly. Treat a claimed, recently
> managed account as equal to the operator's own site — go there *before* directory
> listings, not after. A name demoted on directory consensus while the operator's own
> page said otherwise is a wrong rating.

### Reliable — consensus among several, when no official source exists

| Source | Use for |
|---|---|
| **Crowdsourced review sites** — Yelp, TripAdvisor, Yellow Pages | Name, address, hours, and structured status flags such as a CLOSED banner |
| **Articles in primary publications** — outlets doing their own reporting | Closure, renaming, relocation |
| **Local newspaper and media reporting** | Same |
| **Reliable online map resources** — Google, Bing, MapQuest, HERE WeGo, in multiple views | Pin placement, boundaries, street layout |
| **Wikipedia** | Coordinates for well-known landmarks, parks and major POIs |

These are **usable**, not merely corroborating. Where no official source exists, a
consensus across several of them supports a rating on its own.

### Unreliable — never use

Data aggregators, spammy directory sources, unverified listing scrapers. **Consensus
between unreliable sources is to be disregarded entirely** — three aggregators agreeing
is worth nothing. This is also why an aggregator listing that persists years after a
closure proves nothing.

Official restaurant menus, including scanned or user-photographed ones, are acceptable
supporting evidence for a business name.

## Research by dimension

### Query intent

Establish what the user wanted **before** looking at results. Research the query itself when it has more than one plausible reading — the guideline is explicit that you must understand the query rather than guess. Obvious misspellings are read as the intended term. Foreign-language queries are researched or translated, never released.

### Existence and closure

Always research the real-world state, whatever the status field claims.

**Batch the page fetches first.** Each result's pop-up carries a URL. Collect them and run one parallel pass before reading anything:

```bash
python3 telus-ai-skills/tools/check_urls.py --query "<the map query>" --run-id "<task-id>" <url1> <url2> ...
```

It fetches concurrently (default 4 workers, `--workers N` to change), falls back to a browser for JavaScript-heavy or bot-protected pages, and writes the extracted text plus `report.json` to `TELUS-TASKS/url_content/<run-id>/`. One run settles the page-based half of existence, official name, and address for every result at once, instead of fetching them one at a time.

Read the saved content, not just the status codes. A `200` on a chain locator that no longer lists the branch is evidence of closure; a `200` on a parked domain is not evidence of anything.

What the checker cannot do here, so do not wait on it for these:

- **Pin accuracy** — needs map imagery, not page text. That comes from the screenshot.
- **Distance** — from coordinates via `../../tools/maps_distance.py`.
- **Address-type results** — a street, locality or postal code has no business URL to fetch.
- **Results whose pop-up has no URL** — fall back to searching for the official site by name.

A checker failure (403, CAPTCHA, timeout, empty extraction) is **manual review**, not proof of closure. Treat it as evidence not yet gathered, and say so.

- Evidence **for** closure: an official page or claimed social account saying so; a primary publication reporting it; recent street imagery showing the premises vacant or rebranded; removal from an official chain locator.
- Evidence **against**: current opening hours on the official site, recent managed-account posts, a current chain-locator listing.
- A temporary closure announced by the business is **open**, with no limit on duration.
- Entity exists nearby but the result's data is wrong → that is a data-accuracy fault, not non-existence.

### Official name

Every name a location uses for itself is correct. Look for it in the chain locator, the About section, storefront signage on official sites or claimed accounts. Failing those: signage in recent street or online imagery, crowdsourced review pages, recent primary publications, official menus.

The corporate name is not automatically the correct name for a specific location. If the name cannot be confirmed and nothing is objectively wrong with it, rate `Can't Verify`.

### Category

Research what the entity actually does, and what entities of that kind typically offer **in that market** — soft-category membership is market-dependent. An incorrect category forces the combined rating to `Incorrect` regardless of the name.

### Address

Confirm against the official website first, then government/postal registries. For a business with no official address listed, a consensus of three sources is acceptable; failing that, `Can't Verify`.

`Can't Verify` is the right call when there is no official webpage, no official address listed, a general absence of official resources, no street imagery, or the official source uses an unexpected format such as an intersection (`Main St and 2nd St`) or exit (`Exit 5, Hwy 101`) address.

### Pin location

Build **consensus** across map resources, aerial views, hybrid views, street imagery, and official venue maps. Then reconcile with the task's own map layers — that reconciliation is mandatory, not optional.

**In practice that reconciliation happens through a screenshot.** An agent cannot open the rating tool, so the user supplies a zoomed satellite or hybrid frame per result, plus one Show All frame for the task. Those images are the tool's map layer; judge them rather than asking the user to pre-judge them. Full method in `pin-accuracy.md` → *Judging a pin from a screenshot*. Two rules carry over here: an image has **no scale**, so distance still comes from coordinates via `../../tools/maps_distance.py`; and `Can't Verify` is for evidence that does not exist, not for a frame you were not sent — ask for a better frame first.

Evidence strength determines how precise the pin must be to earn `Perfect`: the more evidence available for the location, the tighter the Perfect area becomes.

| Situation | Rating |
|---|---|
| Specific location under a shared rooftop identified by strong evidence | Only that location is `Perfect` → follow-up `Yes` |
| Shared rooftop identified, specific location within it unconfirmed | The whole rooftop is `Perfect` → follow-up `No` |
| Several rooftops share the address, no strong evidence which one | `Can't Verify` |
| The result *is* the shared address (address-type, e.g. an apartment complex where every building carries it, §10.1) | `Perfect` — no "which building" question exists |

> **The distinction that decides this.** Uncertainty *within* one identified rooftop is `Perfect` + follow-up `No`. Uncertainty about *which* rooftop is `Can't Verify`. The §9.1.1.1 options table reads as if a multi-rooftop parcel is a `Perfect` + `No` case; the §9.2.2 prose and the escalation above are the governing reading, and the §10.1 apartment-complex example is an address-type exception rather than a contradiction of it. Blind testing confirmed a rater will otherwise answer `No` to escape a "which building?" problem and wrongly award `Perfect`. Confirm against rendered pages 116, 119 and 179 if a task turns on it.

Leave a comment with coordinates and resource links whenever the pin was difficult to judge or could not be verified.

### Prominence

Judge against real-world candidates, not the returned set. Primary publications, official rankings, and visitor-volume evidence support a prominence claim. "It appeared first" is not evidence of prominence.

### Distance

Measure from the **outer edge of the user viewport**, never from the device icon, which has no rating significance. The tool's ruler gives distances directly.

Compare against **all real-world candidates**, not only the displayed results — a closer option that was not returned still demotes the ones that were. Density sets the scale: the same absolute distance can be acceptable in a rural area and a demotion in a dense one.

`../../tools/maps_distance.py` computes straight-line distance between coordinate pairs deterministically. It informs a rating; it never decides one.

## When evidence runs out

Say so, then apply the rubric's own fallback — do not invent a rating and do not default everything to the middle.

| Situation | Correct outcome |
|---|---|
| Closure undecidable | Assume it could exist; Name/Address/Pin → `Can't Verify` |
| Name unconfirmable, nothing objectively wrong | Name → `Can't Verify` |
| Address unconfirmable | Address → `Can't Verify` |
| Pin unconfirmable | Pin → `Can't Verify`, with coordinates and links in the comment |
| Evidence genuinely tied on existence | Check `Business/POI is closed or does not exist`; rate relevance as if it existed |
| Rating Search Relevance only, existence unclear | Same as tied — checkbox, then relevance as if it existed |
| Obvious data fault present | Stays rateable. `Can't Verify` does not apply |

`Can't Verify` is a finding, not an escape hatch. Use it only where the rubric permits it, and never to avoid a judgement the evidence actually supports.

### Two checks you must run before rating `Can't Verify`

Both are cheap, and skipping either has produced a wrong `Can't Verify` on a real task:

1. **Forward-geocode the claimed address and measure the pin against it.** The recon does this automatically and prints *pin sits N m from the claimed address*. A reverse lookup only says what is *nearest* — it will happily name the neighbouring door. Two unit numbers 4 m apart in one building read as "different feature" and are not. The pin-to-claimed distance is the actual question.
2. **Run one targeted search for another source.** If a rating turns on a source count — the back-office rule needs the operator's site or a consensus of three — go and look for the third before giving up. **A host on the recon's walled list still counts.** The script cannot fetch Yelp or MapQuest; you can reach both through search, and what they show is evidence.

`Can't Verify` means the evidence does not exist. It does not mean the script could not fetch it.

## Disclosing evidence in the output

Every non-obvious rating names the evidence type behind it, or states plainly why verification was impossible. These phrases are the **floor**:

- `official site — hours listed, open`
- `chain locator — branch absent; primary publication confirms closure`
- `aerial + street imagery agree; reconciled with task map`
- `no official page, no street imagery — Can't Verify`

**The working standard is one clause per dimension the source supports, with the numbers included — see `output-style.md`.** The task-facing comment stays bare so it pastes cleanly; the chat output carries the distances, coordinates, source tiers and reasoning, so the rater can audit each rating and overrule you where the evidence is thin.
