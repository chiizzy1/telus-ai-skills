# Research Workflow

The **executable order of operations** for a Maps task. `rating-contract.md` decides which label you may use and `research-evidence.md` decides what counts as proof; this file decides **what to run, in what order, and what to do when a source blocks you**.

> **Run `scripts/maps_recon.py` first — it executes Phases 0–3 in one command** and writes an evidence bundle with a RUN ID that your output must quote. See SKILL.md, *Mandatory Recon Gate*. This file is the manual fallback and the reference for interpreting what the script reports: the fallback ladder for blocked sources, how to read a reverse-geocode result, and what no tool can settle.

Run the phases in order. Each one says what it settles and what it cannot settle. Skipping a phase is allowed only when the phase has nothing to act on (no pins shown, no business results), and the omission is stated in the output.

All commands are written to run from the **workspace root** (the folder containing `telus-ai-skills/` and `TELUS-TASKS/`).

## Contents

- [Phase 0 — The location-intent gate](#phase-0--the-location-intent-gate)
- [Phase 1 — Batch the page fetches](#phase-1--batch-the-page-fetches)
- [Phase 2 — Reverse-geocode every pin](#phase-2--reverse-geocode-every-pin)
- [Phase 3 — Build the candidate set and rank it](#phase-3--build-the-candidate-set-and-rank-it)
- [Phase 4 — Confirm real-world state](#phase-4--confirm-real-world-state)
- [The fallback ladder](#the-fallback-ladder)
- [Batch your own lookups](#batch-your-own-lookups--one-round-trip-not-six)
- [What no tool can settle](#what-no-tool-can-settle)

---

## Phase 0 — The location-intent gate

**No tool. Do this before touching anything else,** and write the conclusion into the output header. It decides which distance column in the result card means anything — and frequently the answer is *neither*.

Work the overrides top-down and **stop at the first match**:

| # | Condition | Location intent | Consequence |
|---|---|---|---|
| 1 | Query names a place — locality, full address, street, named POI | **The stated place** | Ignore user location **and** viewport entirely. Both distance columns are noise. |
| 2 | Query says "near me" / "nearby" / "nearest" / "my location" | **User location** | Ignore the viewport even when it is FRESH. |
| 3 | Otherwise | Apply the decision table in `user-intent.md` | Fresh + user inside → user location. Fresh + user outside → viewport. Stale → user location. |

Row 1 is the single highest-leverage line in this skill and the most common source of a wrong rating. A query like `[loves travel stop Boise, ID]`, `[food Tulsa, OK]` or `[Chevron 225 Langley Drive Lawrenceville GA]` fixes its own intent; demoting such a result because it sits far from the user is the guideline's own named "common wrong answer".

Row 3 needs the **Show All** screenshot to settle user-inside-vs-outside. The device icon marks the viewport's centre, never the user — do not read it as the user. Ask for Show All rather than inferring, because inside-vs-outside inverts the outcome.

Record the conclusion as one line before rating anything:

> `Location Intent: <conclusion> — <why>. Distance columns that matter: <User | Viewport | neither>.`

## Phase 1 — Batch the page fetches

One parallel run, before reading anything. Never fetch pages one at a time.

```bash
python3 telus-ai-skills/tools/check_urls.py \
  --query "<the map query>" \
  --run-id "maps-<slug>-<YYYYMMDD>" \
  --workers 8 \
  <url1> <url2> <url3> ...
```

What to put in the batch, in this order of preference:

1. Every result pop-up URL the task provides.
2. Where a pop-up has no URL — the chain's **official store locator page** for that branch, guessed from its URL pattern (`local.safeway.com/safeway/<st>/<city>/<street>.html`, `stores.victoriassecret.com/us/<st>/<city>/`, `loves.com/locations/<st>/<city>/…`). A **404 on a chain locator is positive evidence of closure**, so a failed guess is still informative.
3. A search-engine URL per unidentified business, to discover the official site.

Then **read the saved `.txt` files**, not the status codes:

```bash
ls TELUS-TASKS/url_content/<run-id>/
sed -n '22,80p' TELUS-TASKS/url_content/<run-id>/0N_<host>.txt
```

A `200` on a locator that no longer lists the branch is evidence of closure. A `200` on a parked domain is evidence of nothing — one Willard coffee shop's apparent official domain now serves gambling spam, and an agent cited it as confirming the menu.

> **Gotcha:** if the run folder already exists, `check_urls.py` writes to `<run-id>-NNNNNN` instead. Never create the folder first, and check for a renamed sibling before concluding a fetch produced nothing.

**Settles:** existence, closure, official name, official address, official category.
**Cannot settle:** pin placement, distance, anything about an address-type result.

## Phase 2 — Reverse-geocode every pin

Run once per result pin. Space the calls ~1s apart and send a User-Agent — the service is free and rate-limited.

```bash
curl -s -A "telus-eval/1.0" \
  "https://nominatim.openstreetmap.org/reverse?lat=<LAT>&lon=<LNG>&format=json&zoom=18" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('display_name'))"
```

Also geocode the **claimed** address forward, so you can compare the two:

```bash
curl -s -A "telus-eval/1.0" \
  "https://nominatim.openstreetmap.org/search?q=<urlencoded+address>&format=json&limit=3" \
  | python3 -c "import sys,json;[print(r['lat'],r['lon'],'|',r['display_name']) for r in json.load(sys.stdin)]"
```

**Settles:** which parcel, building or POI the pin actually sits on; disputes over locality and postal code; whether pin and claimed address agree.

**Read the output as a lead, not a verdict.** It returns the nearest addressable feature, not a building footprint, so treat these patterns carefully:

| Pattern | What it usually means |
|---|---|
| Returns the result's own name at the result's address | Strong corroboration → `Perfect` is well supported |
| Returns a **neighbouring business** | Investigate whether they share one building before concluding `Next Door` — inside a shared space `Next Door` does not exist at all |
| Returns a **different locality or postcode** | Check the postal city against the official source before demoting; rural ZIPs routinely span several communities |
| Returns only a street name | The dataset has no address point there; fall back to the screenshot |

**Cannot settle:** rooftop-vs-parcel. That is decided on the supplied hybrid frame, per `pin-accuracy.md`.

## Phase 3 — Build the candidate set and rank it

The demotion trigger in `relevance.md` is *"other results that satisfy the query and provide the same or similar service are closer"* — judged against **all real-world candidates, not the returned set**. This phase produces that set. It is what catches a better result the task failed to return.

Find candidates inside a box around the location intent:

```bash
curl -s -A "telus-eval/1.0" \
  "https://nominatim.openstreetmap.org/search?q=<Brand+or+Category>&format=json&limit=20&viewbox=<W>,<N>,<E>,<S>&bounded=1" \
  | python3 -c "import sys,json;[print(r['lat'],r['lon'],'|',r['display_name'][:70]) for r in json.load(sys.stdin)]"
```

**OSM chain coverage is patchy — always cross-check against the brand's official locator** before concluding a location does or does not exist. OSM listing three Victoria's Secret stores in Wisconsin when the official directory lists nine is typical.

Then rank everything, returned and un-returned, from the location intent:

```bash
cat > /tmp/pairs.txt <<'EOF'
intent->R1 <name>: <INTENT_LAT>,<INTENT_LNG> <R1_LAT>,<R1_LNG>
intent->R2 <name>: <INTENT_LAT>,<INTENT_LNG> <R2_LAT>,<R2_LNG>
intent->X <name> (NOT RETURNED): <INTENT_LAT>,<INTENT_LNG> <X_LAT>,<X_LNG>
EOF
python3 telus-ai-skills/tools/maps_distance.py --batch /tmp/pairs.txt
```

Sanity check: the computed distances should reproduce the card's `Distance to User` values. When they do, the pin coordinates are confirmed. When they don't, something is misread — recheck before rating.

Present the ranking as a table in the output, marking which candidates were **not returned**. Two rules then fall straight out of `relevance.md`:

- A closer satisfying candidate exists → demote the returned ones.
- The result **is** the closest that exists → **do not demote for distance at all**, however far it is.

**Only open, existing candidates count.** A closed branch never demotes anything, which makes Phase 4 a prerequisite for trusting this ranking.

## Phase 4 — Confirm real-world state

Run for every business/POI result, whatever the `Status` field says — blank status is not evidence of trading.

| Evidence **for** closure | Evidence **against** |
|---|---|
| Official locator returns **404** for that branch | Current hours on the official page |
| Branch absent from the official store directory | A current listing in the official directory |
| Primary publication reporting the closure | Recent posts on a claimed social account |
| Recent street imagery showing the unit vacant | Live booking or ordering links |

Aggregator and directory listings **persist for years after a store closes** and are not evidence of existence. Confirm against the operator's own source before letting a listing affect a distance ranking.

Then apply `result-level-issues.md`. The distinction that changes the rating: with **no `PERMANENT_CLOSURE` status shown**, a researched closure means check the box and rate relevance *as if open, with no demotion for closure*. The −2 demotion applies only when the tool actually displays `PERMANENT_CLOSURE`.

## The fallback ladder

Blocking is normal — expect it on Yelp, Cloudflare-fronted brand sites, Simon mall directories and search engines under load. A blocked source is **evidence not yet gathered**, never proof of closure and never an excuse for `Can't Verify`. Work down the ladder until something answers:

| Symptom | Next move |
|---|---|
| `403` + captcha (Yelp, Restaurantji, Trulia) | `WebSearch` the same question — titles and snippets often carry the address and hours |
| `403` Cloudflare on a brand site | Search for the **specific branch page** URL, then fetch that rather than the index |
| `202` / DuckDuckGo returns a JS shell | Switch channel entirely to `WebSearch`; the HTML endpoint is rate-limited |
| `200` but "No extractable content" | JavaScript-rendered. `WebFetch` the canonical URL, or search for a mirror carrying the same data |
| `500` on an official locator index | Fetch a per-state or per-branch page instead of the index |
| Every route blocked | Say so explicitly in the evidence line, name the tier you could not reach, and rate on what you did verify |

Never report a check you did not perform. "The official locator was Cloudflare-blocked, so name rests on directory consensus" is a passing answer; implying you read the locator is a critical failure.

## Batch your own lookups — one round trip, not six

The recon script parallelises its own fetches. **It cannot parallelise yours.** When it finishes, a fixed set of questions is left open, and they are independent of one another — so issue them **together**, in a single message where your harness allows multiple tool calls per turn. Where it does not, still plan them as one list and work straight through without interleaving.

After the recon prints, the open questions are always drawn from this list:

| Question | When it is open | Tool |
|---|---|---|
| Is this result trading? | any result the closure scan could not confirm — walled host, no page, or a rebrand flag | `WebSearch` "<name> <address>" |
| Does it actually offer the queried product? | product/service queries only — `[breakfast]`, `[donuts]`, `[bubble tea]` | `WebFetch` the menu page |
| What is the official name and address? | the operator's own page was unreadable | `WebSearch` "<name> <street> <city>" |

Three results with two open questions each is six lookups. **Issued as one batch that is a single round trip; issued one at a time it is six, and that difference has been the largest single cost on real tasks** — minutes, not seconds.

The anti-pattern to avoid: search → read the answer → form a view → search again. Decide the whole question list first, fire it, then read everything back together. You almost never need the answer to lookup #1 in order to phrase lookup #2.

## What no tool can settle

Send these back to the screenshot or the guideline, not to another query:

- **Rooftop vs parcel vs neighbour** — the supplied hybrid frame, per `pin-accuracy.md`.
- **Whether a frame shows one building or two** — ask the user; they can zoom and switch layers and you cannot.
- **Which unit under a shared roof** — usually unknowable, which is `Perfect` + follow-up `No`, not `Can't Verify`.
- **The rating itself** — tools inform a rating; `rating-contract.md` decides it.
