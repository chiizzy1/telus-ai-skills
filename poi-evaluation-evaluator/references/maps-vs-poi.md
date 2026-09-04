# POI Evaluation vs Maps Search Evaluation

Two TELUS families, four shared dimension names, and almost no shared scales. This
file exists because a measured assessment failure came from answering POI questions
out of the Maps rubric — twice, in a run of seven.

## The failure this file prevents

On a live POI assessment I rated an overly broad category `Correct`, writing that
*"Approximate is not a category label anywhere in the rubric"* and calling the option
a distractor. It is §9.1, a real band that Maps does not have. On another question I
named the exact risk, put my confidence at 75/25, and answered from the Maps rule
anyway.

The lesson is not "be more careful." It is procedural:

> **A rating option you do not recognise is evidence you are on the wrong rubric —
> not evidence that the option is a distractor.** Stop and get the right guideline.
> Detecting the anomaly and explaining it away is the failure. So is hedging: a
> confidence estimate does not substitute for the governing document.

## What has no equivalent in POI

Relevance. Query intent. Viewport versus user location. Distance ladders. Prominence.
Competing results. If you find yourself reasoning about any of these, you have
imported a Maps habit into a task that has no query in it.

## Dimension-by-dimension divergence

| Dimension | Maps Search | POI Evaluation |
|---|---|---|
| **Category** | Folded into Name & Category; a wrong category forces `Incorrect` | Its own question with four bands, including **`Approximate`** (§9.1) for accurate-but-overly-broad |
| **Name** | `Correct` / `Partially Correct` / `Incorrect` / `Can't Verify` | `Correct` / `Partially Correct` / `Incorrect` — **no `Can't Verify`**, plus mandatory error-component checkboxes |
| **Address** | `Correct` / `Partially Correct` / `Incorrect` / `Can't Verify` | Six bands including **`Correct - Formatting Issue`**, **`OK Without`** and **`Missing`**, plus component checkboxes |
| **Pin** | `Perfect` / `Approximate` / `Next Door` / `Wrong` / `Can't Verify` | Same five labels — **the one genuine overlap** — plus the precise-location follow-up on `Perfect` |
| **Source tiers** | Official → Reliable (two tiers) | Official → **Authoritative** → Reliable (three tiers) |
| **Claimed social media** | Official; peer of the website; prefer the more recent on conflict | Official **only if updated within 12 months**; the **website wins** on conflict (§10.1.1.2) |
| **Hours** | Not rated | Rated, from the **official website or official social page only** — review sites, SERPs, street imagery and maps services all barred (§10.1.1) |
| **Existence / closure** | A checkbox that gates the data dimensions | A first-class question, **State**, with four bands and a three-step research procedure (§3.2.1.2.1) |
| **Eligibility** | No equivalent | A first-class question that can **end the task** (`Not a POI`) |
| **Comments** | Naming the guideline section reads as robotic | §11.1 **asks** you to reference the rule when a rating turns on a guideline intricacy |
| **"Nothing there" answers** | `Can't Verify` carries most of the load | Split three ways: **`OK Without`** (correctly absent), **`Missing`** (wrongly absent), `Can't Verify` (undecidable) |

## The `Can't Verify` divergence, specifically

Maps uses `Can't Verify` broadly for "the evidence does not exist." POI narrows it per
dimension, and on URL it means something else entirely:

| Dimension | POI meaning of `Can't Verify` |
|---|---|
| State | Insufficient, outdated, **conflicting**, or unreliable information |
| **URL** | **Temporary downtime only** — 503, maintenance page. A 404 is `Incorrect` |
| Name | Not offered. You must choose one of the three bands |
| Address | Cannot be verified from available sources |
| Pin | Pin is inside the **smallest identifiable area**; outside it is `Wrong` |
| Phone | Cannot be verified using an **official** source |
| Hours | Cannot be verified using an official source; also the answer when the official site itself lists **contradictory** hours |

## The trap that runs the other way

Do not import POI rules into a Maps task either. `Approximate` is not a Maps category
band, the Maps address scale has no `Correct - Formatting Issue`, and a Maps rating
that demotes a claimed social account below the official website is wrong. The Maps
skill carries the matching warning in its Platform Separation section.
