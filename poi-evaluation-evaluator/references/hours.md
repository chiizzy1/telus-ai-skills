# Hours (§10)

The strictest sourcing rule in the guideline, and a dynamic option set.

Not asked at all when State is `Temporarily Closed`.

## Dynamic options (§10.1)

| Listing state | Options offered |
|---|---|
| Hours data present | `Correct` · `Incorrect` · `Can't Verify` |
| `Data not available` | `OK Without` · `Missing` · `Can't Verify` |

| Option | Meaning |
|---|---|
| **Correct** | Verified against official online sources |
| **OK Without** | No hours listed, and the POI is not expected to have them — including businesses open 24 hours |
| **Missing** | No hours listed, but research shows hours are available |
| **Incorrect** | Any listed day or time is inaccurate |
| **Can't Verify** | Cannot be verified from an official source |

## Sourcing — official only, and narrower than everywhere else

> **§10.1.1:** hours may be verified **only** from the business's official website or
> official social media page.

Explicitly barred, even here where they would be allowed for other dimensions:

- Unofficial social pages
- Crowdsourced review sites, **claimed or unclaimed**
- Online street imagery
- SERPs
- **Online maps services and other third-party sites — even when the POI's own
  official source directs you to them**

That last clause is the trap. An official site that says "see our hours on Google" does
not license you to use Google's hours.

## Conflicts (§10.1.1.2)

- Official **website** disagrees with official **social page** → rate on the **website**.
- The official website itself carries **two contradictory sets** of hours for a single
  schedule → **`Can't Verify`**.

## Get the full week (§10.1.1.1)

Many sources default to showing only the current day. That is not the week. Navigate to
Contact or About subpages, and open any dropdown or toggle that expands the full
schedule, before concluding anything.

## General rules (§10.1.2)

- **All days and times must match.** One wrong day makes the whole thing `Incorrect`.
- **Omitted days read as closed.** A day absent from the listing is rated as though
  listed closed.
- **Regular weekly closures need no entry.** A restaurant closed every Monday does not
  need Monday listed; if every other day is right, the hours are `Correct`.
- **Check which day the source starts on.** The tool generally starts at Sunday; sources
  may start at Monday or at the current day. Align them before comparing.
- **Formatting never demotes**: 12- or 24-hour clocks; days as a range or individually;
  days out of order.
- **One minute of tolerance.** An official 2:59pm open against a listed 15:00 is
  acceptable; an official 6:29pm close against 18:30 is acceptable.
- **24-hour representations**: `00:00-00:00`, `00:00-24:00` and `0:00-23:59` all pass.
  `0:00-23:58` fails — a minute of the day is missing.
- **Midnight**: `00:00`, `24:00` and `23:59` are all acceptable variants.
- **Unattended POIs** with no hours → `OK Without`; if hours *are* listed, confirm them
  through official sources.

## POIs not expected to have hours (§10.6)

### Always open

Listed as 24 hours a day → `Correct`. Expected always-open with **no** hours listed →
`OK Without`.

**Hotels** (§10.6.1.1) carry the full ladder:

| Situation | Rating |
|---|---|
| Always open, listed as 24h | `Correct` |
| Expected always open, nothing listed | `OK Without` |
| Fixed **lobby** hours exist, nothing listed | `Missing` |
| Official sources give no fixed hours, but specific hours are listed | **`Can't Verify`** |
| Official site publishes specific lobby hours | Rate normally |

Do **not** rate hotel hours from reception-desk or other service hours — they are not
lobby hours. A hotel publishing only reception hours, with hours listed, is
`Can't Verify`.

### By appointment (§10.6.2.1)

| Situation | Rating |
|---|---|
| Appointment-only, nothing listed | `OK Without` |
| Appointment windows listed as though they were open hours | **`Incorrect`** |
| Both normal business hours and appointments exist; listing matches the business hours | `Correct` |
| Both exist; nothing listed | `Missing` |

### Schools and universities (§10.6.2.2)

No hours published → `OK Without`. Hours published — including office or departmental
hours — → rate normally.

> **Do not infer weekdays.** Where official hours state `8am-5pm` without naming days,
> the expectation is **every day of the week**. A listing that excludes the weekend is
> `Incorrect`; one covering all seven days is `Correct`. Most schools operate on
> weekdays, and that is exactly the inference the guideline forbids.

### Daylight-based (§10.6.3)

Parks, beaches and trails closing at sunset are not expected to carry fixed hours.

| Situation | Rating |
|---|---|
| Nothing listed | `OK Without` |
| Fixed open time accurate, close left open (`8:00-`) | `Correct` |
| Fixed open time inaccurate (`10:00-` against an 8am open) | `Incorrect` |
| A specific clock time substituted for sunset (`08:00-17:00`) | `Incorrect` |

## Other sections to consult

Seasonal hours §10.3 · additional service hours for restaurants §10.4.1 and pharmacies
§10.4.2 · temporary changes §10.5 · corrections §10.7 · evidence collection, including
the URL and screenshot requirements, §10.8.
