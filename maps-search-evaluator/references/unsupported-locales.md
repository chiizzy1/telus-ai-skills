# Unsupported Locales

Source: **Country Specific Guidelines – [Unsupported Locales]**, v1. Read this when the
task's country has no dedicated country guideline of its own.

You are not expected to know the market. You **are** expected to research it before
rating. Sharing a language is not sharing a country: en_US and en_GB diverge on what a
query even means.

## Contents

- [Working out the address format](#working-out-the-address-format)
- [Address components with no obvious match](#address-components-with-no-obvious-match)
- [Diacritics, language and script](#diacritics-language-and-script)
- [Verifying data in a new market](#verifying-data-in-a-new-market)
- [Prominence in an unfamiliar market](#prominence-in-an-unfamiliar-market)
- [Routing — probably a different task type](#routing--probably-a-different-task-type)

---

## Working out the address format

Before rating any address, establish which components the locale actually requires:

1. **Official sources** — the national postal service, government maps, land registry or
   cadastral records.
2. **Universal Postal Union** — publishes addressing systems for member countries.
3. **Chain-business consensus** — check how several chains write their addresses there.
   If most include a sub-locality, it is probably mandatory.
4. **Expat resources** — `expat blog [LOCALE]` forums explain addressing to people who
   did not grow up with it.

## Address components with no obvious match

Match what you find to the TryRating components as best you can. Two decided cases:

| Result | Official | Rating |
|---|---|---|
| **The Button Box**, 17 Patrick Street, Mullingar, Co Westmeath, N91 EW6D, Ireland | **West House**, 17 Patrick Street, … | **Incorrect – Street Number** |
| 30 David Street, **Dunedin 9012**, New Zealand | 30 David Street, **Caversham**, Dunedin 9012, NZ | **Incorrect – Country-Specific Issue** |

Both are counter-intuitive and worth memorising:

- An Irish **building or estate name** occupies the street-number slot. A wrong building
  name is `Incorrect – Street Number` even though a full address is otherwise present.
- A missing **sub-locality** where the locale requires one is
  `Incorrect – Country-Specific Issue`, not `Incorrect – Locality`.

## Diacritics, language and script

**Relevance.** When the query carries a diacritic, results containing it are relevant and
results without it generally are **not** — the user took the trouble to type it.
Exceptions: no matching result carries the diacritic, or omitting it is a common
misspelling.

**POI and business names.** Verify against official resources and treat a wrong or missing
diacritic as a minor or moderate misspelling — so `Partially Correct`, not `Incorrect`,
unless the name becomes unrecognisable.

**Address components.**

| Situation | Rating |
|---|---|
| The diacritic is verifiable via the national postal service, and the result omits or mangles it | **Incorrect** |
| No consensus among postal service, street imagery and official resources | **Not** a demotion — leave it |

**Mixed scripts or languages within one address** → `Incorrect – Language/Script Issue`.

## Verifying data in a new market

- **Claimed social media pages are official resources**, and many markets use them instead
  of websites. See `research-evidence.md`.
- **Government and cadastral maps** are the strongest pin resource in an unfamiliar market
  — they carry property lines, which makes the correct rooftop identifiable in satellite
  view. Reach for these before guessing from imagery alone.
- Third-party map and street-imagery sites can be reliable; prefer the most recently
  updated one you can find.

## Prominence in an unfamiliar market

Prominence varies by locale and cannot be assumed from your own market.

- **Suspected chain** — search the brand name with **no location modifier** to gauge how
  well known it is.
- **Category query** — search the category near the location intent; a more prominent
  real-world result may exist that was never returned.
- **Population density** — judge it from current satellite imagery, since density sets the
  scale for what counts as a distance demotion.

## Routing — probably a different task type

The source document also covers driving and pedestrian **routing**: road signage, illegal
manoeuvres, time-of-day and vehicle restrictions, and road markings — including that a
painted median is legal to cross in Japan and New Zealand but acts as a barrier in
Belgium, Sweden, Hungary and Italy.

**Maps Search Evaluation has no routing dimension.** Nothing in the rating contract asks
you to judge a route. Treat that section as belonging to a separate Routing task family
and do not invent a routing rating here. If a task genuinely asks for one, it is not this
skill — route it via `../telus-evaluator/SKILL.md`.
