# Output Style

`comment-examples.md` governs the **task-facing comment** — the backticked block pasted into the rating tool. This file governs everything else in the chat response: the evidence lines, the tables, and the commentary that follows the rating blocks.

The two are written for different readers and must not be blended. The comment goes to a reviewer inside the tool and stays bare. The chat output goes to the human rater, who needs enough to **check your work and overrule you** — so it carries the distances, the sources, the tiers and the reasoning that the comment deliberately omits.

## Contents

- [Evidence lines](#evidence-lines)
- [Lead with the decisive finding](#lead-with-the-decisive-finding)
- [The candidate ranking table](#the-candidate-ranking-table)
- [Commentary after the ratings](#commentary-after-the-ratings)
- [Tone](#tone)

---

## Evidence lines

One per result, after the ratings. **One clause per dimension it supports, semicolon-separated**, each clause naming both the source and what that source settles. A bare phrase is the floor, not the target — a reviewer should be able to audit each rating without asking you where anything came from.

> `Evidence: Safeway's own store locator confirms 5510 Norbeck Rd, Rockville, MD 20853 with current 6 AM–11 PM hours, so the store exists and is open; it brands the store "Safeway Norbeck Rd" and describes it as a supermarket, so the bare "Safeway" name and "Grocery Store" category are both right; OpenStreetMap independently places the store at 39.09443, -77.11032 against the result's 39.094428, -77.110039, and the pin tip is on the anchor building's rooftop in the supplied hybrid frame.`

Four habits make these useful:

- **Tie each source to a dimension.** "Locator confirms the address *and* the category" beats "checked the locator".
- **Give the numbers.** Coordinates, offsets in metres, distances. These are exactly what the comment must not carry, so this is where they live.
- **Name a weak tier honestly.** `eight independent directory headings all render "degrees" plural; this is not a Tier-1 confirmation` tells the rater how hard to defend it.
- **Say when a pin was judged from a screenshot**, never phrasing it as though you explored the live map.

When a source could not be reached, say which one and what you did instead. `The official locator and the mall directory were both bot-walled, so the unit number rests on directory silence` is a passing answer. Implying you read a page you did not is a critical failure.

## Lead with the decisive finding

When research turns up something that determines the whole task, open with it, above the header block. Do not bury it under the template.

> **The best result wasn't returned.** Your Show Viewport frame has a "The Cheesecake Factory" POI sitting inside the purple box, right beside the user icon… That's **87 metres**.

> **Result 2 is permanently closed** — that's the headline finding. Safeway's own locator returns 404 for that store…

If nothing decisive turned up, skip this and go straight to the header.

## The candidate ranking table

Whenever a distance demotion is in play, show the ranking from Phase 3 — including candidates the task did **not** return. It is the evidence for every distance call in the task, and it lets the rater check the demotion at a glance.

| Cheesecake Factory | Distance to user | Returned? |
|---|---|---|
| **Natick Mall** | **87 m** | **No** |
| Chestnut Hill / Newton | 17.29 km | No |
| Burlington (Result 2) | 24.50 km | Yes |

Mark the un-returned rows. They are usually the point.

## Commentary after the ratings

Close with short titled paragraphs — normally two or three, never a wall. Three kinds earn their place:

**1. Defend a counterintuitive call.** When a rating runs against instinct, name the rule that produced it before the rater has to ask.

> **Why 53 km is still Excellent.** The guideline says explicitly not to demote for distance when the result is the closest possible one… Nothing closer exists to prefer.

> **Result 3 is Bad despite being the closest Safeway to the user.** The device icon marks the centre of the viewport, not the user…

**2. Name the trap.** Say what would mislead someone rating this quickly.

> **The distance figures are a trap on this one.** 25.6 km from the user looks like a Distance/Prominence demotion, and it isn't. The query states its own location… Do not check that box.

> **The trap on this task is a store that no longer exists.** Several directories still list a Victoria's Secret at 835 W Johnson Street — the user's own town… It closed in January 2019.

**3. Hand back what only the human can settle.** Frame ambiguity, a cut-off header, anything you inferred rather than saw. Say what you rated, what would change it, and why they can see what you cannot.

> **The pin is the one call I'd like you to check.** At the frame's scale the tip looks to land roughly 20–25 ft west of the roofline… If you zoom and the tip is touching the roof, switch to **Perfect** and drop the comment. You can see the live map and I'm reading one fixed frame.

Do not write commentary for its own sake. A task where every result is Excellent and every dimension Correct needs none.

## Tone

- **State the rule, not a feeling.** "Sparse chain, closest that exists, no distance demotion" — not "this seems reasonable".
- **Make every claim checkable.** A number, a source, or a named rule. If you cannot supply one, the rating is a hunch and should be reconsidered.
- **Flag assumptions at the point they bite,** not in a footnote. If the Query field was cut off, say so where it affects relevance.
- **Do not hedge a rating you can defend.** Offer the alternative reading and say why it loses, rather than splitting the difference.
- **Separate the two kinds of pushback.** A correction about *what is in the frame* wins immediately — the rater can zoom and switch layers and you cannot. A disagreement about *the rating* gets re-checked against the guideline and changes only if the guideline supports it. Say which one you are doing.
