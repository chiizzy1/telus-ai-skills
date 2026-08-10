# Comment Examples

Task-facing comments are pasted verbatim into the rating tool and read by a human reviewer. `rating-contract.md` says **when** a comment is mandatory; this file says **how it must read**.

Every comment below is a worked example from a real task. Copy the shape, not the words.

## Contents

- [The formula](#the-formula)
- [Worked examples by trigger](#worked-examples-by-trigger)
- [Anti-patterns](#anti-patterns)
- [Links](#links)

---

## The formula

Two sentences, occasionally three. Plain words.

1. **Open by naming the intent**, in the form `The query is …`. State what the user wanted, not what the result is.
2. **Then say what the result does and why it was demoted**, in one sentence per fault.
3. **If you corrected something, give the corrected value and a shortened source link.**

Name the competing result **by name or street**, never by a distance figure. "Much farther than the Boba Chai result" is what a reviewer can check at a glance; "3.8 km versus 0.4 km" is what they have to decode.

**Links attach to corrections, not to demotions.** Demoting on distance or intent asserts nothing factual, so there is nothing to source — those comments stay link-free. Correcting a name, an address component or a category does assert a fact, so it carries the corrected value and where it came from.

Write in English regardless of test locale. Never include PII — no personal names, contact details or account numbers, even when they appear as map labels.

## Worked examples by trigger

**Distance demotion, a closer option was returned**

> `The query is a Chase Bank near the user. This Montague Street branch satisfies the intent but is much farther than the Front Street result.`

**Distance demotion, the better option was NOT returned**

> `The query is a Cheesecake Factory near the user. This Peabody result is the farthest of the three, and there is a Cheesecake Factory in the Natick Mall the user is already in.`

**Viewport is the location intent, result sits outside it**

> `The query is a Safeway near the area the user is viewing. This result sits outside that area, and the Norbeck Rd result is inside it.`

Note the opening: when the viewport carries the intent, say "the area the user is viewing", not "near the user". The phrasing is doing real work — it tells the reviewer which rule you applied.

**Partial category fit**

> `The query is a bubble tea store near the user. This is a Thai restaurant that also serves boba, so it only partly fits the intent.`

**Category miss, plus a wrong classification**

> `The query is a zoo near the user. This is a county boat launch and picnic park with no animals, so it is not a zoo and the Wildlife Park category is wrong.`

**Wrong service type at the right address**

> `The query is a Love's travel stop in Boise. This result is the truck repair shop rather than the travel stop, and its pin sits in the truck parking area instead of on the service building.`

**Query named a business AND an address; result is the address alone**

> `The query is for the Chevron at 225 Langley Dr. This result is only the address, so the user cannot tell whether it is the gas station they asked for.`

**Result is a different street from the one queried**

> `The query is 615 East Ave N. This result is 615 North Ave in Hartland, which is a different street and a long way from the user. The nearest real 615 East Ave N is in La Crosse.`

**Closed business, demoted on distance rather than closure**

> `The query is a Safeway near the area the user is viewing. This result sits outside that area, and the Norbeck Rd result is inside it. The store also closed permanently in April 2025.`

The closure goes **last** and as a separate sentence, because closure is not what drove the rating. Never write a comment implying a result was demoted for being closed.

**Pin on the property but off the rooftop**

> `The query is 403 4th St in Ridgeway. The pin sits on the property but just off the west edge of the house roof rather than on it.`

**Name or address correction — carries a link**

> `The query is a bubble tea store near the user. This is a Thai restaurant that also serves boba, so it only partly fits. The name should be -18 degrees F Tea House: facebook.com/thaitanickitchen`

**Category correction — carries a link**

> `The query is breakfast near the user. This diner is a long way from the user when Willard has its own breakfast options, and the Sandwich Shop category is wrong for a 24-hour diner: yelp.com/biz/track-s-end-bellevue`

Give the corrected value in plain words, then the shortest URL that shows it. Cite the source you actually opened — not a search page, and never a domain you did not read.

## Anti-patterns

Each of these reads as machine-written and slows a reviewer down:

| Do not write | Write instead |
|---|---|
| `3.789 km from the user versus 0.383 km` | `much farther than the Boba Chai result` |
| `Per §10.4 category distance demotion` | *(nothing — the checkbox already says why)* |
| `User intent is a bubble tea shop; however, given that the result is a Thai restaurant which also offers boba tea as part of a broader menu, and considering…` | two short sentences |
| `Rating: Good. Checkbox: Distance. Comment: far.` | prose, not a field dump |
| `https://www.yelp.com/biz/thai-tanic-and-18-degrees-f-tea-house-sterling-heights` | the same link, shortened |
| a link on a pure distance demotion | no link — nothing factual was asserted |
| a Google or DuckDuckGo results page as the source | the page you actually opened |
| `Closed, so demoted to Acceptable` | closure last, and never as the demotion reason |

Distances and evidence tiers belong in the **chat output's Evidence line**, not the paste buffer. Source links for corrections belong in **both** — the comment carries the one link that backs the correction, the evidence line carries the full picture.

## Links

The contract asks for a source link whenever you report something as wrong, and **requires** links for `Incorrect – Other Issue`.

| Comment type | Link? |
|---|---|
| Relevance demotion — distance, prominence, user intent | **No.** Nothing factual is asserted, so there is nothing to source |
| Name, address-component or category correction | **Yes.** Corrected value, then the shortest URL that shows it |
| `Incorrect – Other Issue` | **Yes, mandatory**, to every resource used |

> `The query is a zoo near the user. This is a county boat launch and picnic park with no animals, so it is not a zoo and the Wildlife Park category is wrong. Marathon County lists the address as 226300 Bluegill Avenue, Wausau, WI 54401, and the park name should not be repeated in the address line: <shortened link>`

Cite only what you opened. A link you did not read is the fabrication failure in the quality gate, and it is worse than no link at all.

**The one thing the contract asks for that we do not do:** name the guideline section behind the demotion. A section number in a pasted comment reads as machine output and adds nothing the checkbox has not already said. This is a deliberate divergence, recorded in SKILL.md — reverse it there if a reviewer asks for citations.
