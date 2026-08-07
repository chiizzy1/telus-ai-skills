# Maps Rating Contract

The single authority for **what the UI offers, what each label is called, and which fields disappear when**. Every label here is transcribed from the official guideline. If a label does not appear in this file, do not use it in a rating or an output template.

Other references explain *how to decide* a rating. This file defines *what you are allowed to say*.

## Contents

- [Task types](#task-types)
- [Query level](#query-level)
- [Result level: the two gate checkboxes](#result-level-the-two-gate-checkboxes)
- [Field availability matrix](#field-availability-matrix)
- [Relevance](#relevance)
- [Name and Category Accuracy](#name-and-category-accuracy)
- [Address Accuracy](#address-accuracy)
- [Pin Accuracy](#pin-accuracy)
- [Comment triggers](#comment-triggers)
- [Release Survey](#release-survey)
- [Labels that do not exist](#labels-that-do-not-exist)

## Task types

| Task type | Rates relevance | Rates Name/Category, Address, Pin |
|---|---|---|
| Search Relevance | Yes | No — stop after relevance |
| Search 2.0 | Yes | Yes, for whichever fields the UI presents |

For any result in a Search 2.0 task you may be asked for all ratings, some, one, or none. This is expected and is **not** a reason to escalate or release. Rate only what is shown.

Some results appear normal or greyed out with no rating fields at all. No rating is required. Also expected; also not a technical issue.

## Query level

One top-level question per query, answered **before** rating any result, and answered even when the task returns no results.

**Is there a navigational result for this query?**

| Answer | Meaning |
|---|---|
| `Yes` | Exactly one real-world result could completely satisfy the user intent |
| `No` | More than one real-world result could satisfy it |

The question is about the real world, not about the results shown. You do not need to see the results to answer it.

## Result level: the two gate checkboxes

Checked in this order, before any rating.

**1. `Result name/title is in unexpected language or script`**

Judges the result **name/title only** — not the address details beneath it. Expected when the name is in the language/script of the test locale, the query, the result region, any combination of those, or is an official company/chain/brand name commonly used in that market.

Not an unexpected-language issue: missing or added diacritics (`e` for `é`), and other minor spelling differences. Use this box only for problems that interfere with understanding the name/title.

Address details in an unexpected language are a different thing entirely — those go to `Incorrect – Language/Script Issue` under Address Accuracy.

> Checking this box **completes the result**. Every other field becomes unavailable.

**2. `Business/POI is closed or does not exist`**

Applies to business/POI results only — **never** to address-type results. Use it when research shows the result is closed or never existed, is randomly moving (a food truck with no fixed schedule), or is a non-recurring past event with no remaining maps intent.

Requires evidence that the business is no longer operational. When resources cannot settle it, assume the business could exist and rate Name, Address, and Pin as `Can't Verify` — unless there is an obvious data error such as a missing mandatory address component or a pin in the ocean, which stays rateable.

Treat a temporary closure as open when the business announces it on its own webpage or managed social account. There is no limit on how long that closure may last.

> Checking this box leaves **only relevance** rateable. Rate relevance as if the place were open and did exist. Never invent Name, Address, or Pin ratings for a gated result.

## Field availability matrix

| Condition | Navigational Q | Relevance | Name/Category | Address | Pin |
|---|---|---|---|---|---|
| Search Relevance task | Yes | Yes | — | — | — |
| Search 2.0, no gate triggered | Yes | Yes | Yes | Yes | Yes |
| `Unexpected language or script` checked | Yes | **Hidden** | **Hidden** | **Hidden** | **Hidden** |
| `Closed or does not exist` checked | Yes | Yes | **Hidden** | **Hidden** | **Hidden** |
| Result shown with no rating fields | Yes | — | — | — | — |
| UI simply omits a dimension | Yes | as shown | as shown | as shown | as shown |

A hidden field gets no rating and no comment. Say it was gated; do not guess what it would have been.

## Relevance

Rated independently of every data inaccuracy. Always assume the result exists and its displayed data is correct — even when your research proved the opposite.

| Label | Definition |
|---|---|
| `Navigational` | The most likely result implied by the query, location, and/or viewport that completely satisfies a distinct user intent — via extreme prominence, uniqueness, or proximity |
| `Excellent` | A high-quality result that clearly satisfies user intent. Multiple results can be Excellent, and it is the highest initial rating for ambiguous queries and any query not eligible for Navigational |
| `Good` | Only partially satisfies intent, due to relevance, prominence, or distance |
| `Acceptable` | Technically satisfies intent but does so poorly, due to relevance or distance |
| `Bad` | Does not satisfy intent, due to lack of relevance or great distance when closer satisfying results exist |

Rating one result `Navigational` does not stop other results from satisfying the query to a lesser degree.

**Demotion checkboxes — mandatory at `Good` or below:**

| Checkbox | When |
|---|---|
| `User Intent issue` | The result only partially fulfils the query intent |
| `Distance/Prominence issue` | Too far based on user or viewport location; or less prominent than the initial query intent implies; or the query asked for something at a specific location and the result is not at or near it |

Select both when both drove the rating. A `Good`-or-below rating also requires a comment.

## Name and Category Accuracy

Also written as "Name Accuracy" in the guideline. One rating covering **both** the business/POI name and its category — a fault in either demotes the combined rating.

| Label | When |
|---|---|
| `n/a` | All address-type results — residential addresses, streets, localities, regions, countries. They have no name or category to rate |
| `Correct` | The name is one the location actually uses for itself on official sources, and the category is right |
| `Partially Correct` | The name is recognisable but flawed — misspelling, missing punctuation, extra words, a misspelled location modifier |
| `Incorrect` | The name is unrecognisable, **or** the category is wrong, misleading, misspelled, or in an unexpected language |
| `Can't Verify` | The name cannot be confirmed or denied with available resources and nothing is objectively wrong with it |

**An incorrect category forces `Incorrect` regardless of how accurate the name is.**

**Issue checkboxes — presented at `Partially Correct` or `Incorrect`:** `Name Issue`, `Category Issue`. Use one or both.

## Address Accuracy

A **parent rating** plus, when the parent is `Incorrect`, checkboxes naming what is wrong. Do not present the checkboxes as if they were top-level ratings.

**Parent rating:**

| Label | When |
|---|---|
| `Correct` | All required components present and accurate |
| `Correct with Formatting Issue` | Everything correct and present but not in the expected format — component order, extra spacing, double comma, non-required but correct components |
| `Incorrect` | One or more components wrong or missing, or one of the issue types below applies |
| `Can't Verify` | Cannot be confirmed either way — no official page, no official address listed, no street imagery, or the official source uses an unexpected format such as an intersection or exit address |

**Component checkboxes, available under `Incorrect`:** `Street Number`, `Unit/Apt`, `Street Name`, `Sub-Locality`, `Locality`, `Region/State`, `Postal Code`, `Country`.

**Issue checkboxes, available under `Incorrect`:**

| Checkbox | When |
|---|---|
| `Incorrect – Address does not exist` | No building and no officially assigned plot at that address. **Address-type results only** — never for POI addresses |
| `Incorrect – Language/Script Issue` | Any address **component** in an unexpected language or script. Not for the name/title, which uses the result-level gate |
| `Incorrect – Country-Specific Issue` | An address problem no other checkbox covers, or additional components beyond the country's normal format that are very unusual or wrong |
| `Incorrect – Other Issue` | Anything not covered above: duplicate components, the POI name repeated in the address, natural features carrying street-address elements, P.O. Box addresses |

**Three gating rules that are easy to get wrong:**

1. Never select an issue **and** a component to report the *same* problem. Do not mark `Language/Script Issue` for the whole address *and* `Street Name` because the street name is in the wrong language.
2. You may select both when the faults are genuinely separate — a language issue across the address *plus* `Street Number` for a numeric error unrelated to language.
3. Once any component is marked `Incorrect`, `Correct with Formatting Issue` is no longer selectable. Report formatting problems you still want to flag via `Incorrect – Other Issue`.

A missing **required** component is `Incorrect`, not `Correct with Formatting Issue`.

## Pin Accuracy

Rated on its own evidence. A pin can be correct while the address is wrong.

| Label | When |
|---|---|
| `Perfect` | Directly on the listed result's rooftop, or on the listed feature where the entity has no rooftop |
| `Approximate` | Inside the result's property boundaries but outside the Perfect area — same property, same side of the street, same block |
| `Next Door` | Anywhere on the property immediately adjacent — same street, same street name, same side, first property to either side, same block |
| `Wrong` | Outside the property boundaries of both the result and its neighbouring properties |
| `Can't Verify` | Placement cannot be confirmed or denied with available resources |

**Follow-up, presented after `Perfect` — `Does the available evidence indicate the result's precise location?`**

| Answer | When |
|---|---|
| `Yes` | The best available evidence pins down the precise location |
| `No` | It does not — e.g. a parcel with several rooftops and no way to tell which, or a shared rooftop with several POIs and no way to tell where under it |

**Two hard rules:**

- A missing pin is `Wrong`. If pins are missing **five or more times in a row**, release the task for technical reasons and explain in the comment.
- There is no `Next Door` inside a shared space. Two buildings sharing a parcel or parking lot can never be `Next Door` to each other, and nothing outside the Approximate area gets `Next Door` — it is `Wrong`.

## Comment triggers

A comment is mandatory for:

- Any relevance rating of `Good`, `Acceptable`, or `Bad`.
- Any data rating that is not `Correct` (Name/Category, Address) or `Perfect` (Pin).
- `Incorrect – Other Issue`, which additionally requires links to the resources used.
- A release for technical reasons.

Every comment: state the user intent, name the guideline section behind the demotion, give the correct information and a direct source link when you found something wrong, shorten long URLs, stay concise, write in English whatever the test locale, and include no PII.

## Release Survey

`Adult Content` · `Technical Issue` · `Not Enough Time Allocated` · `Other`

Never release because the call is hard, because the query looks unrelated to maps (rate every result `Bad`), because the query or results sit outside your market, because the query returned no results (answer the navigational question and submit), or because the query is in a foreign language (research or translate it).

## Labels that do not exist

Guard against these. Each is a plausible-sounding invention, not a UI option:

| Not a label | Use instead |
|---|---|
| Pin Accuracy `Acceptable` | `Approximate` or `Next Door` |
| Address Accuracy `Address Does Not Exist` as a top-level rating | `Incorrect` + `Incorrect – Address does not exist` |
| Address Accuracy `Language/Script Issue` as a top-level rating | `Incorrect` + `Incorrect – Language/Script Issue` |
| Address Accuracy `Country-Specific Issue` / `Other Issue` as top-level ratings | `Incorrect` + the matching issue checkbox |
| Relevance `HS` / `S` / `SS` / `NS` | That is Search SBS. Maps uses Navigational–Bad |
| Name Accuracy `Partially Incorrect` | `Partially Correct` |
