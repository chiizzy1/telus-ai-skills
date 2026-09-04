# URL (§4)

Whenever possible the listing should show an **official website**. Only if none exists
may an official social media page take its place.

| Option | Meaning |
|---|---|
| **Correct** | Official website homepage; or the location-specific page where one exists; or — if there is no official website — the claimed social page updated within the past year |
| **Partially Correct** | Multi-location POI: a location-specific page (site or social) exists, but the URL leads to the parent homepage or the business-wide social page |
| **OK Without** | No URL displayed, and research confirms no official website and no qualifying social page |
| **Missing** | A qualifying official presence exists, but no URL is listed |
| **Incorrect** | See the list below |
| **Can't Verify** | The site exists but returns a 503, a maintenance page, or another signal of **temporary** downtime |

## The conditional that decides most multi-location cases

> If a location-specific page exists → that page is `Correct`, the parent homepage is
> `Partially Correct`. **But if location-specific pages are not available**, the main
> page (or the page carrying the addresses) is **`Correct`**.

So `Partially Correct` is never safe by default. Go and check whether the chain
publishes per-location pages — many do, under a store locator, and the answer turns
entirely on that. A Shell station homepage is `Partially Correct` precisely because
`find.shell.com` publishes a page per station; a chain with no such pages would make
the identical homepage `Correct`.

The same rule applies to social media: a location-specific social page makes the
business-wide page `Partially Correct`; if no location-specific social page exists, the
business-wide page can be `Correct`.

## `Incorrect` — the full list

- Points to an irrelevant or unofficial site.
- Points to the **wrong** location-specific page.
- Points to an irrelevant sub-page of the official site.
- Points to an outdated presence — a replaced, unmaintained social account.
- Redirects to a domain-parking or spam page.
- **Leads to the POI's official social page when an official website exists** and
  should have been prioritised.
- Leads to an official social page **not updated within the past year**.
- Returns a **404** or similar permanent-access error.

> A 404 is `Incorrect`. A 503 is `Can't Verify`. The distinction is permanent versus
> temporary, not reachable versus unreachable — and it is not a place to record that
> *your* fetch failed.

## What never counts as a correct URL (§4.3)

Business directory sites such as Yellow Pages · third-party sites, **even where the
business claims and actively updates the page** · any URL not associated with the POI.

## Unattended POIs

Transit stops, bike racks and similar do not need a URL — absent, they are
`OK Without`. But if a URL *is* listed for one, it must be confirmed through official
sources, and then the standard options apply.

## Multiple official social pages

Where a POI has no website but several claimed social pages all updated within the
past year, **any of them is `Correct`**.
