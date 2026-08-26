# Worked Examples From The Guideline

Use with `../SKILL.md`. Every pair below is an official example from the Related Results guidelines (January 2026). Use them as lookup precedent: find the pair whose *shape* matches the one you are rating, then apply the rule that decided it.

Precedent is a check on your reasoning, not a substitute for it. A pair that resembles one of these still has to be researched, because the rating often turns on a fact about that specific POI.

## Contents

- [Excellent](#excellent)
- [Good](#good)
- [Acceptable](#acceptable)
- [Bad](#bad)
- [Pairs that look alike and rate differently](#pairs-that-look-alike-and-rate-differently)

## Excellent

| Query | Result | Why |
|---|---|---|
| `[starbucks letterman]` | Starbucks | Business name plus a street. Any Starbucks is an exact match. |
| `[kfc chicago]` | KFC | Location word is already satisfied. Any KFC is an exact match. |
| `[food]` | Taco Bell | No type specified, so anything offering food fits. |
| `[mall near me]` | Sandcreek Commons | A mall was asked for and a mall was returned. |
| `[ev station]` | EVgo Charging Station | Exactly the service asked for. |
| `[golf store]` | Golf Galaxy | Specializes in the queried category. |
| `[willow]` | The Willow - A Blooming Collective | Vague query, result carries the word. |
| `[Costco]` | Costco Pharmacy | Same brand, department inside the queried business. |

## Good

| Query | Result | Why |
|---|---|---|
| `[starbucks]` | Peet's Coffee | Alternative coffee shop. Competitors cap at Good. |
| `[burger king]` | Chick-Fil-A | Both fast food, similar menu and setting. |
| `[ice cream]` | McDonald's | Sells it, but it is a side line at a burger chain. |
| `[matcha]` | Boba Guys | Serves matcha alongside its main boba business. |
| `[chicken wings]` | Pizza Hut | Offers wings, sells mainly pizza. |
| `[ev station]` | Chevron with both gas and EV charging | Provides the service as one of two. Confirm the chargers exist. |

## Acceptable

| Query | Result | Why |
|---|---|---|
| `[motor oil]` | Target | Stocks it, is a general retailer. |
| `[golf store]` | Dick's Sporting Goods | Sells golf gear among all sports, not dedicated to it. |
| `[ontario mills]` | UNIQLO Ontario Mills | Mall queried, store inside it returned. |
| `[uniqlo]` | Ontario Mills | Store queried, the mall containing it returned. |
| `[sushi]` | Ramen Nagi | Both Japanese. No sushi, but not a surprising result. |
| `[coffee]` | Boba Works | No coffee, but the same beverage field. |

## Bad

| Query | Result | Why |
|---|---|---|
| `[chase bank]` | Autozone | No relationship. |
| `[cvs near me]` | CV Capital Funding | Shared letters, unrelated intent. |
| `[ev station]` | Chevron with no EV charging | Service not available. |
| `[motor oil]` | Macy's | Does not sell it at all. |
| `[uniqlo]` | The Mall at Short Hills | Mall does not contain the store. |
| `[vegan restaurant]` | McDonald's | Dietary constraint violated. |
| `[dry cleaning]` | Dry Creek Vineyards | Shared word, unrelated intent. |
| `[fast food]` | Alexander's Steakhouse | Fine dining against a fast food intent. |
| `[dinner]` | Starbucks | Does not serve the meal asked for. |
| `[sushi]` | Haidilao Hotpot | Different meal type. User would be surprised. |
| `[safeway]` | Starbucks inside the Safeway | Different brand inside the queried business. |
| `[dog park]` | Dog grooming | Clear intent, shared word only. |

## Pairs that look alike and rate differently

These are the comparisons worth holding in mind, because the surface shape is nearly identical and the rating is not.

| | |
|---|---|
| `[golf store]` → Golf Galaxy is **Excellent** | `[golf store]` → Dick's Sporting Goods is **Acceptable** |
| `[sushi]` → Ramen Nagi is **Acceptable** | `[sushi]` → Haidilao Hotpot is **Bad** |
| `[ev station]` → Chevron with chargers is **Good** | `[ev station]` → Chevron without them is **Bad** |
| `[Costco]` → Costco Pharmacy is **Excellent** | `[safeway]` → Starbucks inside it is **Bad** |
| `[uniqlo]` → Ontario Mills is **Acceptable** | `[uniqlo]` → The Mall at Short Hills is **Bad** |
| `[willow]` → The Willow is **Excellent** | `[dog park]` → Lazy Dog Restaurant is **Bad** |

In four of those six, the rating turns on a fact you can only get by researching the specific POI: whether that Chevron has chargers, whether that mall has a UNIQLO, whether the brand inside is the queried brand. Rate the pair, not the pattern.
