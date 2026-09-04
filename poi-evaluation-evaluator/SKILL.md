---
name: poi-evaluation-evaluator
description: Evaluate TELUS POI Evaluation tasks. Use when rating a single POI listing across Validity (Eligibility and State), URL, Name, Address, Pin, Phone, Category and Hours; when the task shows one listing with a name, address, coordinates, phone, URL, category string and weekly hours; or when the task mentions Conventional POI, Service Area, Mobile POI, OK Without, Next Door, Approximate category, or a category string with arrow delimiters.
---

# TELUS POI Evaluation Evaluator

## What this task is, and what it is not

POI Evaluation rates **one listing against reality**. There is no query, no user
location, no viewport, no competing results, and no relevance. You are asked whether
this POI is eligible and open, and then whether each stored field is right.

Maps Search Evaluation rates **results against a query**. The two share dimension
*names* — Name, Address, Pin — and share almost none of their *scales*. Confusing
them is the single most expensive error available on this task, and it is the reason
this skill exists. Read `references/maps-vs-poi.md` before your first task, and again
any time a Maps habit feels like it applies.

## File Locations

- `references/...` paths are inside this skill's folder.
- Sibling TELUS skills are reached with `../<skill>/SKILL.md`.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root.
- Blank task template: `TELUS-TASKS/task-templates/poi-evaluation.md`. The live task
  the user is working on is `TELUS-TASKS/task.md`.
- If a referenced external file cannot be found, use this skill's reference files as
  the operative rubric and say plainly that the official source was unavailable.

## Source Hierarchy

1. The rendered official PDF page: `TELUS-TASKS/POI Evaluation/POI Evaluation.pdf`
   (209 pages), including its tables, screenshots, and labels.
2. The current task UI and any visible task-specific instructions.
3. `TELUS-TASKS/poi-extracted/text.md` as a search and navigation aid only.
4. This skill's reference files.
5. User memory, previous chat, or general judgment.

The extraction loses table cells and layout in places. It locates content; it never
overrides a rendered page. If the user or a prior answer conflicts with the guideline,
follow the guideline.

> **Extraction trap carried over from Maps.** Search this text with a pattern that
> tolerates a non-breaking space, or you will get zero hits on phrases that are
> present. `grep -P 'Rate[\s\xc2\xa0]+Bad'`, or normalise first:
> `python3 -c "print(open(p).read().replace(chr(0xa0),' '))"`.

## The nine questions, in order

| # | Question | Options | Reference |
|---|---|---|---|
| 1 | **Eligibility** | Conventional POI · Seasonal · Home Based · Service Area · Mobile · Not a POI · Can't Verify | `validity.md` |
| 2 | **State** | Active · Temporarily Closed · Permanently Closed · Can't Verify | `validity.md` |
| 3 | **URL** | Correct · Partially Correct · OK Without · Missing · Incorrect · Can't Verify | `url.md` |
| 4 | **Name** | Correct · Partially Correct · Incorrect | `name.md` |
| 5 | **Address** | Correct · Correct - Formatting Issue · Incorrect · OK Without · Missing · Can't Verify | `address.md` |
| 6 | **Pin** | Perfect · Approximate · Next Door · Wrong · Can't Verify | `pin.md` |
| 7 | **Phone** | Correct · OK Without · Missing · Incorrect · Can't Verify | `phone.md` |
| 8 | **Category** | Correct · **Approximate** · Missing · Incorrect | `category.md` |
| 9 | **Hours** | Correct · OK Without · Missing · Incorrect · Can't Verify | `hours.md` |

Two gates change what you are asked:

- **Eligibility `Not a POI`** ends the task. Nothing downstream is rated.
- **State `Temporarily Closed`** removes the Hours question entirely (§10).

`Perfect` on Pin adds the follow-up *"Does the available evidence indicate the POI's
precise location?"* — `Yes` or `No`. Answer it from the evidence, not from your
confidence.

## Mandatory recon gate

Do not rate any dimension until the recon has run and you have read its output.
Rating from a search snippet is the failure mode this gate exists to stop.

```bash
python3 telus-ai-skills/poi-evaluation-evaluator/scripts/poi_recon.py TELUS-TASKS/task.md
```

It refuses to run on missing inputs, rather than guessing them. If it refuses, fill
the named field in `task.md` and run it again.

| Missing input | What the script does | What you must not do |
|---|---|---|
| Listed coordinates | Refuses | Estimate the pin from the address |
| Listed address | Refuses | Rate Pin against a reverse-geocode alone |
| POI name | Refuses | Proceed on the URL's page title |
| Listed URL | Runs, flags `no_listed_url` | Assume `OK Without` before searching for a site |

### Four rules the script cannot enforce

1. **Read the saved page, not the status code.** A `200` on a parked domain proves
   nothing; a `404` on a chain locator is real closure evidence.
2. **A snippet is not proof.** Snippets locate a source. Only the opened source
   substantiates a rating. This rule has cost a correct rating before.
3. **Cite nothing you did not open.** Saying a page could not be read always beats
   implying you read it.
4. **Batch your own lookups.** Collect every URL you need, fetch them in one parallel
   pass, then reason. Six sequential single-page fetches is how a four-minute task
   becomes a twelve-minute one.

## Source tiers — three, consulted in order

POI uses **Official → Authoritative → Reliable**, and the middle tier does not exist
in the Maps skill. Full detail in `references/research-sources.md`.

| Tier | Members | When |
|---|---|---|
| **Official** | Official website; claimed social media **updated within 12 months** | Always first |
| **Authoritative** | Postal authorities, government maps and cadastre, government business registries | When official is absent, or to confirm what official does not state |
| **Reliable** | Crowdsourced review sites, unofficial social pages, primary publications | Only after the two above are exhausted; rate on *consensus among several* |

Unreliable sources — aggregators, spammy directories — are never used, and consensus
among them is disregarded entirely.

> **SERPs are a locator, not a source.** §2.1.1.1 is explicit: search engine results
> pages may be used to *find* official sources, but never to corroborate POI data or
> confirm open/closed status. **Hours are stricter still** — §10.1.1 permits only the
> official website or official social page, and specifically bars review sites, street
> imagery, SERPs, and online maps services *even when the official source points at
> them*.

## Rules that decide cases, and are easy to get backwards

- **Category has an `Approximate` band.** An accurate-but-overly-broad category is
  `Approximate`, not `Correct` (§9.1). Maps has no such band. This is the divergence
  that produced a wrong answer on a live assessment.
- **Website beats social media on conflict** (§10.1.1.2), and website beats user
  reviews. Maps treats a claimed social account as a peer of the site; POI does not.
- **A correct social page is `Incorrect` when an official website exists** (§4.1) —
  because the site should have been prioritised. A right answer in the wrong tier.
- **A social page not updated within 12 months is `Incorrect`,** not `Can't Verify`.
- **`Can't Verify` on URL means temporary downtime** — a 503 or maintenance page. A
  404 is `Incorrect`. Do not use `Can't Verify` for "I could not reach it."
- **URL homepage-vs-location-page is conditional both ways.** A parent homepage is
  `Partially Correct` **only if** a location-specific page exists. If the chain has
  none, the main page is `Correct`. Go and check for the location page — the answer
  turns entirely on whether it exists.
- **Extra listing information must be verified, not assumed** (§6.1). A suite number
  the operator never publishes and no authoritative source confirms makes the address
  `Incorrect`, not `Correct - Formatting Issue`. `Formatting Issue` is for data that
  is *superfluous but true*.
- **A pin is rated on its own.** §7.1 states the pin rating must not be influenced by
  the address or any other field. A pin can be `Perfect` while the address is wrong.
- **`OK Without` is a research finding.** It asserts the POI *has* no website, phone,
  or hours. Reaching it requires a search that came back empty, not a search you did
  not run.
- **Seasonal POIs are rated on the rating date.** Open today → `Active`. Closed during
  a regular seasonal shutdown → `Temporarily Closed`.
- **Academic breaks, public holidays and labour strikes are not temporary closures.**

## Comments

Mandatory whenever research contradicts the listing, and whenever you rate
`Can't Verify`. Include the research URLs, the corrected value, and — for a bad pin —
the corrected coordinates. Keep them short and in English. No URL shorteners, no PII.

POI diverges from Maps here: §11.1 **asks** you to reference the guideline rule when a
rating turns on a guideline intricacy. In Maps that reads as robotic; here it is best
practice. Examples and the house style are in `references/comments.md`.

## Before you submit — audit

1. Did the recon run, and did you read its output rather than the summary line?
2. Eligibility: did you check the *structure type* for Home Based, and *whether the
   POI travels* for Service Area and Mobile?
3. State: for a suspected closure, did you work §3.2.1.2.1's three steps in order —
   official, then authoritative/reliable, then a recent-review count?
4. Did you confirm whether a **location-specific page** exists before rating URL?
5. Is the social page you relied on **claimed** and **updated within 12 months**?
6. Name: did you check every name the location uses for *itself*, including its own
   social page, before demoting on directory consensus?
7. Name demotion: did you tick the specific error components?
8. Address: did you forward-geocode the claimed address rather than only reverse-
   geocoding the pin?
9. Address: is any component present in the listing but absent from official sources
   verified through an authoritative source?
10. Pin: did you rate it independently of the address?
11. Pin `Perfect`: did you answer the precise-location follow-up from evidence?
12. Category: did you consider `Approximate` before settling on `Correct`?
13. Category: did you check the Category Reference List even though the listed one
    looked fine (§9.1.2 rule 5)?
14. Hours: did you use **only** the official website or official social page?
15. Hours: did you get the **full week**, not the current-day default?
16. Did any dimension get `Can't Verify` because a fetch failed rather than because
    the evidence does not exist?
17. Are comments present for every contradiction and every `Can't Verify`?
18. If the task UI offered an option not listed in this file — **stop.** You are not
    on a POI Evaluation task. Noticing the anomaly is not enough; explaining it away
    is the failure, and hedging is not enough either.
