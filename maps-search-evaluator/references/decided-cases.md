# Decided Cases

Cases the official guideline has **already ruled on**, quoted verbatim from the rendered PDF.

These are not examples to reason about. They are decisions. **When your reasoning and a decided case disagree, the case wins** — that is the quality gate's first rule, and it is the most common way a confident, well-argued rating comes out wrong.

Look the shape up here **before** forming a view on relevance, not after.

## Contents

- [How to search the source](#how-to-search-the-source)
- [Lack of connection — every case is Bad](#lack-of-connection--every-case-is-bad)
- [The three defences the guideline rejects](#the-three-defences-the-guideline-rejects)
- [Distance ladder — many possible results](#distance-ladder--many-possible-results)
- [Distance ladder — few possible results](#distance-ladder--few-possible-results)
- [Applying a case to a new task](#applying-a-case-to-a-new-task)

---

## How to search the source

> **The extracted text contains non-breaking spaces.** `grep "Rate Bad"` returns **zero hits** even though seven Bad cases exist. An agent trusting that grep would conclude the guideline never rates anything Bad. Always normalise ` ` first.

```bash
python3 - <<'PY'
import re
p = "TELUS-TASKS/maps-extracted/text.md"
t = open(p, encoding="utf-8").read().replace(" ", " ")
for m in re.finditer(r"Rate (Bad|Excellent|Good|Acceptable|Navigational)\b", t):
    print(re.sub(r"\s+", " ", t[max(0, m.start() - 700):m.end()]), "\n---")
PY
```

A `grep` that tolerates the NBSP as a single character also works: `grep -nE "Rate.(Bad|Excellent|Good|Acceptable)" TELUS-TASKS/maps-extracted/text.md`

## Lack of connection — every case is Bad

All seven sit in one table in §5.2 *Satisfying User Intent*. Reasons are the guideline's own words.

| Query | Result returned | The guideline's reason | Rating |
|---|---|---|---|
| `[airport]` | Santa Cruz Boardwalk | "no connection between the query and the result" | **Bad** |
| `[Raging Waters 2333 South White Rd San Jose]` | 2333 South White Rd | "correct address, but does not include the business named in the query, so users will have no way of knowing if this is truly connected to the business or not" | **Bad** |
| `[Raging Waters]` | 2333 South White Rd | "Query is the name of a business and result is for the correct address, but does not include the business name" | **Bad** |
| `[valley fair mall]` | Macy's, inside that mall | "Result is for a store, not a mall. This store is inside the requested mall, but does not satisfy the intent of the query, which is the whole mall" | **Bad** |
| `[macy's]` | Westfield Valley Fair, the containing mall | "This mall contains the requested store, but this result is the whole mall, not the single store the user asked for" | **Bad** |
| `[costco]` | Costco Gasoline, 1601 Coleman Ave | "The store and the station are at the same address and share a brand name, **but the result is not what the user asked for**" | **Bad** |
| `[costco gas]` | Costco store, 1601 Coleman Ave | same wording, reversed | **Bad** |

**The shape, generalised.** The query names entity A; the result is entity B, where B is *inside* A, *contains* A, or is a *differently-functioning sibling* of A sharing its brand and address. Every instance is Bad. Data dimensions are still rated normally — Bad relevance does not imply a wrong name, address or pin.

## The three defences the guideline rejects

Each is a plausible argument for rating higher. Each is explicitly considered and overruled in the text above. Do not re-derive them:

1. **"Same address."** Rejected twice, in both Costco rows, in those exact words.
2. **"Shares a brand name."** Rejected in the same sentence, both times.
3. **"It is inside / it contains the thing they asked for."** Rejected in the Valley Fair and Macy's rows.

A fourth, not in the text but the same error: *"navigating there gets the user to the right building."* The Costco store and its gas station are one site; the guideline still rates both directions Bad.

**Worked applications on real tasks:**

| Task query | Result | Matching case | Rating |
|---|---|---|---|
| `[walmart in Elkton, MD]` | Walmart Pharmacy — department inside the Supercenter, same address | `[costco]` → Costco Gasoline | **Bad** (User Intent) |
| `[walmart in Elkton, MD]` | Walmart Connection Center — same | `[costco]` → Costco Gasoline | **Bad** (User Intent) |
| `[loves travel stop Boise, ID]` | Love's Truck Care, same address | `[costco]` → Costco Gasoline | **Bad** (User Intent) |
| `[Chevron 225 Langley Drive Lawrenceville GA]` | 225 Langley Dr, bare address | `[Raging Waters …address]` | **Bad** (User Intent) |
| `[211 w119th st, Pretty flawless hair, Chicago]` | 211 W 119th St, bare address | `[Raging Waters …address]` | **Bad** (User Intent) |

## Distance ladder — many possible results

`[starbucks]`, user **inside** a fresh viewport. Verbatim from the worked example:

| Result | Rating | The guideline's words |
|---|---|---|
| ① 865 Market Street | **Excellent** | "for Starbucks locations that are in close proximity to the user" |
| ② 170 O'Farrell St | **Good** (Distance/Prominence) | "for locations that are a bit farther away from the closest relevant locations to the user" |
| ③ 264 Kearny St | **Acceptable** (Distance/Prominence) | "for relevant locations that are even farther away from the user but still inside the viewport" |
| ④ 580 California St | **Bad** (Distance/Prominence) | "When there are many locations close to the user, rate Bad for locations that are significantly farther away **and** outside the viewport" |
| ⑤ 140 Mason Street | **Excellent** | "in close proximity to the user" |

Two things this settles. **Multiple results can be Excellent** — ① and ⑤ both are. And **Bad on distance needs two conditions together**: significantly farther *and* outside the viewport, *while* many locations sit close to the user. One condition alone is not enough.

## Distance ladder — few possible results

`[zara]`, Miami. Same query family, different supply, and the ladder flattens:

| Result | Rating | The guideline's words |
|---|---|---|
| ➀ 19501 Biscayne Blvd, Aventura | **Excellent** | "for the closest Zara location, **even when outside the fresh viewport**" |
| ② 420 Lincoln Rd, Miami Beach | **Good** (Distance/Prominence) | "When there aren't any possible results in the fresh viewport, rate Good for locations that are a bit farther away from the user/viewport" |
| ③ 590 Collins Ave, Miami Beach | **Good** (Distance/Prominence) | identical wording |
| ④ 701 S Miami Ave, Miami | **Good** (Distance/Prominence) | identical wording |

**Three results share one Good band.** Where supply is sparse, do not spread results across Excellent → Good → Acceptable by rank; the closest is Excellent and the rest sit together in Good. Splitting hairs between 2nd and 3rd closest is a dense-market behaviour, and the guideline shows it only for Starbucks.

## Applying a case to a new task

Match on **shape**, never on the business:

1. Does the query name entity A while the result is B — inside A, containing A, or a same-brand sibling with a different function? → the lack-of-connection table. **Bad.**
2. Does the query name a business *and* an address, while the result is the bare address? → `[Raging Waters]`. **Bad.**
3. Is this a distance call? → count the real-world candidates from the recon's Phase 3 table first. Many → the Starbucks ladder. Few → the Zara ladder.
4. Only when no case matches do you reason from the general rules in `relevance.md`.

State which case you applied in the chat output's evidence line. If you find yourself explaining why a decided case *shouldn't* apply here, stop — that is the failure mode this file exists to prevent.
