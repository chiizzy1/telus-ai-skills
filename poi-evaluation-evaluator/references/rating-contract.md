# Rating Contract

The exact option set for every question, transcribed from the rendered guideline. This
file is the wrong-rubric detector.

> **If the task UI offers an option that is not in this file, you are not on a POI
> Evaluation task.** Stop and get the right guideline. Noticing the anomaly is not
> enough. Explaining it away is the failure. And hedging is not enough either — a
> confidence estimate does not substitute for the governing document.

## 1 · Eligibility (§3.1.1)

`Conventional POI` · `Seasonal` · `Home Based` · `Service Area` · `Mobile` · `Not a POI` ·
`Can't Verify`

`Not a POI` ends the task. `Can't Verify` is for an entity that cannot be verified at
all from insufficient, outdated or unreliable information.

## 2 · State (§3.2.1)

`Active` · `Temporarily Closed` · `Permanently Closed` · `Can't Verify`

`Temporarily Closed` removes the Hours question.

## 3 · URL (§4.1)

`Correct` · `Partially Correct` · `OK Without` · `Missing` · `Incorrect` · `Can't Verify`

## 4 · Name (§5.1)

`Correct` · `Partially Correct` · `Incorrect`

**No `Can't Verify`.** On `Partially Correct` or `Incorrect`, tick every applicable
error component: Acronym/Abbreviation · Article · Capitalization · Misspelling ·
Punctuation · Synonyms · Missing Words · Extra Words · Service-Level Mismatch ·
Holding Name/Corporate Structure · Category as Name · Other.

## 5 · Address (§6.1)

`Correct` · `Correct - Formatting Issue` · `Incorrect` · `OK Without` · `Missing` ·
`Can't Verify`

On `Incorrect`, tick every incorrect or missing component. Components include the
address parts themselves plus Language/Script Issue, Market Specific Issue, and Other.

## 6 · Pin (§7.1)

`Perfect` · `Approximate` · `Next Door` · `Wrong` · `Can't Verify`

`Perfect` triggers: *Does the available evidence indicate the POI's precise location?*
→ `Yes` · `No`.

## 7 · Phone (§8.1)

`Correct` · `OK Without` · `Missing` · `Incorrect` · `Can't Verify`

## 8 · Category (§9.1)

`Correct` · `Approximate` · `Missing` · `Incorrect`

**No `Can't Verify`.** `Approximate` is real — it is the band for a category that
accurately represents the POI but is overly broad or only a partial fit, where the
reference list contains something more relevant.

## 9 · Hours (§10.1)

Options are **dynamic**, and depend on whether hours data is present in the listing:

| Listing state | Options offered |
|---|---|
| Hours data available | `Correct` · `Incorrect` · `Can't Verify` |
| `Data not available` | `OK Without` · `Missing` · `Can't Verify` |

If you were offered `Correct` you were shown hours; if you were offered `Missing` you
were not. Do not reach for a band the interface did not present.

## Corrections you may be asked for

| Trigger | Field |
|---|---|
| URL `Partially Correct`, `Incorrect`, `Missing` | The correct URL |
| Name `Partially Correct`, `Incorrect` | The correct name |
| Address `Incorrect`, `Missing` | The correct address |
| Pin not `Perfect` | Corrected coordinates |
| Phone `Incorrect`, `Missing` | The correct number |
| Category not `Correct` | The best-fit category string |
| Hours `Incorrect`, `Missing` | The correct weekly hours, plus URL and screenshot evidence |
