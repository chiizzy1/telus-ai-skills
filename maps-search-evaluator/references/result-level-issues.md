# Result-Level Issues

Before rating relevance or data accuracy, check each result for two high-level issues. Exact labels and field-hiding rules live in `rating-contract.md`; this file explains how to decide.

## Contents

- [1. Result Name/Title in Unexpected Language or Script](#1-result-nametitle-in-unexpected-language-or-script)
- [2. Business/POI Is Closed or Does Not Exist](#2-businesspoi-is-closed-or-does-not-exist)
  - [The two decisions are independent](#the-two-decisions-are-independent)
  - [Closed/non-existent vs. merely wrong data](#closednon-existent-vs-merely-wrong-data)
  - [When evidence cannot settle it](#when-evidence-cannot-settle-it)
- [3. PERMANENT_CLOSURE Status](#3-permanent_closure-status)
  - [Step 2: Set the checkbox from reality](#step-2-set-the-checkbox-from-reality-not-from-the-status)
  - [Step 3: Set the relevance starting point](#step-3-set-the-relevance-starting-point-from-expectedness)
  - [Combining the two steps](#combining-the-two-steps)
  - [Worked Examples](#worked-examples)

---

## 1. Result Name/Title in Unexpected Language or Script

A result name or title is in an **expected** language or script when it is in:
- The language/script of the **test locale**
- The language/script of the **query**
- A language/script of the **result region**
- Any combination of the above
- An **official company, chain, or brand name** commonly used in the market, even if it's not in any of the above languages

If the result name/title is in an **unexpected** language or script → check the **"Result name/title is in unexpected language or script"** checkbox. **No further rating is required** — all other fields become unavailable.

### Language/Script Decision Rules

| Source | Expected? | Example |
|--------|-----------|---------|
| **Query language** | ✅ Yes | Test locale: en_US, query: `[mystery]`, result: "Mystery Spot" → English matches query. |
| **Test locale language** | ✅ Yes | Test locale: es_ES, query: `[college]`, result: "Colegio Skyline" → Spanish matches test locale. |
| **Result region language** | ✅ Yes | Test locale: en_US, result in Rio de Janeiro, query: `[beach]`, result: "Praia de Copacabana" → Portuguese is the language of Brazil. |
| **Official brand name** | ✅ Yes | Test locale: ar_SA, query: `[ماكدونالدز]`, result: "McDonald's" → Official brand name is always expected. |
| **None of the above** | ❌ No | Test locale: en_US, result in California, query: `[market]`, result: "ေစျးကွက်" (Burmese) → Unexpected. |
| **Wrong regional language** | ❌ No | Test locale: en_US, result in Rio (Portuguese-speaking), result: "Playa de Copacabana" (Spanish) → Spanish is not the language of Brazil. |
| **Wrong brand language** | ❌ No | Test locale: ar_SA, result in Riyadh, query: `[ماكدونالدز]`, result: "マクドナルド" (Japanese) → Not the brand's official name, query language, locale, or region. |

### Short Queries
If the query is so short that the language cannot be identified, assume the query language is that of the test locale.

### Query Locale vs. Test Locale
When the test locale and query locale differ, consider the **query locale** the expected language (it provides more detailed information). Example: Query Locale en_ID, Test Locale id_ID → English is expected.

### Minor Spelling Differences
Do NOT flag as unexpected language/script:
- Missing or added diacritics (e.g., "e" instead of "é")
- Minor spelling differences in unnecessary or less relevant parts of a name

Only flag issues that **interfere with understanding the name/title**.

### Address Title (Address Results)
Address results don't have a name — the first line of the address appears as the title. Flag when this title is in an unexpected language/script.

Some address components are **localized** (city, state, country — may be translated to the test locale language). Others are **not typically localized** (feature types like "square," "bridge," street names, building names).

### Bilingual Areas
In bilingual areas, official names in **any** of the area's languages are expected, unless your Country-Specific Guidelines say otherwise.

---

## 2. Business/POI Is Closed or Does Not Exist

### The two decisions are independent

Almost every mistake in this area comes from merging two separate questions. Keep them apart:

| Decision | Driven by | Never driven by |
|---|---|---|
| **Do I check the closed/non-existent box?** | The **real-world state** your research established | The `status` field in the tool |
| **What relevance rating do I start from?** | Whether a `PERMANENT_CLOSURE` result is **expected or unexpected** | Whether the business is closed |

The status field never decides the checkbox. The checkbox never decides relevance. Research decides the checkbox; expectedness decides the relevance starting point.

### What the checkbox means

Check it when research shows the result is:

- **Closed** — permanently shut down, no longer operating
- **Non-existent** — no such business at the listed address, or never existed
- **Randomly moving** — e.g. a food truck with no fixed schedule
- **A non-recurring past event** with no remaining significance and no maps intent

Requirements and consequences:

- Applies to **business/POI results only** — never to address-type results.
- Requires **evidence** that the business is no longer operational.
- **Checking it leaves only relevance rateable.** Name, Address, and Pin are hidden. Do not produce those ratings, and do not describe what they would have been.
- You must still give a relevance rating, made **as if the place were open and did exist**.

### Never demote to Bad for closure alone

Closure is never by itself grounds for `Bad`. You may find independent reasons to rate `Bad`, but closure cannot be the sole one.

### Closed/non-existent vs. merely wrong data

If the entity actually exists nearby but the result's name or address is wrong, that is a **data-accuracy problem**, not non-existence. Use the data drop-downs and leave the closure box unchecked.

Worked case from the guideline: a `Caribou Coffee` result carries the chain's official URL and a phone number matching a real nearby Caribou, but the street address belongs to a Nike store in the same shopping centre. The business plainly exists — so the box stays unchecked and the fault is recorded as `Address Accuracy: Incorrect – Street Number, Street Name`, with Name `Correct` and Pin `Perfect`.

### Temporarily closed

Treat a temporarily closed business **as open** when the closure is announced on the business's own webpage or managed social account — construction, remodelling, vacation, any reason. There is **no limit** on how long that closure may last.

### When evidence cannot settle it

- Assume the business **could exist**.
- Rate Name, Address, and Pin as `Can't Verify`.
- Exception: an obvious data fault stays rateable — a missing mandatory address component, or a pin in the ocean.
- If the evidence is genuinely **tied**, or you are rating **Search Relevance only**, check the closed/non-existent box and rate relevance as if the entity did exist.

---

## 3. PERMANENT_CLOSURE Status

`PERMANENT_CLOSURE` changes **where the relevance rating starts**. It never decides the checkbox, and it is never trusted on its own.

### Step 1: Always research

Whatever the status says, research the real-world state. The status may be wrong in either direction.

### Step 2: Set the checkbox from reality, not from the status

| Real-world state (researched) | Status shown | Closed box | Data fields |
|---|---|---|---|
| Open / exists | none | No | Rateable |
| Closed / does not exist | none | **Yes** | Hidden |
| Open / exists | `PERMANENT_CLOSURE` | No — it is open | Rateable |
| Closed / does not exist | `PERMANENT_CLOSURE` | **Yes** | Hidden |
| Cannot determine | either | No | `Can't Verify` |

The third row is the one people get wrong: a business that research shows is **open** does not get the closed box just because the tool displays `PERMANENT_CLOSURE`. Its data fields stay rateable.

### Step 3: Set the relevance starting point from expectedness

Expectedness is a property of **the query and the surrounding options**, not of the business's condition.

**Expected** — the closed result is the best or only thing that could ever be returned. Both must hold:

- The permanently closed result satisfies the user intent completely, **and**
- No other result satisfies the actual user intent within the area of location intent.

Typical cases: a navigational query that can only return this one closed result; a chain query where every chain location in the area is closed and the nearest open one is significantly farther away.

> **Rate as if open.** In most cases that lands on `Navigational` or `Excellent`.

**Unexpected** — open results exist in the area of location intent that would fully satisfy the intent without altering the query.

Typical cases: category queries, which always have many candidates; queries with several possible interpretations; most chain queries, where open locations remain nearby.

> **Demote by 2.** The highest available rating becomes `Acceptable`.

**Rare exception:** if a category query has only one match in a large area and it is `PERMANENT_CLOSURE`, treat it as *expected* and rate as if open. The guideline calls this extremely rare.

### Combining the two steps

| Situation | Closed box | Relevance | Data fields |
|---|---|---|---|
| Expected `PERMANENT_CLOSURE`, research confirms closed | Yes | As if open — usually `Navigational` / `Excellent` | Hidden |
| Expected `PERMANENT_CLOSURE`, research shows open | No | As if open — usually `Navigational` / `Excellent` | Rateable |
| Unexpected `PERMANENT_CLOSURE`, research confirms closed | Yes | Demote by 2 — max `Acceptable` | Hidden |
| Unexpected `PERMANENT_CLOSURE`, research shows open | No | Demote by 2 — max `Acceptable` | Rateable |
| No status, research confirms closed | Yes | As if open, no demotion for closure | Hidden |
| No status, research shows open | No | Rate normally | Rateable |

Whenever the closed box is checked, "Hidden" means exactly that: report the gate in your output and produce no data ratings.

### Worked Examples

**Expected — Navigational Query:**
- Query: `[99 bottles santa cruz]`, Result: "99 Bottles of Beer on the Wall, PERMANENT_CLOSURE, Santa Cruz, CA"
- This is the specific business the user asked for. Even though it's permanently closed, there's no other "99 Bottles" in Santa Cruz. → Check closed box, rate relevance as if open → **Navigational**.

**Expected — All Chains Closed in Area:**
- Query: `[chico's]`, User in Hamilton ON, Viewport in Toronto ON
- Result ①: "Chico's, PERMANENT_CLOSURE, 100 City Centre Dr, Mississauga, ON" → In center of viewport, no open locations anywhere nearby → Check closed box, rate **Excellent** (as if open).
- Result ②: "Chico's, 5151 Main St, Williamsville, NY" → Closest open location just across the border → rate **Excellent**.

**Unexpected — Open Options Nearby:**
- Query: `[vintage store]`, User in Washington DC
- Result ①: "Meeps Vintage" (open, close to user) → **Excellent**
- Result ②: "Miss Pixie's" (open, close to user) → **Excellent**
- Result ③: "Buffalo Exchange, PERMANENT_CLOSURE" → Open vintage stores exist nearby, so this closed result is unexpected. Check closed box, highest rating is **Acceptable**. Given abundance of nearby results, **Bad** is also defensible.
